#! /usr/bin/env python3

import socket, sys, re
import pathlib
sys.path.append("../lib")
import params
from os import path
from os.path import exists

from framedSock import FramedSock

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
)

progname = "testClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Cant parse Server: port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

sock = socket.socket(addrFamily, socktype)

if sock is None:
    print('could not open socket')
    sys.exit(1)
sock.connect(addrPort)

fsock = FramedSock((sock, addrPort))
for i in range(1):
    filename = input("Enter the the filename of the file to be transfer: ")
    if exists(filename):
        file = open(filename, 'rb')
        payload = file.read()
        if len(payload) == 0:
            print("Cant send empty file")
            sys.exit(0)
        else:
            fsock.send(filename.encode(), debug)
            file_exists = fsock.receive(debug).decode()
            if file_exists == 'True':
                print("That file all ready exist")
                sys.exit(0)
            else:
                fsock.send(payload, debug)
                print("Server:  ", fsock.receive(debug).decode())
    else:
        print("File '%s' dosnt exist." % filename)
        print(pathlib.Path().absolute())
