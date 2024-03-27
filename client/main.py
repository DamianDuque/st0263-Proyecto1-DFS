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

  parser = argparse.ArgumentParser(description="gRPC file transfer client")
  parser.add_argument(
    "-out", "--root_dir", required=True, type=str, help="root client directory")
  parser.add_argument(
    "-in", "--in_dir", required=True, type=str, help="root client directory")
  subparsers = parser.add_subparsers(dest="action", help="client possible actions")
  subparsers.required = True

  download_parser = subparsers.add_parser("open", help="open file from server")
  download_parser.add_argument("-f", "--filename", required=True, type=str, help="file name to open")
  upload_parser = subparsers.add_parser("create",help="create and upload file to server")
  upload_parser.add_argument("-f", "--filename", required=True, type=str, help="file name to create")
  list_parser = subparsers.add_parser("ls",help="list directories and files")

  subparsers.add_parser("list", help="list files on server")

  args = parser.parse_args()

  logger.info("ip_adress:{ip_adress}, port:{port}, action:{action}"
    .format(
      ip_adress=namenodeIp,
      port=namenodePort,
      action=args.action))

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
