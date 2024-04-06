from concurrent import futures
import logging
import os
import time
import grpc
import sys
from entities.index_table import IndexTable
from entities.datanode_list import DatanodeListStructure,Datanode
#probando
# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from protos import file_pb2_grpc as servicer
from protos.file_pb2 import DatanodeList,Empty,DirectoryContent

logger = logging.getLogger(__name__)


class FileServicer(servicer.NameNodeServiceServicer):
  def __init__(self,dataNodesList:DatanodeListStructure,indexTable:IndexTable):
    self.__dataNodesList=dataNodesList
    self.__indexTable=indexTable
    self.__globalCount=0
    self.__dataNodeIdCounter=0

  def create(self, request, context):
    filename= request.filename
    chunks_number= request.chunks_number
    #Datanodes must be leaders
    availableDatanodes = self.__dataNodesList.get_leaders()
    
    try:
      if len(availableDatanodes)==0:
        yield DatanodeList()
      ## Round Robin implementation
      for i in range(0, chunks_number):
        """ if filename in self.__indexTable.keys() and i == 0:
          lastChunk = self.__indexTable[filename][-1]
          yield DatanodeList(localization=lastChunk.location)
          continue """
        
        index= self.__globalCount%len(availableDatanodes)
        datanode:Datanode=availableDatanodes[index]
        location=datanode.location
        self.__globalCount+=1
        yield DatanodeList(localization=location)
        
    
    except Exception as e:
        logger.error("Error while sending locations: {}".format(e))
        # Manejar cualquier otro error que pueda ocurrir durante la lectura del archivo
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details("Error while sending locations")
        yield DatanodeList()
        return

  def open(self, request, context):
    try:
        
        filename= request.filename
        list= self.__indexTable[filename]
        if len(list) == 0:
          yield DatanodeList()
        else:
          for chunk in list:
            localization=chunk.location
            name= chunk.name
            yield DatanodeList(localization=localization,chunkname=name)

    except KeyError as e:
       # Archivo no existe, no encuentra la llave
       logger.error("Error filename doesn't exist {}".format(e))
       context.set_code(grpc.StatusCode.NOT_FOUND)
       context.set_details("Error filename doesn't exist")
       yield DatanodeList()
       return
    except Exception as e:
        logger.error("Error while sending locations: {}".format(e))
        # Manejar cualquier otro error que pueda ocurrir durante la lectura del archivo
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details("Error while sending locations")
        yield DatanodeList()
        return
  
  def heart_beat(self, request, context):
    datanodeId=request.id
    datanodeSocket= request.socket
    datanodeIsLeader= request.is_leader
    currentTime= time.time()
    dataNodeToSave= Datanode(uid=datanodeId,location=datanodeSocket,isLeader=datanodeIsLeader,last_hearth_beat=currentTime)
    self.__dataNodesList.add_datanode(dataNodeToSave)
    logger.info("ping done with {datanodeInfo}".format(datanodeInfo=datanodeSocket))
    return Empty()
  
  def report(self, request, context):
    # Process the received ChunkReport
    file_id = request.filename
    chunk_id = request.partname
    datanode_id = request.location
    # Update the index table with the chunk information
    #add entry to index table
    if file_id!="" and chunk_id!="":
      logger.info("Report arrived from {sender} datanode for {chunk} chunk from {file} file".format(sender=datanode_id,chunk=chunk_id,file=file_id))
      self.__indexTable.add_entry_index_table(filename=file_id,part_info=chunk_id,datanode_id=datanode_id)
    else:
      logger.info("Empty report arrived from {sender} datanode".format(sender=datanode_id))

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
    self.__indexTable= IndexTable(logger)
    self.__datanodesList= DatanodeListStructure()
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




 




  

