from server import DatanodeServer
from heartBeatClient import Client
from uuid import uuid4
from reports import Reports
from threading import Thread
import os
import logging
from dotenv import load_dotenv

def run_ping(client:Client):
  client.ping()
def run_initial_report(report:Reports,directory):
  report.initial_report(directory=directory)
    
load_dotenv("datanode/.env")
#Cargando variables de entorno y retorndolas
def initialize()->tuple[int, int, int, int, str, str, str]:
    address = str(os.getenv("SERVER_HOST"))
    port = str(os.getenv("SERVER_PORT"))
    workers = int(os.getenv("SERVER_WORKERS"))
    directory = os.getenv("SERVER_DIRECTORY")
    nameNodeIP= os.getenv("NAMENODE_IP")
    nameNodePort= os.getenv("NAMENODE_PORT")
    ttl = int(os.getenv("TTL"))
    return address, port, workers, directory, nameNodeIP, nameNodePort, ttl
def main():
  log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  logging.basicConfig(level=logging.INFO, format=log_fmt)
  ip_address, port, max_workers, files_directory,nameNodeIP,nameNodePort,ttl = initialize()
  
  datanodeId = str(uuid4())[:8]

  report = Reports(
    datanodeId,
    nameNodeIP,
    nameNodePort)

  server = DatanodeServer(
    ip_address,
    port,
    max_workers,
    files_directory,
    report)

  client = Client(
    datanodeId,
    ip_address, 
    port,
    nameNodeIP,
    nameNodePort,
    ttl
  )
  initial_report_thread= Thread(target=run_initial_report, args=(report,files_directory,))
  ping_thread = Thread(target=run_ping, args=(client,))
  ping_thread.setDaemon(True)
  ping_thread.start()
  initial_report_thread.start()
  server.start()  
  

if __name__ == "__main__":
  main()
