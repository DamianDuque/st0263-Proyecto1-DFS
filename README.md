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
    python namenode/main.py 
    ```
1. Launch gRPC file transfer client in second console:
  
    - open *test_file.txt* file from server to *resources/client* directory:
        ```bash
        python -m client.main open -out client/resources/downloaded_files -f file.txt        
        ```
    - create file *test_file.txt* (by default in a const dir)
        ```bash
        python -m client.main create -out client/resources/partitioned_files -in client/resources/complete_files -f file.txt
        ```
    - append data from file *test_file.txt* to *test_file.txt* (by default in a const dir)
        ```bash
        python -m client.main append -out client/resources/partitioned_files -in client/resources/complete_files -f b.txt -fdfs a.txt
        ```
    - list of files stored in the system
        ```bash
        python -m client.main ls 
        ```
    - help command:
        ```bash
         python -m client.main  -h
        ```

      

