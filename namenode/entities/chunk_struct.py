from .datanode_list import DatanodeListStructure
class Chunk:
  def __init__(self, name:str):
    self.name = name
    self.locations = []
  def add_location(self,datanode_id: str):
    if datanode_id not in self.locations:
      #print("ENTERED ADD LOCATION WITH THIS ID:", datanode_id)
      self.locations.append(datanode_id)