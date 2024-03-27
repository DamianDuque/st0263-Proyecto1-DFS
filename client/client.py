import logging
import os
import time
import json
from . import splitter

import grpc

from protos.file_pb2 import ReadFileReq,WriteFileReq,FileOpenReq,FileCreateReq,Empty
from protos.file_pb2_grpc import FileStub,NameNodeServiceStub

logger = logging.getLogger(__name__)

class Client:
  def _create_name_node_client(self,host: int,port:int):
         socket="{}:{}".format(host,port)
         channel: grpc.Channel = grpc.insecure_channel(socket)
         return  NameNodeServiceStub(channel)
    
  def _create_datanode_client(self,socket:str):
        channel: grpc.Channel = grpc.insecure_channel(socket)
        return  FileStub(channel)
  def __init__(self, ip_address, port,root_dir,in_dir):
    self.__ip_address = ip_address
    self.__port = port
    self.__files_directory=root_dir
    self.__in_dir=in_dir
    self._PIECE_SIZE_IN_BYTES = 1024 * 1024 # 1MB
    logger.info("created instance " + str(self))

  def list(self):
    return
  def open(self,file_name):
     namenodeStub= self._create_name_node_client(self.__ip_address,self.__port)
     logger.info("calling namenodeserver...")
     req= FileOpenReq(filename=file_name)
     try:
      response_stream = namenodeStub.open(req)
      for response in response_stream:
         localization="{}".format(response.localization)
         chunkname="{}".format(response.chunkname)
         self.read(socket=localization,file_name=file_name,chunk_name=chunkname)
         
     except grpc.RpcError as e:
        logger.error("gRPC error: {}".format(e.details()))
        return
    
  def read(self,socket,file_name,chunk_name):
    
    try:
      datanodeStub= self._create_datanode_client(socket=socket)
      logger.info("downloading chunk {chunk} from file:{file_name} in socket: {socket}".format(file_name=file_name,chunk=chunk_name,socket=socket))
      req= ReadFileReq(filename=file_name,chunkname=chunk_name)
      #Remote Call procedure to datanode download
      response_bytes = datanodeStub.read(req)
      self.__saving_chunk(response_bytes, chunk_name, file_name)
    except grpc.RpcError as e:
        logger.error("gRPC error: {}".format(e.details()))
    

  def __saving_chunk(self, response_bytes, out_file_name, out_file_dir):
    try:
      #Si directorio no existe, lo crea para guardar las particiones del archivo.
      directory=os.path.join(self.__files_directory, out_file_dir)
      if not os.path.exists(directory):
        os.mkdir(directory)
      with open(directory+"/"+out_file_name, "wb") as fh:
        fh.write(response_bytes.buffer)
    except Exception as e:
        print("An error occurred while saving the chunk: {}".format(e))
        logger.error("Error while saving chunk: {}".format(e))
      
  
  def create(self,file_name):
    
    try:
      namenodeStub= self._create_name_node_client(self.__ip_address,self.__port)
      splitter.hadoop_style_split(filename=file_name,in_path=self.__in_dir,out_path=self.__files_directory, chunk_size= self._PIECE_SIZE_IN_BYTES)
      directory=os.path.join(self.__files_directory,file_name)
      chunksList= os.listdir(directory)
      chunksNumber=len(chunksList)
      req= FileCreateReq(filename=file_name,chunks_number=chunksNumber)
      response_stream = namenodeStub.create(req)
      chunkIndex=0
      for response in response_stream:
         localization="{}".format(response.localization)
         chunkName=chunksList[chunkIndex]
         self.__uploadToNameNode(socket=localization,filename=file_name,chunk_name=chunkName)
         chunkIndex+=1
    except grpc.RpcError as e:
      logger.error("gRPC error: {}".format(e.details()))    
    except Exception as e:
      logger.error("internal error: {}".format(e))
  
  def list_index(self):
    try:
      namenodeStub= self._create_name_node_client(self.__ip_address,self.__port)
      req= Empty()
      response_stream = namenodeStub.listin(req)
      tablestr = response_stream.table
      tablestr2 = str(tablestr)
      tabledic = json.loads(tablestr2)
      logger.info("Updated index table: {table}".format(table=tablestr))
    except grpc.RpcError as e:
      logger.error("gRPC error: {}".format(e.details()))    
    except Exception as e:
      logger.error("internal error: {}".format(e))




  def __uploadToNameNode(self,socket,filename,chunk_name):
    filePath=os.path.join(self.__files_directory,filename,chunk_name)
    try:
      with open(filePath, "rb") as fh:
        piece = fh.read(self._PIECE_SIZE_IN_BYTES)
        if not piece:
          raise EOFError
        req= WriteFileReq(filename=filename,chunkname=chunk_name,buffer=piece)
        datanodeStub= self._create_datanode_client(socket=socket)
        logger.info("Trying creating file on datanode- {location}".format(location=socket))
        datanodeStub.write(req)
        logger.info("creating file ok: chunk:{chunkname} datanode- {location}".format(chunkname=chunk_name,location=socket))
    except grpc.RpcError as e:
        logger.error("gRPC error: {}".format(e.details()))    
    except Exception as e:
      logger.error("internal error: {}".format(e))
    

  def __list_files(self, response_stream):
    for response in response_stream:
      print("file name: {}, size: {} bytes".format(response.filename, response.size))

  def __str__(self):
    return "ip:{ip_address}, port:{port}"\
      .format(
        ip_address=self.__ip_address,
        port=self.__port
        )
