from concurrent import futures
import logging
import os
import time

import grpc

from protos.file_pb2 import FileDownloadRsp, UploadRsp, FileListRsp
from protos import file_pb2_grpc as file_pb2_grpc

logger = logging.getLogger(__name__)

class FileServicer(file_pb2_grpc.FileServicer):
  _PIECE_SIZE_IN_BYTES = 1024 * 1024 # 1MB

  def __init__(self, files_directory):
    self.__files_directory = files_directory

  def listAll(self, request, context):
    logger.info("sending files list")
    files = []
    for root, dirs, filenames in os.walk(self.__files_directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(file_path, self.__files_directory)
            file_size = os.path.getsize(file_path)
            files.append((relative_path, file_size))

    if not files:
        yield FileListRsp()
    else:
        for file_info in files:
            yield FileListRsp(filename=file_info[0], size=file_info[1])
    
  def listChunksFromFile(self, request, context):
    filename= request.filename
    logger.info("sending partitions list from file {filename}".format(filename=filename))
    path=os.path.join(self.__files_directory, filename)
    print(path)
    files = [(f, os.path.getsize(path+ "/" + f))
      for f
      in os.listdir(path)
      if os.path.isfile(path + "/" + f)]

    if len(files) == 0:
      yield FileListRsp()
    else:
      for file in files:
        yield FileListRsp(filename=file[0], size=file[1])

  def download(self, request, context):
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
        return FileDownloadRsp(buffer=piece)    
    except FileExistsError:
      error_detail = "File: " + file_name+"/"+file_partition_name + " not exists"
      logger.error(error_detail)
      context.set_details(error_detail)
      context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
      return FileDownloadRsp()
    except Exception as e:
        logger.error("Error while reading file: {}".format(e))
        # Manejar cualquier otro error que pueda ocurrir durante la lectura del archivo
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details("Error while reading file or empty file")
        return FileDownloadRsp(buffer="")
    #Inserta las particiones de un archivo en el servidor
  def upload(self, request, context):
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
          return UploadRsp()
        except Exception as e:
          logger.error("Error while reading or receiving file: {}".format(e))
          # Manejar cualquier otro error que pueda ocurrir durante la lectura del archivo
          context.set_code(grpc.StatusCode.INTERNAL)
          context.set_details("Error while reading file or receiving file")
          return UploadRsp()
  


class FileServer():
  _ONE_DAY_IN_SECONDS = 60 * 60 * 24

  def __init__(self, ip_address, port, max_workers, files_directory, private_key_file, cert_file):
    self.__ip_address = ip_address
    self.__port = port
    self.__max_workers = max_workers
    self.__files_directory = files_directory
    self.__private_key_file = private_key_file
    self.__cert_file = cert_file
    # with open(self.__private_key_file, "rb") as fh:
    #   private_key = fh.read()
    # with open(self.__cert_file, "rb") as fh:
    #   certificate_chain = fh.read()

    self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    file_pb2_grpc.add_FileServicer_to_server(FileServicer(self.__files_directory), self.__server)
    self.__server.add_insecure_port(str(self.__ip_address) + ":" + str(self.__port))
    logger.info("created instance " + str(self))


  def __str__(self):
    return "ip:{ip_address},\
      port:{port},\
      max_workers:{max_workers},\
      files_directory:{files_directory},\
      private_key_file:{private_key_file},\
      cert_file:{cert_file}"\
      .format(
        ip_address=self.__ip_address,
        port=self.__port,
        max_workers=self.__max_workers,
        files_directory=self.__files_directory,
        private_key_file=self.__private_key_file,
        cert_file=self.__cert_file)

  def start(self):
    logger.info("starting instance " + str(self))
    self.__server.start()
    try:
      while True:
        time.sleep(FileServer._ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
      self.__server.stop(0)
