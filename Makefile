#Borra y genera los archivos de proto (Re-genera los archivos de proto)
proto:
	@rm -f ./protos/*.py
	@python3 -m grpc_tools.protoc -I ./protos --python_out=./protos --pyi_out=./protos --grpc_python_out=./protos ./protos/file.proto