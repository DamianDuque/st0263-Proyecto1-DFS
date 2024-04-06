from .datanode_list import DatanodeListStructure
class Chunk:
  def __init__(self, name:str,datanodesList:DatanodeListStructure):
    self.name = name
    self.locations = DatanodeListStructure
    self.datanodesList=datanodesList
  def add_location(self,datanode_id: str):
    datanodeInfo= self.datanodesList.get_datanode(datanode_id)
    print(datanodeInfo)
    self.locations.add_datanode(datanodeInfo)