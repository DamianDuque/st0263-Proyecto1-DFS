# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import file_pb2 as file__pb2


class FileStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.read = channel.unary_unary(
                '/File/read',
                request_serializer=file__pb2.ReadFileReq.SerializeToString,
                response_deserializer=file__pb2.ReadFileRsp.FromString,
                )
        self.write = channel.unary_unary(
                '/File/write',
                request_serializer=file__pb2.WriteFileReq.SerializeToString,
                response_deserializer=file__pb2.WriteRsp.FromString,
                )


class FileServicer(object):
    """Missing associated documentation comment in .proto file."""

    def read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def write(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'read': grpc.unary_unary_rpc_method_handler(
                    servicer.read,
                    request_deserializer=file__pb2.ReadFileReq.FromString,
                    response_serializer=file__pb2.ReadFileRsp.SerializeToString,
            ),
            'write': grpc.unary_unary_rpc_method_handler(
                    servicer.write,
                    request_deserializer=file__pb2.WriteFileReq.FromString,
                    response_serializer=file__pb2.WriteRsp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'File', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class File(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def read(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/File/read',
            file__pb2.ReadFileReq.SerializeToString,
            file__pb2.ReadFileRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def write(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/File/write',
            file__pb2.WriteFileReq.SerializeToString,
            file__pb2.WriteRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class NameNodeServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.open = channel.unary_stream(
                '/NameNodeService/open',
                request_serializer=file__pb2.FileOpenReq.SerializeToString,
                response_deserializer=file__pb2.DatanodeList.FromString,
                )
        self.create = channel.unary_stream(
                '/NameNodeService/create',
                request_serializer=file__pb2.FileCreateReq.SerializeToString,
                response_deserializer=file__pb2.CreateRsp.FromString,
                )
        self.heart_beat = channel.unary_unary(
                '/NameNodeService/heart_beat',
                request_serializer=file__pb2.DatanodeInfo.SerializeToString,
                response_deserializer=file__pb2.HeartBeatRsp.FromString,
                )
        self.report = channel.unary_unary(
                '/NameNodeService/report',
                request_serializer=file__pb2.ChunkReport.SerializeToString,
                response_deserializer=file__pb2.Empty.FromString,
                )
        self.listin = channel.unary_stream(
                '/NameNodeService/listin',
                request_serializer=file__pb2.Empty.SerializeToString,
                response_deserializer=file__pb2.DirectoryContent.FromString,
                )
        self.get_followers = channel.unary_stream(
                '/NameNodeService/get_followers',
                request_serializer=file__pb2.LeaderFollowersReq.SerializeToString,
                response_deserializer=file__pb2.follower_info.FromString,
                )


class NameNodeServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def open(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def heart_beat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def report(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def listin(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_followers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NameNodeServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'open': grpc.unary_stream_rpc_method_handler(
                    servicer.open,
                    request_deserializer=file__pb2.FileOpenReq.FromString,
                    response_serializer=file__pb2.DatanodeList.SerializeToString,
            ),
            'create': grpc.unary_stream_rpc_method_handler(
                    servicer.create,
                    request_deserializer=file__pb2.FileCreateReq.FromString,
                    response_serializer=file__pb2.CreateRsp.SerializeToString,
            ),
            'heart_beat': grpc.unary_unary_rpc_method_handler(
                    servicer.heart_beat,
                    request_deserializer=file__pb2.DatanodeInfo.FromString,
                    response_serializer=file__pb2.HeartBeatRsp.SerializeToString,
            ),
            'report': grpc.unary_unary_rpc_method_handler(
                    servicer.report,
                    request_deserializer=file__pb2.ChunkReport.FromString,
                    response_serializer=file__pb2.Empty.SerializeToString,
            ),
            'listin': grpc.unary_stream_rpc_method_handler(
                    servicer.listin,
                    request_deserializer=file__pb2.Empty.FromString,
                    response_serializer=file__pb2.DirectoryContent.SerializeToString,
            ),
            'get_followers': grpc.unary_stream_rpc_method_handler(
                    servicer.get_followers,
                    request_deserializer=file__pb2.LeaderFollowersReq.FromString,
                    response_serializer=file__pb2.follower_info.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'NameNodeService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NameNodeService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def open(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/NameNodeService/open',
            file__pb2.FileOpenReq.SerializeToString,
            file__pb2.DatanodeList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/NameNodeService/create',
            file__pb2.FileCreateReq.SerializeToString,
            file__pb2.CreateRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def heart_beat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NameNodeService/heart_beat',
            file__pb2.DatanodeInfo.SerializeToString,
            file__pb2.HeartBeatRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def report(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NameNodeService/report',
            file__pb2.ChunkReport.SerializeToString,
            file__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def listin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/NameNodeService/listin',
            file__pb2.Empty.SerializeToString,
            file__pb2.DirectoryContent.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_followers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/NameNodeService/get_followers',
            file__pb2.LeaderFollowersReq.SerializeToString,
            file__pb2.follower_info.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
