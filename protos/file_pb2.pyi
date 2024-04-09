from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReadFileRsp(_message.Message):
    __slots__ = ("buffer",)
    BUFFER_FIELD_NUMBER: _ClassVar[int]
    buffer: bytes
    def __init__(self, buffer: _Optional[bytes] = ...) -> None: ...

class ReadFileReq(_message.Message):
    __slots__ = ("filename", "chunkname")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CHUNKNAME_FIELD_NUMBER: _ClassVar[int]
    filename: str
    chunkname: str
    def __init__(self, filename: _Optional[str] = ..., chunkname: _Optional[str] = ...) -> None: ...

class WriteFileReq(_message.Message):
    __slots__ = ("filename", "chunkname", "buffer")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CHUNKNAME_FIELD_NUMBER: _ClassVar[int]
    BUFFER_FIELD_NUMBER: _ClassVar[int]
    filename: str
    chunkname: str
    buffer: bytes
    def __init__(self, filename: _Optional[str] = ..., chunkname: _Optional[str] = ..., buffer: _Optional[bytes] = ...) -> None: ...

class WriteRsp(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FileOpenReq(_message.Message):
    __slots__ = ("filename",)
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    filename: str
    def __init__(self, filename: _Optional[str] = ...) -> None: ...

class FileCreateReq(_message.Message):
    __slots__ = ("filename", "chunks_number", "operation")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_NUMBER_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    filename: str
    chunks_number: int
    operation: str
    def __init__(self, filename: _Optional[str] = ..., chunks_number: _Optional[int] = ..., operation: _Optional[str] = ...) -> None: ...

class HeartBeatRsp(_message.Message):
    __slots__ = ("cluster_id", "id_datanode", "is_leader")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    ID_DATANODE_FIELD_NUMBER: _ClassVar[int]
    IS_LEADER_FIELD_NUMBER: _ClassVar[int]
    cluster_id: int
    id_datanode: str
    is_leader: bool
    def __init__(self, cluster_id: _Optional[int] = ..., id_datanode: _Optional[str] = ..., is_leader: bool = ...) -> None: ...

class DatanodeList(_message.Message):
    __slots__ = ("localization", "chunkname")
    LOCALIZATION_FIELD_NUMBER: _ClassVar[int]
    CHUNKNAME_FIELD_NUMBER: _ClassVar[int]
    localization: str
    chunkname: str
    def __init__(self, localization: _Optional[str] = ..., chunkname: _Optional[str] = ...) -> None: ...

class WarningMessage(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class CreateRsp(_message.Message):
    __slots__ = ("datanode_list", "warning_message")
    DATANODE_LIST_FIELD_NUMBER: _ClassVar[int]
    WARNING_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    datanode_list: DatanodeList
    warning_message: WarningMessage
    def __init__(self, datanode_list: _Optional[_Union[DatanodeList, _Mapping]] = ..., warning_message: _Optional[_Union[WarningMessage, _Mapping]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DatanodeInfo(_message.Message):
    __slots__ = ("id", "socket", "cluster")
    ID_FIELD_NUMBER: _ClassVar[int]
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    id: str
    socket: str
    cluster: int
    def __init__(self, id: _Optional[str] = ..., socket: _Optional[str] = ..., cluster: _Optional[int] = ...) -> None: ...

class ChunkReport(_message.Message):
    __slots__ = ("partname", "filename", "location")
    PARTNAME_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    partname: str
    filename: str
    location: str
    def __init__(self, partname: _Optional[str] = ..., filename: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class DirectoryContent(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class LeaderFollowersReq(_message.Message):
    __slots__ = ("leader_id", "cluster_id")
    LEADER_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    leader_id: str
    cluster_id: int
    def __init__(self, leader_id: _Optional[str] = ..., cluster_id: _Optional[int] = ...) -> None: ...

class follower_info(_message.Message):
    __slots__ = ("follower_id", "follower_location")
    FOLLOWER_ID_FIELD_NUMBER: _ClassVar[int]
    FOLLOWER_LOCATION_FIELD_NUMBER: _ClassVar[int]
    follower_id: str
    follower_location: str
    def __init__(self, follower_id: _Optional[str] = ..., follower_location: _Optional[str] = ...) -> None: ...
