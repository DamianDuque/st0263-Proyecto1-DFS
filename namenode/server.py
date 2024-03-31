from concurrent import futures
import logging
import os
import time
import json

import grpc

import sys
#probando
# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from protos import file_pb2_grpc as servicer
from protos.file_pb2 import DatanodeList,Empty,DirectoryContent

logger = logging.getLogger(__name__)


class FileServicer(servicer.NameNodeServiceServicer):
  def __init__(self,dataNodesList,indexTable):
    self.__dataNodesList=dataNodesList
    self.__indexTable=indexTable
    self.__globalCount=0

  def create(self, request, context):
    filename= request.filename
    chunks_number= request.chunks_number

    availableDatanodes = []
    for key, value in self.__dataNodesList.items():
      if value == True:
        availableDatanodes.append(key)
    try:
      if len(availableDatanodes)==0:
        yield DatanodeList()

      ## Round Robin implementation

      for i in range(0, chunks_number):
        index= self.__globalCount%len(availableDatanodes)
        location=availableDatanodes[index]
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
  
  def ping(self, request, context):
    datanodeSocket= request.socket
    self.__dataNodesList[datanodeSocket]=True
    print(self.__dataNodesList[datanodeSocket])
    logger.info("ping done with {datanodeInfo}".format(datanodeInfo=datanodeSocket))
    return Empty()
  
  def report(self, request, context):
    # Process the received ChunkReport
    file_id = request.filename
    chunk_id = request.partname
    datanode_id = request.location
    # Update the index table with the chunk information
    logger.info("Report arrived from {sender} datanode for {chunk} chunk from {file} file".format(sender=datanode_id,chunk=file_id,file=chunk_id))
    #self.__indexTable[file_id]=self.__indexTable[file_id].append(Chunk(chunk_id,datanode_id))
    if file_id not in self.__indexTable.keys():
     self.__indexTable[file_id] = [(chunk_id,datanode_id)]
     logger.info("Updated index table to {table}".format(table=self.__indexTable))
    else:
     self.__indexTable[file_id].append((chunk_id,datanode_id))
     logger.info("Updated index table to {table}".format(table=self.__indexTable))
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
    self.__indexTable= {}
    self.__datanodesList={}
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

class Chunk:
  def __init__(self, name, location):
    self.name = name
    self.location = location