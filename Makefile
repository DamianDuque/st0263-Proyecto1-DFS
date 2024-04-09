#Borra y genera los archivos de proto (Re-genera los archivos de proto)
proto-all:
	@python -m grpc_tools.protoc -I ./protos --python_out=./protos --pyi_out=./protos --grpc_python_out=./protos ./protos/file.proto
run-namenode:
	@python namenode/main.py
run-datanode:
	@python datanode/main.py
run-docker-compose-namenode:
	@docker run \
    --name namenode \
    --env-file namenode/.env \
    --expose 8000 \
    -p 8000:8000 \
    -v $(pwd)/namenode:/app \
    --network proyecto-1 \
    your_preferred_image_name \
    python main.py
