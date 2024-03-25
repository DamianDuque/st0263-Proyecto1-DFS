import logging
import os
import time
from . import splitter

import grpc

from protos.file_pb2 import ReadFileReq,WriteFileReq,FileOpenReq,FileCreateReq
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
  def __init__(self, ip_address, port, cert_file,root_dir):
    self.__ip_address = ip_address
    self.__port = port
    self.__cert_file = cert_file
    self.__files_directory=root_dir
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
         self.read(localization,file_name=file_name,chunk_name=chunkname)
         
     except grpc.RpcError as e:
        logger.error("gRPC error: {}".format(e.details()))
    
    

  def read(self,socket,file_name,chunk_name):
    datanodeStub= self._create_datanode_client(socket=socket)
    logger.info("downloading chunk {chunk} from file:{file_name} in socket: {socket}".format(file_name=file_name,chunk=chunk_name,socket=socket))
    req= ReadFileReq(filename=file_name,chunkname=chunk_name)
   
    try:
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
    namenodeStub= self._create_name_node_client(self.__ip_address,self.__port)
    splitter.hadoop_style_split(file_name, 1024 * 1024)
    directory=os.path.join(self.__files_directory,file_name)
    print(os.listdir(directory))
    chunksList= os.listdir(directory)
    chunksNumber=len(chunksList)
    try:
      req= FileCreateReq(filename=file_name,chunks_number=chunksNumber)
      response_stream = namenodeStub.create(req)
      chunkIndex=0
      for response in response_stream:
         localization="{}".format(response.localization)
         chunkName=chunksList[chunkIndex]
         self.__uploadToServer(socket=localization,filename=file_name,chunk_name=chunkName)
         chunkIndex+=1
    except grpc.RpcError as e:
      logger.error("gRPC error: {}".format(e.details()))    
    except Exception as e:
      logger.error("internal error: {}".format(e))




  def __uploadToServer(self,socket,filename,chunk_name):
    filePath=os.path.join(self.__files_directory,filename,chunk_name)

    try:
      with open(filePath, "rb") as fh:
        piece = fh.read(self._PIECE_SIZE_IN_BYTES)
        if not piece:
          raise EOFError
        req= WriteFileReq(filename=filename,chunkname=chunk_name,buffer=piece)
        datanodeStub= self._create_datanode_client(socket=socket)
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
    return "ip:{ip_address}, port:{port}, cert_file:{cert_file}"\
      .format(
        ip_address=self.__ip_address,
        port=self.__port,
        cert_file=self.__cert_file)
