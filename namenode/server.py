from concurrent import futures
import logging
import os
import time

import grpc

import sys

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory of the current directory (i.e., the root directory of your project)
parent_dir = os.path.dirname(current_dir)
grand_dir = os.path.dirname(parent_dir)

# Add the parent directory to the Python path
sys.path.append(grand_dir)
print(grand_dir)

from protos import namenode_pb2_grpc as servicer
from protos.namenode_pb2 import DatanodeList

logger = logging.getLogger(__name__)

class FileServicer(servicer.NameNodeServiceServicer):
  def __init__(self,availableDatanode,indexTable):
    self.__availableDatanode=availableDatanode
    self.__indexTable=indexTable

  def create(self, request, context):
   """  filename= request.filename
    chunks_number= request.chunks_number
    try:

    except:
      print('An exception occurred') """
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
            yield DatanodeList(localization=localization)

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
class NameNodeServer():
  _ONE_DAY_IN_SECONDS = 60 * 60 * 24
  def __init__(self, ip_address, port, max_workers):
    self.__ip_address = ip_address
    self.__port = port
    self.__max_workers = max_workers
    self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    self.__indexTable= {"file1.txt":[Chunk("chunk1","localhost:8000"),Chunk("chunk2","localhost:8000")]}
    self.__availableDatanodes={"localhost:8000":true}
    servicer.add_NameNodeServiceServicer_to_server(FileServicer(self.__availableDatanodes,self.__indexTable),self.__server)
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