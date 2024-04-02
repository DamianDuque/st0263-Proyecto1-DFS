#Borra y genera los archivos de proto (Re-genera los archivos de proto)
proto-all:
	@rm -f ./protos/*.py
	@python -m grpc_tools.protoc -I ./protos --python_out=./protos --pyi_out=./protos --grpc_python_out=./protos ./protos/file.proto
run-namenode:
	@python namenode/main.py
run-datanode:
	@python datanode/main.py
