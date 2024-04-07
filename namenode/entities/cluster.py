from .datanode_list import Datanode, DatanodeListStructure
from colorama import Fore, Style

class Cluster:
    def __init__(self, id):
        self.cluster_id = id
        self.datanodeList = DatanodeListStructure()
        self.leader_id:str= ""
        
    def add_datanode(self,datanode:Datanode)->bool:
        is_leader=False
        if len(self.datanodeList.datanodes)==0:
            self.leader_id=datanode.uid
            is_leader=True
        self.datanodeList.add_datanode(datanode)
        return is_leader

    def get_id(self):
        return self.cluster_id

    def print(self):
        print(Fore.RED)
        print(self.leader_id)
        print(Style.RESET_ALL)
        print(" ")
        self.datanodeList.print_list()