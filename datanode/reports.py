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
  def __init__(self,datanodeIP,datanodePort,nameNodeIP,nameNodePort):
        self.__my_ip = datanodeIP
        self.__my_port=datanodePort
        self.__namenode_ip=nameNodeIP
        self.__namenode_port=nameNodePort

  def _create_name_node_client(self,host:int ,port:int):
        socket="{}:{}".format(host,port)
        channel: grpc.Channel = grpc.insecure_channel(socket)
        return  NameNodeServiceStub(channel)

  def report_partition(self, file_name, file_partition_name):
        try:
            # Create a gRPC channel to connect to the Namenode
            namenode_stub = self._create_name_node_client(self.__namenode_ip, self.__namenode_port)
            # Create a ChunkReport message
            datanode_id = str(self.__my_ip)+":"+str(self.__my_port)
            report_tosend = ChunkReport(filename=file_name, partname=file_partition_name, location=datanode_id)
            # Send the ChunkReport to the Namenode
            namenode_stub.report(report_tosend)
        #except grpc.RpcError as e:
        #    logger.error("gRPC error: {}".format(e.details()))
        except Exception as e:
            logger.error("internal error: {}".format(e))