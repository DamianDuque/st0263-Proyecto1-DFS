from .datanode_list import DatanodeListStructure
class Chunk:
  def __init__(self, name:str,datanodesInSystem:DatanodeListStructure):
    self.name = name
    self.locations = DatanodeListStructure()
    self.datanodesInSystem=datanodesInSystem
  def add_location(self,datanode_id: str):
    datanodeInfo= self.datanodesInSystem.get_datanode(datanode_id)
    self.locations.add_datanode(datanodeInfo)