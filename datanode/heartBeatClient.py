from protos.file_pb2_grpc import NameNodeServiceStub
from protos.file_pb2 import DatanodeInfo
import time
import logging
import os
import grpc
from dotenv import load_dotenv
load_dotenv("datanode/.env")
logger = logging.getLogger("datanode-client")
class Client:
    def __init__(self, datanodeId,cluster_id, datanodeIP, datanodePort, nameNodeIP, nameNodePort, ttl):
        self.__my_id = datanodeId
        self.__my_cluster=cluster_id
        self.__my_ip = datanodeIP
        self.__my_port=datanodePort
        self.__namenode_ip=nameNodeIP
        self.__namenode_port=nameNodePort
        self.__ttl=ttl

    def _create_name_node_client(self, host:int, port:int):
        socket="{}:{}".format(host, port)
        channel: grpc.Channel = grpc.insecure_channel(socket)
        return  NameNodeServiceStub(channel)
    
    def updateenv(self, datanode_id,cluster_id):
        datanode_id_variable = 'DATANODE_ID'
        datanode_id_value = datanode_id
        cluster_id_variable = 'CLUSTER_ID'
        cluster_id_value = cluster_id

        # Read the contents of the .env file
        with open('datanode/.env', 'r') as f:
            lines = f.readlines()

        # Update the line with the new value
        for i, line in enumerate(lines):
            if line.startswith(datanode_id_variable):
                lines[i] = f'{datanode_id_variable}={datanode_id_value}\n'
                continue
            elif line.startswith(cluster_id_variable):
                lines[i] = f'{cluster_id_variable}={cluster_id_value}\n'
                break

        # Write the updated contents back to the .env file
        with open('datanode/.env', 'w') as f:
            f.writelines(lines)

        
    def ping(self, n):
        datanodeSocket= "{}:{}".format(self.__my_ip, self.__my_port)
        namenodeStub= self._create_name_node_client(self.__namenode_ip,self.__namenode_port)
        if self.__my_cluster=="":
            cluster_id=-1
        else:
            cluster_id=int(self.__my_cluster)
        req= DatanodeInfo(id=self.__my_id, socket=datanodeSocket,cluster=cluster_id)
        print(self.__my_id)
        try:
            while True:
                ping_resp = namenodeStub.heart_beat(req)
                cluster_id, datanode_id, is_leader  = ping_resp.cluster_id,ping_resp.id_datanode,ping_resp.is_leader
                logger.info("ping done, info received: cluster_id: {cluster}, datanode_id: {datanode}, is leader: {leader}".format(cluster = cluster_id, datanode = datanode_id, leader = is_leader))
                req= DatanodeInfo(id=self.__my_id, socket=datanodeSocket, cluster=cluster_id)
                self.updateenv(datanode_id,cluster_id)
                if n == 1:
                    return datanode_id,cluster_id
                time.sleep(self.__ttl)
        except grpc.RpcError as e:
            logger.error("gRPC error: {}".format(e.details()))
        


