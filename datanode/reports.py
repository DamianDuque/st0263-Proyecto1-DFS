import time
import logging
import grpc
import os
import sys

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from protos.file_pb2 import ChunkReport
from protos.file_pb2_grpc import  NameNodeServiceStub


logger = logging.getLogger("datanode-client")

class Reports:
      def __init__(self, datanodeId, nameNodeIP, nameNodePort):
        self.__my_id = datanodeId
        self.__namenode_ip=nameNodeIP
        self.__namenode_port=nameNodePort
      def _create_name_node_client(self, host:int ,port:int):
        socket="{}:{}".format(host, port)
        channel: grpc.Channel = grpc.insecure_channel(socket)
        return  NameNodeServiceStub(channel)
      def report_partition(self, file_name, file_partition_name):
        try:
            # Create a gRPC channel to connect to the Namenode
            namenode_stub = self._create_name_node_client(self.__namenode_ip, self.__namenode_port)
            # Create a ChunkReport message
            datanode_id = str(self.__my_id)
            report_tosend = ChunkReport(filename=file_name, partname=file_partition_name, location=datanode_id)
            # Send the ChunkReport to the Namenode
            namenode_stub.report(report_tosend)
        #except grpc.RpcError as e:
        #    logger.error("gRPC error: {}".format(e.details()))
        except Exception as e:
            logger.error("internal error: {}".format(e))
      def initial_report(self,directory):
            #print(self.__namenode_ip)
            namenode_stub = self._create_name_node_client(self.__namenode_ip, self.__namenode_port)
            logger.info("Initial Report displaying")
            current_dir = []
            datanode_id = str(self.__my_id)
            for directorio, subdirectorios, archivos in os.walk(directory):
                  file= os.path.basename(directorio)
                  #print(directorio,directory)
                  if str(directorio) == directory:
                        continue
                  for archivo in archivos:
                        current_dir.append((file,archivo,datanode_id))
                  
            if  len(current_dir)<1:
                  report_tosend=ChunkReport(location=datanode_id)
                  namenode_stub.report(report_tosend)
            else:
                  report_tosend=ChunkReport()
                  for file_info in current_dir:
                        filename,partname,location=file_info
                        report_tosend=ChunkReport(filename=filename, partname=partname, location=location)
                        namenode_stub.report(report_tosend)
                  logger.info("updated index table with current dir values")