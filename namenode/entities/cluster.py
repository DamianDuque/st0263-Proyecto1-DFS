from .datanode_list import Datanode,DatanodeListStructure
import logging

logger = logging.getLogger(__name__)
class Cluster:
    def __init__(self, id,datanodesInSystem:DatanodeListStructure):
        self.cluster_id = id
        self.datanodeListInSystem = datanodesInSystem
        self.datanode_ids_List=[]
        self.leader_id:str= ""
        
    def add_datanode(self,datanode:Datanode)->bool:
        is_leader=False
        if datanode.uid not in self.datanode_ids_List:
            if len(self.datanode_ids_List)==0:
                self.leader_id=datanode.uid
                is_leader = True
            self.datanode_ids_List.append(datanode.uid)
        else:
            if datanode.uid==self.leader_id:
                is_leader=True
        return is_leader
    
    def choose_new_leader(self):
        logger.info("ID: {cluster_id} -- Leader: {leader_id}".format(cluster_id=self.cluster_id,leader_id=self.leader_id))
        candidates = [candidate for candidate in self.datanodeListInSystem.get_alive_datanodes() if candidate.uid in self.datanode_ids_List]
        #print(f'Len Candi -- {len(candidates)}')
        if len(candidates) != 0:
            self.leader_id = candidates[0].uid
            logger.info("ID: {cluster_id} -- Leader CAMBIO: {leader_id}".format(cluster_id=self.cluster_id,leader_id=self.leader_id))
            self.datanodeListInSystem.set_is_leader(candidates[0].uid, True)
            


    def get_id(self):
        return self.cluster_id

    def print(self):
        '''print("ID: ",self.cluster_id)
        print("leader",self.leader_id)
        print("Datanodes: ")
        for datanode in self.datanode_ids_List:
            print("- ",datanode)'''
        pass