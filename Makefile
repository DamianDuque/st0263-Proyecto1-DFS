#Borra y genera los archivos de proto (Re-genera los archivos de proto)
proto-client-datanode:
	@rm -f ./protos/file_pb2_grpc.py
	@rm -f ./protos/file_pb2.py
	@python3 -m grpc_tools.protoc -I ./protos --python_out=./protos --pyi_out=./protos --grpc_python_out=./protos ./protos/file.proto
proto-datanode:
	@rm -f ./datanode/protos/*.py
	@python3 -m grpc_tools.protoc -I ./datanode/protos --python_out=./datanode/protos --pyi_out=./datanode/protos --grpc_python_out=./protos ./datanode/protos/file.proto
#Borra y genera los archivos de proto (Re-genera los archivos de proto)
proto-namenode:
	@rm -f ./namenode/src/proto_files/*.py
	@python3 -m grpc_tools.protoc -I ./namenode/src/proto_files --python_out=./namenode/src/proto_files --pyi_out=./namenode/src/proto_files --grpc_python_out=./namenode/src/proto_files ./namenode/src/proto_files/namenode.proto
proto-client-namenode:
	@rm -f ./protos/namenode_pb2_grpc.py
	@rm -f ./protos/namenode_pb2.py
	@python3 -m grpc_tools.protoc -I ./protos --python_out=./protos --pyi_out=./protos --grpc_python_out=./protos ./protos/namenode.proto