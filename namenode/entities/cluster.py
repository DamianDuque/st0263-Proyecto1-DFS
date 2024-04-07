from .datanode_list import Datanode,DatanodeListStructure

class Cluster:
    def __init__(self, id,datanodesInSystem:DatanodeListStructure):
        self.cluster_id = id
        self.datanodeListInSystem = datanodesInSystem
        self.datanode_ids_List=[]
        self.leader_id:str= ""
        
    def add_datanode(self,datanode:Datanode)->bool:
        is_leader=False
        if datanode.uid not in self.datanode_ids_List:
            if len(self.datanode_ids_List)==0 or self.datanodeListInSystem.get_datanode(self.leader_id).is_alive==False:
                print(datanode.uid)
                self.leader_id=datanode.uid
                is_leader=True
            self.datanode_ids_List.append(datanode.uid)
        else:
            if datanode.uid==self.leader_id or self.datanodeListInSystem.get_datanode(self.leader_id).is_alive==False:
                is_leader=True
        return is_leader

    def get_id(self):
        return self.cluster_id

    def print(self):
        print("ID: ",self.cluster_id)
        print("leader",self.leader_id)
        print("Datanodes: ")
        for datanode in self.datanode_ids_List:
            print("- ",datanode)