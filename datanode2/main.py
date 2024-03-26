from server import DatanodeServer
from heartBeatClient import Client
from threading import Thread
import os
import logging
from dotenv import load_dotenv

def run_ping(client:Client):
   client.ping()
    
    
load_dotenv("datanode2/.env")
#Cargando variables de entorno y retorndolas
def initialize()->tuple[int, int, int, str, str, str]:
    address = str(os.getenv("SERVER_HOST"))
    port = str(os.getenv("SERVER_PORT"))
    workers = int(os.getenv("SERVER_WORKERS"))
    directory = os.getenv("SERVER_DIRECTORY")
    nameNodeIP= os.getenv("NAMENODE_IP")
    nameNodePort= os.getenv("NAMENODE_PORT")
    return address, port, workers, directory,nameNodeIP,nameNodePort
def main():
  log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  logging.basicConfig(level=logging.INFO, format=log_fmt)
  ip_address, port, max_workers, files_directory,nameNodeIP,nameNodePort = initialize()
  
  server = DatanodeServer(
    ip_address,
    port,
    max_workers,
    files_directory)

  client = Client(
    ip_address,
    port,
    nameNodeIP,
    nameNodePort
  )
  ping_thread = Thread(target=run_ping, args=(client,))
  ping_thread.setDaemon(True)
  ping_thread.start()
  server.start()  
  

if __name__ == "__main__":
  main()