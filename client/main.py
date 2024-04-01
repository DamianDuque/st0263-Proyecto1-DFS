import argparse
import logging
from client.client import Client
from dotenv import load_dotenv
import os
load_dotenv("client/.env")
def main():
  namenodeIp= os.getenv("NAMENODE_IP")
  namenodePort=os.getenv("NAMENODE_PORT")
  log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  logging.basicConfig(level=logging.INFO, format=log_fmt)
  logger = logging.getLogger(__name__)

  parser = argparse.ArgumentParser(description="client")
  subparsers = parser.add_subparsers(dest="action", help="=> actions")
  subparsers.required = True
  subparsers.add_parser("list", help="list files on distributed file system")

  download_parser = subparsers.add_parser("open", help="open file from server")
  download_parser.add_argument(
    "-out", "--root_dir", required=True, type=str, help="root client output directory")
  download_parser.add_argument(
    "-in", "--in_dir", required=True, type=str, help="root client input directory ")
  download_parser.add_argument("-f", "--filename", required=True, type=str, help="file name to open")
  upload_parser = subparsers.add_parser("create",help="create and upload file to server")
  upload_parser.add_argument(
    "-out", "--root_dir", required=True, type=str, help="root client output directory")
  upload_parser.add_argument(
    "-in", "--in_dir", required=True, type=str, help="root client input directory ")
  upload_parser.add_argument("-f", "--filename", required=True, type=str, help="file name to create")


  args = parser.parse_args()


  client = Client(namenodeIp, namenodePort,args.root_dir,args.in_dir)

  action = args.action
  if action == "open":
    client.open(args.filename)
  elif action== "create":
    client.create(args.filename)
  elif action== "ls":
    client.list_index()
  else:
    logger.error("no such action " + action)

if __name__ == "__main__":
  main()
