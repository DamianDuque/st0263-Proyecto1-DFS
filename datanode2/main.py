from server import DatanodeServer
import os
import logging
from dotenv import load_dotenv


load_dotenv("datanode2/.env")
#Cargando variables de entorno y retorndolas
def initialize()->tuple[int, int, int, str, str, str]:
    address = str(os.getenv("SERVER_HOST"))
    port = str(os.getenv("SERVER_PORT"))
    workers = int(os.getenv("SERVER_WORKERS"))
    directory = os.getenv("SERVER_DIRECTORY")
    return address, port, workers, directory
def main():
  log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  logging.basicConfig(level=logging.INFO, format=log_fmt)
  ip_address, port, max_workers, files_directory = initialize()
  
  server = DatanodeServer(
    ip_address,
    port,
    max_workers,
    files_directory)
  server.start()

if __name__ == "__main__":
  main()
