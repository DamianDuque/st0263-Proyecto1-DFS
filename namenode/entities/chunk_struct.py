from .datanode_list import DatanodeListStructure
class Chunk:
  def __init__(self, name:str):
    self.name = name
    self.locations = []
  def add_location(self,datanode_id: str):
    self.locations.append(datanode_id)