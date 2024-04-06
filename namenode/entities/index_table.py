import logging
from .datanode_list import DatanodeListStructure
from .chunk_struct import Chunk
class IndexTable:
  def __init__(self, logger:logging.Logger, datanodeListInSystem:DatanodeListStructure):
    self.__indexTable={}
    self.datanodeListInSystem=datanodeListInSystem

  def add_entry_index_table(self, filename, part_info,datanode_id):
    self.__indexTable[filename] = [Chunk(name=part_info,datanodesList=self.datanodeListInSystem)]
    self.logger.info("Updated index table to {table}".format(table=self.__indexTable.values())) 