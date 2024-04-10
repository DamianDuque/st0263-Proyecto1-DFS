import time
import logging
logger = logging.getLogger(__name__)

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
        self.is_alive = time_difference <= 6
        is_leader = self.get_is_leader()
        logger.info("Is leader: {leader}".format(leader = is_leader))
        if not self.is_alive:
            logger.info("Datanode: {uid} -- Murio".format(uid = self.uid))
        else:
            logger.info("Datanode: {uid} -- Vive".format(uid = self.uid))
        return is_leader and not self.is_alive

    def get_is_leader(self):
        return self.is_leader

    def print_datanode(self):
        logger.info("id: {uid},location{location}, is alive? {is_alive}".format(uid = self.uid, location = self.location, is_alive = self.is_alive))
    
class DatanodeListStructure:
    def __init__(self):
        self.datanodes = {}

    def set_is_leader(self, uid: str, is_leader: bool):
        self.datanodes[uid].is_leader = is_leader

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