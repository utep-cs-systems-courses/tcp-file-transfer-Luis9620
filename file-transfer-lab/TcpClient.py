#! /usr/bin/env python3
import socket
import sys
import re
import params
from os.path import exists
from FramedSock import framed_send, framed_receive
sys.path.append("../lib")

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

address_family = socket.AF_INET
socket_type = socket.SOCK_STREAM
address_port = (serverHost, serverPort)

socket_to_connect = socket.socket(address_family, socket_type)

if socket_to_connect is None:
    print('There was a problem, could not open socket')
    sys.exit(1)

socket_to_connect.connect(address_port)

file_to_send = input("Name of the file to be send : ")

if exists(file_to_send):
    file_copy = open(file_to_send, 'r')
    file_data = file_copy.read()
    if len(file_data.encode('utf-8')) == 0:
        sys.exit(0)
    else:
        framed_send(socket_to_connect, file_data.encode(), debug)
        print("received:", framed_receive(socket_to_connect, debug))

else:
    print("file does not exist.")
    sys.exit(0)
