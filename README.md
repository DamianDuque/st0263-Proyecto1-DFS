# grpc-file-transfer

SSL secured file transfer gRPC client and server written in Python language.
Original Repo: https://github.com/r-sitko/grpc-file-transfer/blob/master/server/main.py


### Prerequisites

* Python3
* pip3
* OpenSSL

### Example usage

1. Prepare project:
    - Go to project root directory.
    - Use the package manager for Python to install dependencies.
        ```bash
        pip3 install -r requirements.txt
        ```
1. Launch gRPC file transfer server in first console:
    ```bash
    python server/main.py 
    ```
1. Launch gRPC file transfer client in second console:
    - list available files to download from server
        ```bash
        python -m client.main -i localhost -p 8000 -c cert/server.crt -dir client/resources list
        ```
    - download *test_file.txt* file from server to *resources/client* directory:
        ```bash
        python -m client.main -i localhost -p 8000 -c cert/server.crt -dir client/resources  open  -f file1.txt
        ```
    - upload file *test_file.txt* (by default in a const dir)
        ```bash
        python -m client.main -i localhost -p 8000 -c cert/server.crt -dir client/resources  upload  -f damian.jpg -p part0003.txt
        ```
## Description of client and server arguments

* server
```
```
* client
```
usage: main.py [-h] -i IP_ADRESS -p PORT -c CERT_FILE {download,list} ...

gRPC file transfer client

positional arguments:
  {download,list}       client possible actions
    download            download file from server
    list                list files on server

optional arguments:
  -h, --help            show this help message and exit
  -i IP_ADRESS, --ip_adress IP_ADRESS
                        IP address of server
  -p PORT, --port PORT  port address of server
  -c CERT_FILE, --cert_file CERT_FILE
                        certificate file path

If you use download action you must provide below paramaters:
optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        where to save files
  -f FILE, --file FILE  file name to download
```
