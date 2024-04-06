import time
class Datanode:
    def __init__(self,uid:str,location:str,isLeader:bool,last_heart_beat:int):
        self.uid = uid
        self.is_alive= False
        self.is_leader= isLeader   
        self.location=location
        self.last_heart_beat=last_heart_beat
    def set_alive(self):
        time_difference = time.time() - self.last_heart_beat
        self.is_alive = time_difference <= 80
    
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
