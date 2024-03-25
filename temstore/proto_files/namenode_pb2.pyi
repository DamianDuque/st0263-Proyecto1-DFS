from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

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
    __slots__ = ("localization",)
    LOCALIZATION_FIELD_NUMBER: _ClassVar[int]
    localization: str
    def __init__(self, localization: _Optional[str] = ...) -> None: ...

class DatanodeInfo(_message.Message):
    __slots__ = ("socket",)
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    socket: str
    def __init__(self, socket: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
