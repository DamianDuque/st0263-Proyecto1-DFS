import time
import logging
import grpc
import os
import sys

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from protos.file_pb2 import LeaderFollowersReq, follower_info, WriteFileReq
from protos.file_pb2_grpc import  NameNodeServiceStub, FileStub


logger = logging.getLogger("datanode-client")

class Replication:
      def __init__(self, datanodeId, cluster, datanodeIP, datanodePort, nameNodeIP, nameNodePort):
        self.__my_id = datanodeId
        self.__my_cluster=cluster
        self.__my_ip = datanodeIP
        self.__my_port=datanodePort
        self.__namenode_ip=nameNodeIP
        self.__namenode_port=nameNodePort
   
      def _create_name_node_client(self,host: int,port:int):
            socket="{}:{}".format(host,port)
            channel: grpc.Channel = grpc.insecure_channel(socket)
            return  NameNodeServiceStub(channel)

      def __uploadToNameNode(self,socket,filename,chunk_name):   
      
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


      def followers(self,leader_id, cluster_id,file_name, chunk_name):
    
            try:
                  namenodeStub= self._create_name_node_client(self.__ip_address,self.__port)## Revisar esta info
                  req = LeaderFollowersReq(leader_id=leader_id, cluster_id=cluster_id)
                  response_stream = namenodeStub.get_followers(req)
                  
                  for response in response_stream:
                        #Actualizar a esta version--
                        localization="{}".format(response.datanode_list.localization)
                        self.__uploadToNameNode(socket=localization,filename=file_name,chunk_name=chunk_name)

            except grpc.RpcError as e:
                  logger.error("gRPC error: {}".format(e.details()))    
            except Exception as e:
                  logger.error("internal error: {}".format(e))



      