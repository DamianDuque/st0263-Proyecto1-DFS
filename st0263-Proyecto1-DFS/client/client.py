import logging
import os
import time
import json
from . import splitter
from . import unificator

import grpc

from protos.file_pb2 import ReadFileReq,WriteFileReq,FileOpenReq,FileCreateReq,Empty
from protos.file_pb2_grpc import FileStub,NameNodeServiceStub

logger = logging.getLogger(__name__)

class Client:
  def _create_name_node_client(self,host: int,port:int):
         socket="{}:{}".format(host,port)
         channel: grpc.Channel = grpc.insecure_channel(socket, options=[('grpc.max_receive_message_length', 134217758),('grpc.max_send_message_length', 134217758)])
         return  NameNodeServiceStub(channel)
    
  def _create_datanode_client(self,socket:str):
        channel: grpc.Channel = grpc.insecure_channel(socket, options=[('grpc.max_receive_message_length', 134217758),('grpc.max_send_message_length', 134217758)])
        return  FileStub(channel)
  
  def __init__(self, ip_address, port,root_dir,in_dir):
    self.__ip_address = ip_address
    self.__port = port
    self.__files_directory=root_dir
    self.__in_dir=in_dir
    self._PIECE_SIZE_IN_BYTES = 1024 * 1024 * 128 # 128 MB

  def open(self,file_name):
     namenodeStub= self._create_name_node_client(self.__ip_address,self.__port)
     logger.info("calling namenodeserver...")
     req= FileOpenReq(filename=file_name)
     try:
      response_stream = namenodeStub.open(req)
      for response in response_stream:
        print(response)
        localization=response.localization
        chunkname=response.chunkname
        self.read(socket=localization,file_name=file_name,chunk_name=chunkname)
      
      unificator.unificator(split_dir=self.__files_directory, filename = file_name)
         
     except grpc.RpcError as e:
        logger.error("gRPC error: {}".format(e.details()))
        return
    
  def read(self,socket,file_name,chunk_name):
    
    #try:
      datanodeStub= self._create_datanode_client(socket=socket)
      logger.info("downloading chunk {chunk} from file:{file_name} in socket: {socket}".format(file_name=file_name,chunk=chunk_name,socket=socket))
      req= ReadFileReq(filename=file_name,chunkname=chunk_name)
      #Remote Call procedure to datanode download
      response_bytes = datanodeStub.read(req)
      self.__saving_chunk(response_bytes, chunk_name, file_name)
      logger.info("succesfully downloaded file: {file_name} from socket: {socket}.".format(file_name=file_name,chunk=chunk_name,socket=socket))
    #except grpc.RpcError as e:
        #logger.error("gRPC error: {}".format(e.details()))
    

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
      req = FileCreateReq(filename=file_name,chunks_number=chunksNumber, operation="Create" )
      response_stream = namenodeStub.create(req)
      
      chunkIndex=0
      for response in response_stream:
         if response.HasField('warning_message'):
           raise Exception(response.warning_message.message)
         localization="{}".format(response.datanode_list.localization)
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
      for content in response_stream:
         print(f"- {content.name}")
    except grpc.RpcError as e:
     logger.error("gRPC error: {}".format(e.details()))    
    except Exception as e:
     logger.error("internal error: {}".format(e))


  def __uploadToNameNode(self,socket,filename,chunk_name, pathpart=None):
    if pathpart:
       filePath = pathpart
    else:
       filePath = os.path.join(self.__files_directory,filename,chunk_name)
    
    try:

      with open(filePath, "rb") as fh:
        piece = fh.read(self._PIECE_SIZE_IN_BYTES)
        if not piece:
          raise EOFError
        req= WriteFileReq(filename=filename,chunkname=chunk_name,buffer=piece)
        datanodeStub= self._create_datanode_client(socket=socket)
        logger.info("Trying to create file on datanode- {location}".format(location=socket))
        datanodeStub.write(req)
        logger.info("creating file ok: chunk:{chunkname} datanode- {location}".format(chunkname=chunk_name,location=socket))
    except grpc.RpcError as e:
        logger.error("gRPC error: {}".format(e.details()))    
    except Exception as e:
      logger.error("internal error: {}".format(e))


  def create_appends(self,file_name,appends_dir):
    
    try:
      namenodeStub= self._create_name_node_client(self.__ip_address,self.__port)
      chunksList= os.listdir(appends_dir)
      chunksNumber=len(chunksList)
      req= FileCreateReq(filename=file_name,chunks_number=chunksNumber, operation="Append")
      response_stream = namenodeStub.create(req)
      chunkIndex=0
      for response in response_stream:
         localization="{}".format(response.datanode_list.localization)
         chunkName=chunksList[chunkIndex]
         part_dir = os.path.join(appends_dir,chunkName)
         self.__uploadToNameNode(socket=localization,filename=file_name,chunk_name=chunkName, pathpart=part_dir)
         chunkIndex+=1
    except grpc.RpcError as e:
     logger.error("gRPC error: {}".format(e.details()))    
    except Exception as e:
     logger.error("internal error: {}".format(e))



  def append(self,file_name, file_name_dfs):
    namenodeStub= self._create_name_node_client(self.__ip_address,self.__port)
    logger.info("calling namenodeserver...")
    req= FileOpenReq(filename=file_name_dfs)
    try:
      response_stream = namenodeStub.open(req)
      for response in response_stream:
        localization="{}".format(response.localization)
        chunkname="{}".format(response.chunkname)
        last_response = (localization, chunkname)

      if last_response is not None:
      # Call the read function only once using information from the last response
        self.read(socket=last_response[0], file_name=file_name_dfs, chunk_name=last_response[1])

      donwloaded_chunk_path = self.__files_directory+"/"+file_name_dfs
      re_split_path = self.__files_directory+"/"+"re-split"
      
      splitter.hadoop_style_split(filename=chunkname,in_path=donwloaded_chunk_path,out_path=re_split_path, chunk_size= self._PIECE_SIZE_IN_BYTES, second_filename=file_name, second_in_path=self.__in_dir)
      directorio_destino = f"{re_split_path}/{file_name}"
      self.create_appends(file_name_dfs, directorio_destino)
               
    except grpc.RpcError as e:
      logger.error("gRPC error: {}".format(e.details()))
      return    
      