import logging
from .datanode_list import DatanodeListStructure,Datanode
from .chunk_struct import Chunk

class IndexTable:
  def __init__(self, logger:logging.Logger, datanodeListInSystem:DatanodeListStructure):
    self.__indexTable={}
    self.datanodeListInSystem=datanodeListInSystem
    self.logger = logger


  def getIndexTable(self):
    return self.__indexTable

  def get_all_chunk_data_from_name(self, filename):
    return self.__indexTable[filename]
  
  def getChunkNames(self, filename):
    chunkNames = []
    for existingChunk in self.__indexTable[filename]:
      if existingChunk.name not in chunkNames:
        chunkNames.append(existingChunk.name)
    return chunkNames
  
  def add_entry_index_table(self, filename, part_name,datanode_id):
  
    if filename in self.__indexTable.keys():
      for existingChunk in self.__indexTable[filename]:
        chunkNamesList = self.getChunkNames(filename)
        if existingChunk.name==part_name:
          existingChunk.add_location(datanode_id)
        elif part_name not in chunkNamesList:
          chunk = Chunk(name=part_name,datanodesInSystem=self.datanodeListInSystem)
          chunk.add_location(datanode_id)
          self.__indexTable[filename].append(chunk)
        
      self.logger.info("Updated index table")
    else:
      chunk= Chunk(name=part_name,datanodesInSystem=self.datanodeListInSystem)
      chunk.add_location(datanode_id) 
      self.__indexTable[filename] = [chunk]
      self.logger.info("Updated index table")
    
      
  '''def print_indexTable(self):
    for filename in self.__indexTable.keys():
      print(filename+"\n")
      print(len(self.__indexTable[filename]))
      for existingChunk in self.__indexTable[filename]:
        print(f' || PRINT --- name: {existingChunk.name} || ')
        for location in existingChunk.locations.get_alive_datanodes():
          datanode:Datanode=location
          print(f'|| PRINT --- location {datanode.location} ||')'''
