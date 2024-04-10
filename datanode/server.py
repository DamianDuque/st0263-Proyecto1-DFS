from concurrent import futures

import logging
import os
import time

import grpc
import sys
from reports import Reports
from replication import Replication

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


# Import statements for protobuf files
from protos.file_pb2 import WriteRsp,ReadFileRsp
from protos.file_pb2_grpc import  FileServicer, add_FileServicer_to_server



logger = logging.getLogger("datanode")

class FileServicer(FileServicer):
  _PIECE_SIZE_IN_BYTES = 1024 * 1024 * 128# 1MB
  
  def __init__(self, files_directory, reports, namenode_ip, namenode_port, datanode_id, datanode_cluster, is_leader):
    self.__files_directory = files_directory
    self.__reportclass = reports
    self.__namenode_ip = namenode_ip
    self.__namenode_port = namenode_port
    self.__datanode_id = datanode_id
    self.__datanode_cluster = datanode_cluster
    self.__is_leader = is_leader

  
  def read(self, request, context):
    file_name = request.filename
    file_partition_name= request.chunkname
    print(file_partition_name)
    #main directory/filename/partition_number.extension
    dir_path=self.__files_directory + "/"+file_name+"/"+file_partition_name
    try:
      #Archivo no existe o no es un archivo regular, levanta un err.
      if not os.path.isfile(dir_path):
        print(dir_path)
        raise FileExistsError
      #Archivo vacio, Error End of file.
      if os.path.getsize(dir_path) == 0:
        raise EOFError
      logger.info("sending partition: {partition} of original file {filename}".format(partition=file_partition_name,filename=file_name))
      with open(dir_path, "rb") as fh:
        piece = fh.read(FileServicer._PIECE_SIZE_IN_BYTES)
        if not piece:
          raise EOFError
        return ReadFileRsp(buffer=piece)    
    except FileExistsError:
      error_detail = "File: " + file_name+"/"+file_partition_name + " not exists"
      logger.error(error_detail)
      context.set_details(error_detail)
      context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
      return ReadFileRsp()
    except Exception as e:
        logger.error("Error while reading file: {}".format(e))
        # Manejar cualquier otro error que pueda ocurrir durante la lectura del archivo
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details("Error while reading file or empty file")
        return ReadFileRsp(buffer="")
    #Inserta las particiones de un archivo en el servidor
  def write(self, request, context):
        file_name = request.filename
        file_partition_name= request.chunkname
        file_partition=request.buffer
        try:
          #si no existe directorio, lo crea.
          directory=os.path.join(self.__files_directory, file_name)
          if not os.path.exists(directory):
            os.mkdir(directory)
          #recibe chunk en bytes con su respectivo nombre
          file_to_write= os.path.join(directory,file_partition_name)
          logger.info("receiving {partition} partition from file: {file_name}".format(file_name=file_name,partition=file_partition_name))
          with open(file_to_write, "wb") as fh:
            fh.write(file_partition)

          logger.info("trying to report {partition} partition from file: {file_name}".format(file_name=file_name,partition=file_partition_name))
          self.__reportclass.report_partition(file_name, file_partition_name)
          logger.info("Succesfully reported {partition} partition from file: {file_name}".format(file_name=file_name,partition=file_partition_name))
          
          if self.__is_leader:
            replicate = Replication(nameNodeIP=self.__namenode_ip, nameNodePort=self.__namenode_port)
            replicate.followers(self.__datanode_id, self.__datanode_cluster,directory,file_name,file_partition_name)
          
          return WriteRsp()
        except Exception as e:
          logger.error("Error while reading or receiving file: {}".format(e))
          # Manejar cualquier otro error que pueda ocurrir durante la lectura del archivo
          context.set_code(grpc.StatusCode.INTERNAL)
          context.set_details("Error while reading file or receiving file")
          return WriteRsp()
  
 

class DatanodeServer():
  _ONE_DAY_IN_SECONDS = 60 * 60 * 24

  def __init__(self, ip_address, port, max_workers, files_directory, reports, namenode_ip, namenode_port, datanode_id, datanode_cluster, is_leader,private_address):
        
    self.__ip_address = ip_address
    self.__port = port
    self.__max_workers = max_workers
    self.__files_directory = files_directory
    self.__reportc = reports
    self.__namenode_ip = namenode_ip
    self.__namenode_port =  namenode_port
    self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=20), options=[('grpc.max_receive_message_length', 134217758),('grpc.max_send_message_length', 134217758)])
    self.__datanode_id = datanode_id
    self.__datanode_cluster = datanode_cluster
    self.__is_leader = is_leader
    self.__private_address= private_address
    add_FileServicer_to_server(FileServicer(self.__files_directory, self.__reportc,self.__namenode_ip, self.__namenode_port, self.__datanode_id, self.__datanode_cluster, self.__is_leader), self.__server)
    self.__server.add_insecure_port(str(self.__private_address) + ":" + str(self.__port))
    logger.info("created datanode instance " + str(self))
   
  def __str__(self):
    return "ip:{ip_address},port:{port},max_workers:{max_workers},files_directory:{files_directory}".format(ip_address=self.__ip_address,port=self.__port,max_workers=self.__max_workers,files_directory=self.__files_directory)

  def start(self):
    logger.info("starting instance " + str(self))
    self.__server.start()
    try:
      while True:
        time.sleep(DatanodeServer._ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
      self.__server.stop(0)

