from server import DatanodeServer
from heartBeatClient import Client
from reports import Reports
from threading import Thread
import os
import logging
from dotenv import load_dotenv

def run_fist_ping(client:Client):
  datanode_id,cluster_id = client.ping(1)
  return datanode_id,cluster_id
def run_ping(client:Client):
  client.ping(9)
def run_initial_report(report:Reports,directory):
  report.initial_report(directory=directory)
    
load_dotenv("datanode/.env")
def initialize()->tuple[int, int, int, int, str, str, str, str]:
    address = str(os.getenv("SERVER_HOST"))
    port = str(os.getenv("SERVER_PORT"))
    workers = int(os.getenv("SERVER_WORKERS"))
    directory = os.getenv("SERVER_DIRECTORY")
    nameNodeIP= os.getenv("NAMENODE_IP")
    nameNodePort= os.getenv("NAMENODE_PORT")
    ttl = int(os.getenv("TTL"))
    datanode_id = os.getenv("DATANODE_ID")
    cluster_id= os.getenv("CLUSTER_ID")
    return address, port, workers, directory, nameNodeIP, nameNodePort, ttl, datanode_id,cluster_id
def main():
  log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  logging.basicConfig(level=logging.INFO, format=log_fmt)
  ip_address, port, max_workers, files_directory,nameNodeIP,nameNodePort,ttl, datanode_id,cluster_id = initialize()
  
  client = Client(
    datanode_id,
    cluster_id,
    ip_address, 
    port,
    nameNodeIP,
    nameNodePort,
    ttl
  ) 
  datanode_id,cluster_id = run_fist_ping(client=client)
  client = Client(
    datanode_id,
    cluster_id,
    ip_address, 
    port,
    nameNodeIP,
    nameNodePort,
    ttl
  ) 
  #Do after first ping
  report = Reports(
    datanode_id,
    nameNodeIP,
    nameNodePort)
  
  run_initial_report(report,files_directory)
  
  server = DatanodeServer(
    ip_address,
    port,
    max_workers,
    files_directory,
    report)

  

  ping_thread = Thread(target=run_ping, args=(client,))
  ping_thread.setDaemon(True)
  ping_thread.start()
  server.start()  
  

if __name__ == "__main__":
  main()
