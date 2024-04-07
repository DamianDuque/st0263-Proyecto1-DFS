from protos.file_pb2_grpc import NameNodeServiceStub
from protos.file_pb2 import DatanodeInfo
import time
import logging
import grpc
from dotenv import load_dotenv
logger = logging.getLogger("datanode-client")
load_dotenv("datanode/.env")

class Client:
    def __init__(self, datanodeId, datanodeIP, datanodePort, nameNodeIP, nameNodePort, ttl):
        self.__my_id = datanodeId
        self.__my_ip = datanodeIP
        self.__my_port=datanodePort
        self.__namenode_ip=nameNodeIP
        self.__namenode_port=nameNodePort
        self.__ttl=ttl

    def _create_name_node_client(self, host:int, port:int):
        socket="{}:{}".format(host, port)
        channel: grpc.Channel = grpc.insecure_channel(socket)
        return  NameNodeServiceStub(channel)
        
    def ping(self):
        datanodeSocket= "{}:{}".format(self.__my_ip, self.__my_port)
        print(datanodeSocket)
        namenodeStub= self._create_name_node_client(self.__namenode_ip,self.__namenode_port)
        req= DatanodeInfo(id=self.__my_id, socket=datanodeSocket, is_leader=True)
        try:
            while True:
                namenodeStub.heart_beat(req)
                logger.info("ping done")
                time.sleep(self.__ttl)
        except grpc.RpcError as e:
            logger.error("gRPC error: {}".format(e.details()))
        


