from protos.file_pb2_grpc import NameNodeServiceStub
from protos.file_pb2 import DatanodeInfo
import time
import logging
import grpc
logger = logging.getLogger("datanode-client")

class Client:
    def __init__(self,datanodeIP,datanodePort,nameNodeIP,nameNodePort):
        self.__my_ip = datanodeIP
        self.__my_port=datanodePort
        self.__namenode_ip=nameNodeIP
        self.__namenode_port=nameNodePort

    def _create_name_node_client(self,host:int ,port:int):
        socket="{}:{}".format(host,port)
        channel: grpc.Channel = grpc.insecure_channel(socket)
        return  NameNodeServiceStub(channel)
        
    def ping(self):
        datanodeSocket= "{}:{}".format(self.__my_ip,self.__my_port)
        print(datanodeSocket)
        namenodeStub= self._create_name_node_client(self.__namenode_ip,self.__namenode_port)
        req= DatanodeInfo(socket=datanodeSocket)
        try:
            while True:
                namenodeStub.ping(req)
                logger.info("ping done")
                time.sleep(60)
        except grpc.RpcError as e:
            logger.error("gRPC error: {}".format(e.details()))
        


