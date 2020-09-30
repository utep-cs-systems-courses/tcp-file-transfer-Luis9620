# ! /usr/bin/env python3
import sys
import re
import socket
sys.path.append("../lib")       # for params
import params
import os
from FramedSock import framed_send, framed_receive

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
listener_socket.bind(binding_address)
listener_socket(5)
print("Listening on: ", binding_address)

if __name__ == '__main__':
    while True:
        sock, address = listener_socket.accept()
        while True:
            payload = framed_receive(sock, debug)
            if debug:
                print("rec'd: ", payload)
            if not payload:
                break
            payload += b"!"  # make emphatic!
            framed_send(sock, payload, debug)

            output_file = input("give me output: ")
            output = open(output_file, 'w')
            payload = payload.decode('utf8')
            output.write(payload)



