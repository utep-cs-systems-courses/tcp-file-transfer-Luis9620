# ! /usr/bin/env python3
import sys
import re
import socket
import params
import os

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
binding_address = ("127.0.0.1", listenPort)

if __name__ == '__main__':
    while True:
        sock, address = listener_socket.accept()
