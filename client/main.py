import argparse
import logging
from client.client import FileClient
import os

def main():
  log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  logging.basicConfig(level=logging.INFO, format=log_fmt)
  logger = logging.getLogger(__name__)

  parser = argparse.ArgumentParser(description="gRPC file transfer client")
  parser.add_argument(
    "-i", "--ip_adress", required=True, type=str, help="IP address of server")
  parser.add_argument(
    "-p", "--port", required=True, type=str, help="port address of server")
  parser.add_argument(
    "-c", "--cert_file", required=True, type=str, help="certificate file path")
  parser.add_argument(
    "-dir", "--root_dir", required=True, type=str, help="root client directory")
  subparsers = parser.add_subparsers(dest="action", help="client possible actions")
  subparsers.required = True

  download_parser = subparsers.add_parser("download", help="download file from server")
  download_parser.add_argument("-f", "--filename", required=True, type=str, help="file name to download")
  upload_parser = subparsers.add_parser("upload",help="upload file to server")
  upload_parser.add_argument("-f", "--filename", required=True, type=str, help="file name to upload")

  subparsers.add_parser("list", help="list files on server")

  args = parser.parse_args()

  logger.info("ip_adress:{ip_adress}, port:{port}, cert_file:{cert_file}, action:{action}"
    .format(
      ip_adress=args.ip_adress,
      port=args.port,
      cert_file=args.cert_file,
      action=args.action))

  client = FileClient(args.ip_adress, args.port, args.cert_file,args.root_dir)

  action = args.action
  if action == "download":
    client.download(args.filename, args.partition)
  elif action == "list":
    client.list()
  elif action== "upload":
    client.upload(args.filename)
  else:
    logger.error("no such action " + action)

if __name__ == "__main__":
  main()
