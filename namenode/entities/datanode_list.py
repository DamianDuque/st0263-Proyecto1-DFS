import time

class Datanode:
    def __init__(self,uid:str,cluster_id:int,location:str,isLeader:bool,last_heart_beat:time):
        self.uid = uid
        self.cluster_id = cluster_id
        self.is_alive= True
        self.is_leader= isLeader
        self.location=location
        self.last_heart_beat=last_heart_beat
        

    def set_alive(self):
        time_difference = time.time() - self.last_heart_beat
        self.is_alive = time_difference <= 80

    def get_is_leader(self):
        return self.is_leader()

    def print_datanode(self):
        print(f'id {self.uid},location{self.location}, is alive? {self.is_alive}')
    
class DatanodeListStructure:
    def __init__(self):
        self.datanodes = {}

    def add_datanode(self, datanode: Datanode):    
        self.datanodes[datanode.uid] = datanode

    def remove_datanode(self, uid: str)->Datanode:
        return self.datanodes.pop(uid, None)

    def get_datanode(self, uid: str)->Datanode:
        return self.datanodes.get(uid)

    def get_alive_datanodes(self)->list:
        return [datanode for datanode in self.datanodes.values() if datanode.is_alive]

    def get_leaders(self)->list:
        return [datanode for datanode in self.datanodes.values() if (datanode.is_alive and datanode.is_leader) ]
    
    def get_followers(self)->list:
        return [datanode for datanode in self.datanodes.values() if (datanode.is_alive and not datanode.is_leader) ]
    
    def print_list(self):
        for datanode in self.datanodes.values():
            datanode.print_datanode()