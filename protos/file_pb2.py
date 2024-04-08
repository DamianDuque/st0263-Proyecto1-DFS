# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nfile.proto\"\x1d\n\x0bReadFileRsp\x12\x0e\n\x06\x62uffer\x18\x01 \x01(\x0c\"2\n\x0bReadFileReq\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x11\n\tchunkname\x18\x02 \x01(\t\"C\n\x0cWriteFileReq\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x11\n\tchunkname\x18\x02 \x01(\t\x12\x0e\n\x06\x62uffer\x18\x03 \x01(\x0c\"\n\n\x08WriteRsp\"\x1f\n\x0b\x46ileOpenReq\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"K\n\rFileCreateReq\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x15\n\rchunks_number\x18\x02 \x01(\x03\x12\x11\n\toperation\x18\x03 \x01(\t\"J\n\x0cHeartBeatRsp\x12\x12\n\ncluster_id\x18\x01 \x01(\x03\x12\x13\n\x0bid_datanode\x18\x02 \x01(\t\x12\x11\n\tis_leader\x18\x03 \x01(\x08\"7\n\x0c\x44\x61tanodeList\x12\x14\n\x0clocalization\x18\x01 \x01(\t\x12\x11\n\tchunkname\x18\x02 \x01(\t\"!\n\x0eWarningMessage\x12\x0f\n\x07message\x18\x01 \x01(\t\"k\n\tCreateRsp\x12&\n\rdatanode_list\x18\x01 \x01(\x0b\x32\r.DatanodeListH\x00\x12*\n\x0fwarning_message\x18\x02 \x01(\x0b\x32\x0f.WarningMessageH\x00\x42\n\n\x08Response\"\x07\n\x05\x45mpty\";\n\x0c\x44\x61tanodeInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06socket\x18\x02 \x01(\t\x12\x0f\n\x07\x63luster\x18\x03 \x01(\x03\"C\n\x0b\x43hunkReport\x12\x10\n\x08partname\x18\x01 \x01(\t\x12\x10\n\x08\x66ilename\x18\x02 \x01(\t\x12\x10\n\x08location\x18\x03 \x01(\t\" \n\x10\x44irectoryContent\x12\x0c\n\x04name\x18\x01 \x01(\t\";\n\x12LeaderFollowersReq\x12\x11\n\tleader_id\x18\x01 \x01(\t\x12\x12\n\ncluster_id\x18\x02 \x01(\x03\"&\n\rfollower_info\x12\x15\n\rfollower_info\x18\x01 \x01(\t2Q\n\x04\x46ile\x12$\n\x04read\x12\x0c.ReadFileReq\x1a\x0c.ReadFileRsp\"\x00\x12#\n\x05write\x12\r.WriteFileReq\x1a\t.WriteRsp\"\x00\x32\x97\x02\n\x0fNameNodeService\x12\'\n\x04open\x12\x0c.FileOpenReq\x1a\r.DatanodeList\"\x00\x30\x01\x12(\n\x06\x63reate\x12\x0e.FileCreateReq\x1a\n.CreateRsp\"\x00\x30\x01\x12,\n\nheart_beat\x12\r.DatanodeInfo\x1a\r.HeartBeatRsp\"\x00\x12 \n\x06report\x12\x0c.ChunkReport\x1a\x06.Empty\"\x00\x12\'\n\x06listin\x12\x06.Empty\x1a\x11.DirectoryContent\"\x00\x30\x01\x12\x38\n\rget_followers\x12\x13.LeaderFollowersReq\x1a\x0e.follower_info\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'file_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_READFILERSP']._serialized_start=14
  _globals['_READFILERSP']._serialized_end=43
  _globals['_READFILEREQ']._serialized_start=45
  _globals['_READFILEREQ']._serialized_end=95
  _globals['_WRITEFILEREQ']._serialized_start=97
  _globals['_WRITEFILEREQ']._serialized_end=164
  _globals['_WRITERSP']._serialized_start=166
  _globals['_WRITERSP']._serialized_end=176
  _globals['_FILEOPENREQ']._serialized_start=178
  _globals['_FILEOPENREQ']._serialized_end=209
  _globals['_FILECREATEREQ']._serialized_start=211
  _globals['_FILECREATEREQ']._serialized_end=286
  _globals['_HEARTBEATRSP']._serialized_start=288
  _globals['_HEARTBEATRSP']._serialized_end=362
  _globals['_DATANODELIST']._serialized_start=364
  _globals['_DATANODELIST']._serialized_end=419
  _globals['_WARNINGMESSAGE']._serialized_start=421
  _globals['_WARNINGMESSAGE']._serialized_end=454
  _globals['_CREATERSP']._serialized_start=456
  _globals['_CREATERSP']._serialized_end=563
  _globals['_EMPTY']._serialized_start=565
  _globals['_EMPTY']._serialized_end=572
  _globals['_DATANODEINFO']._serialized_start=574
  _globals['_DATANODEINFO']._serialized_end=633
  _globals['_CHUNKREPORT']._serialized_start=635
  _globals['_CHUNKREPORT']._serialized_end=702
  _globals['_DIRECTORYCONTENT']._serialized_start=704
  _globals['_DIRECTORYCONTENT']._serialized_end=736
  _globals['_LEADERFOLLOWERSREQ']._serialized_start=738
  _globals['_LEADERFOLLOWERSREQ']._serialized_end=797
  _globals['_FOLLOWER_INFO']._serialized_start=799
  _globals['_FOLLOWER_INFO']._serialized_end=837
  _globals['_FILE']._serialized_start=839
  _globals['_FILE']._serialized_end=920
  _globals['_NAMENODESERVICE']._serialized_start=923
  _globals['_NAMENODESERVICE']._serialized_end=1202
# @@protoc_insertion_point(module_scope)
