from concurrent import futures
import logging
import os
import random
import time
import grpc
import sys
from entities.index_table import IndexTable
from entities.datanode_list import DatanodeListStructure,Datanode
from entities.cluster import Cluster
from uuid import uuid4
#probando
# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from protos import file_pb2_grpc as servicer
from protos.file_pb2 import DatanodeList,Empty,DirectoryContent, CreateRsp, WarningMessage, HeartBeatRsp

logger = logging.getLogger(__name__)


class FileServicer(servicer.NameNodeServiceServicer):
  def __init__(self,dataNodesList:DatanodeListStructure,indexTable:IndexTable):
    self.__dataNodesList=dataNodesList
    self.__indexTable=indexTable
    self.__globalCount=0
    self.__cluster_assign_count=0
    self.__cluster_list=[Cluster(id = 0),Cluster(id = 1)]
    self.__used_ids = {}

  def create(self, request, context):
    filename= request.filename
    chunks_number= request.chunks_number
    operation_type = request.operation
    #Datanodes must be leaders
    availableDatanodes = self.__dataNodesList.get_leaders()
    print(availableDatanodes)
    try:
      if len(availableDatanodes)==0:
        yield CreateRsp(datanode_list= DatanodeList())
      ## Round Robin implementation
      indexTable = self.__indexTable.getIndexTable()
      for i in range(0, chunks_number):    
        
        if filename in indexTable.keys() and i == 0:
          if operation_type == "Append":
            lastChunk = self.__indexTable[filename][-1]
            yield CreateRsp(datanode_list=DatanodeList(localization=lastChunk.location))
            continue
          elif operation_type == "Create":
            yield CreateRsp(warning_message = WarningMessage( message= "File already stored in DFS system. If you are certain it is a new file, please rename it. Otherwise, if you want to add new information to an existing file, please store it in a separate file and upload it using the 'Append' method."))
          

        index= self.__globalCount%len(availableDatanodes)
        datanode:Datanode=availableDatanodes[index]
        location=datanode.location
        self.__globalCount+=1
        yield CreateRsp(datanode_list= DatanodeList(localization=location))
        
    
    except Exception as e:
        logger.error("Error while sending locations: {}".format(e))
        # Manejar cualquier otro error que pueda ocurrir durante la lectura del archivo
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details("Error while sending locations")
        yield CreateRsp(datanode_list= DatanodeList())
        return

  def open(self, request, context):
    try:    
        filename= request.filename
        chunk_list= self.__indexTable.get_all_chunk_data_from_name(filename=filename)
        if len(chunk_list) == 0:
          yield CreateRsp( datanode_list= DatanodeList())
        else:
          for chunk in chunk_list:
            localizations_available:DatanodeListStructure=chunk.locations.get_alive_datanodes()
            print(localizations_available)
            random_index = random.randint(0, len(localizations_available)-1)
            datanode:Datanode=localizations_available[random_index]
            location=datanode.location
            name= chunk.name
            return DatanodeList(localization=location,chunkname=name)
          
    except KeyError as e:
       # Archivo no existe, no encuentra la llave
       logger.error("Error filename doesn't exist {}".format(e))
       context.set_code(grpc.StatusCode.NOT_FOUND)
       context.set_details("Error filename doesn't exist")
       yield CreateRsp(datanode_list= DatanodeList())
       return
    except Exception as e:
        logger.error("Error while sending locations: {}".format(e))
        # Manejar cualquier otro error que pueda ocurrir durante la lectura del archivo
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details("Error while sending locations")
        yield CreateRsp(datanode_list = DatanodeList())
        return
  
  def heart_beat(self, request, context):
    datanodeId=request.id
    if datanodeId == "1":
      while True:
        datanodeId = str(uuid4())[:8]
        if datanodeId not in self.__used_ids:
          self.__used_ids[datanodeId] = 1
          break
    
    datanodeSocket= request.socket
    currentTime= time.time()
    dataNodeToSave= Datanode(uid=datanodeId,location=datanodeSocket,isLeader=None,last_heart_beat=currentTime)
    
    
    index= self.__cluster_assign_count%len(self.__cluster_list)
    cluster:Cluster=self.__cluster_list[index]
    is_leader=cluster.add_datanode(dataNodeToSave)
    self.__cluster_assign_count+=1
    dataNodeToSave.is_leader=is_leader
    self.__dataNodesList.add_datanode(dataNodeToSave)
    for cluster in self.__cluster_list:
      cluster.print()
    logger.info("ping done with {datanodeInfo}".format(datanodeInfo=datanodeSocket))
    cluster_id = cluster.get_id()
    return HeartBeatRsp(cluster_id=cluster_id, id_datanode=datanodeId, is_leader=dataNodeToSave.is_leader)
  
  def report(self, request, context):
    # Process the received ChunkReport
    file_id = request.filename
    chunk_name = request.partname
    datanode_id = request.location
    # Update the index table with the chunk information
    #add entry to index table
    if file_id!="" and chunk_name!="":
      logger.info("Report arrived from {sender} datanode for {chunk} chunk from {file} file".format(sender=datanode_id,chunk=chunk_name,file=file_id))
      self.__indexTable.add_entry_index_table(filename=file_id,part_name=chunk_name,datanode_id=datanode_id)
    else:
      logger.info("Empty report arrived from {sender} datanode".format(sender=datanode_id))
    #self.__indexTable.print_indexTable()
    return Empty()
  
  def listin(self, request, context):
    logger.info("Received req from client for updated index list")
    print(self.__indexTable)
    if len(self.__indexTable.items())<1:
      yield DirectoryContent()
    for key, value in self.__indexTable.items():
      print(key)
      yield DirectoryContent(name=key) 
    return 
  
  
class NameNodeServer():
  _ONE_DAY_IN_SECONDS = 60 * 60 * 24
  def __init__(self, ip_address, port, max_workers):
    self.__ip_address = ip_address
    self.__port = port
    self.__max_workers = max_workers
    self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers))
    self.__datanodesList= DatanodeListStructure()
    self.__indexTable= IndexTable(logger, self.__datanodesList)
    servicer.add_NameNodeServiceServicer_to_server(FileServicer(self.__datanodesList,self.__indexTable),self.__server)
    self.__server.add_insecure_port(str(self.__ip_address) + ":" + str(self.__port))
    logger.info("created namenode instance " + str(self))

  def __str__(self):
    return "ip:{ip_address},\
      port:{port},\
      max_workers:{max_workers}"\
      .format(
        ip_address=self.__ip_address,
        port=self.__port,
        max_workers=self.__max_workers)

  def start(self):
    logger.info("starting instance " + str(self))
    self.__server.start()
    try:
      while True:
        time.sleep(NameNodeServer._ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
      self.__server.stop(0)

  

