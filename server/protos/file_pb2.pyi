from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileDownloadRsp(_message.Message):
    __slots__ = ("buffer",)
    BUFFER_FIELD_NUMBER: _ClassVar[int]
    buffer: bytes
    def __init__(self, buffer: _Optional[bytes] = ...) -> None: ...

class FileDownloadReq(_message.Message):
    __slots__ = ("filename", "chunkname")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CHUNKNAME_FIELD_NUMBER: _ClassVar[int]
    filename: str
    chunkname: str
    def __init__(self, filename: _Optional[str] = ..., chunkname: _Optional[str] = ...) -> None: ...

class ListReq(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FileListReq(_message.Message):
    __slots__ = ("filename",)
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    filename: str
    def __init__(self, filename: _Optional[str] = ...) -> None: ...

class FileListRsp(_message.Message):
    __slots__ = ("filename", "size")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    filename: str
    size: int
    def __init__(self, filename: _Optional[str] = ..., size: _Optional[int] = ...) -> None: ...

class FileUploadReq(_message.Message):
    __slots__ = ("filename", "chunkname", "buffer")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CHUNKNAME_FIELD_NUMBER: _ClassVar[int]
    BUFFER_FIELD_NUMBER: _ClassVar[int]
    filename: str
    chunkname: str
    buffer: bytes
    def __init__(self, filename: _Optional[str] = ..., chunkname: _Optional[str] = ..., buffer: _Optional[bytes] = ...) -> None: ...

class UploadRsp(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
