from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

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
    __slots__ = ("filename", "chunks_number")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_NUMBER_FIELD_NUMBER: _ClassVar[int]
    filename: str
    chunks_number: int
    def __init__(self, filename: _Optional[str] = ..., chunks_number: _Optional[int] = ...) -> None: ...

class DatanodeList(_message.Message):
    __slots__ = ("localization", "chunkname")
    LOCALIZATION_FIELD_NUMBER: _ClassVar[int]
    CHUNKNAME_FIELD_NUMBER: _ClassVar[int]
    localization: str
    chunkname: str
    def __init__(self, localization: _Optional[str] = ..., chunkname: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DatanodeInfo(_message.Message):
    __slots__ = ("socket",)
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    socket: str
    def __init__(self, socket: _Optional[str] = ...) -> None: ...

class ChunkReport(_message.Message):
    __slots__ = ("partname", "filename", "location")
    PARTNAME_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    partname: str
    filename: str
    location: str
    def __init__(self, partname: _Optional[str] = ..., filename: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...
