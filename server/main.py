from server import FileServer
import os
import logging
from dotenv import load_dotenv


load_dotenv("server/.env")
#Cargando variables de entorno y retorndolas
def initialize()->tuple[int, int, int, str, str, str]:
    address = str(os.getenv("SERVER_HOST"))
    port = str(os.getenv("SERVER_PORT"))
    workers = int(os.getenv("SERVER_WORKERS"))
    directory = os.getenv("SERVER_DIRECTORY")
    key = os.getenv("SERVER_PRIVATE_KEY_PATH")
    certificate = os.getenv("SERVER_CERTIFICATE_PATH")
    return address, port, workers, directory, key, certificate
def main():
  log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  logging.basicConfig(level=logging.INFO, format=log_fmt)
  ip_address, port, max_workers, files_directory, private_key_file, cert_file = initialize()
  
  server = FileServer(
    ip_address,
    port,
    max_workers,
    files_directory,
    private_key_file,
    cert_file)
  server.start()

if __name__ == "__main__":
  main()
