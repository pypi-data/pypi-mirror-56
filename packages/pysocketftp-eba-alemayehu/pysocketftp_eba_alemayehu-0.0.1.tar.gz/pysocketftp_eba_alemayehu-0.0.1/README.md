# iCog course development tools final project
## Socket file transfer program
> Author: **Eba Alemayehu**
___
## Introduction 

In general this parogram is used to transfer file form the client to the server by using socket. The program uses both C and python programming languages. The c programm makes the socket connection and the python program wrap the c shared liberary and use the methods defined in the library to transfer file to the server. 

This paogram is packaged in wheele file and it is available in pip installer. 


    pip install pysocketftp-eba

## Directory structure

    +-- pysocketftp
    |   +-- socket_ftp_c
    |   |   +-- common.c
    |   |   +-- common.h
    |   |   +-- receive_file.c
    |   |   +-- receive_file.h
    |   |   +-- send_file.c
    |   |   +-- send_file.h
    |   |   +-- CMakeList.txt
    |   +-- __init__.py
    |   +-- socket.py
    +-- src
    |   +-- client_test.c
    |   +-- server_test.s
    |   +-- client.py
    |   +-- server.py
    |   +-- CMakeList.txt
    +-- .gitignore
    +-- README.md
    +-- setup.py

## C socket program
`pysocketftp/socket_ftp_c/`

    recive_file.c

Containes a function called `recive_file(int port)' it accepept one parameter port which is a port number the socket connection will be waiting to accept connection. 

    send_file.c

Contain a fucntion called `send_file()` it accept two paramtters, which are the address to the server which the file will be sent and the path to the file to be sent. 
  
    common.c
Contain two helper functions which are `ifErr` to show error and `formatedSize` to format the file size from bytes to corsponding format (KB, MB, GB)

## Python program 
`pysocketftp/`

    setup.py

It is a wrapper class which access the shared lib file produced from the c fucntions. It contain a class called `Socket`.   `Socket` contain a constructor and two methods. The constructor initialize port and load the c shared lib with `ctypes`. `accept` method starts the server to listen to accept file. `send` method accept the address of the sever and the file path then send the file to the server. 

We have `server.py` and `client.py` files which implement the package as an example. `client.py accept two args, the address of the server and the  file path. 

Start the server
        $ python server.py

Send the file
        $ python client.py 10.0.0.2 /path/to/file  

## Packageing

The project is packaged to `pysocketftp` package. The configraion is written in `setup.py`. The name of the package setup. To run the package 

    python setup.py sdist bdist_wheel

Also the c files are compiled with a `cmake`. `socket_ftp_c/CMakeFile.txt` must be compled to `socket_ftp_c/build` dir. 