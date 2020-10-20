#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50002),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    if not os.fork():
        print("[+] New child process handling connection", addr)
        file_name = sock.recv(1024)
        file_exist = os.path.exists("./" + file_name.decode('utf-8'))
        print(file_exist)
        sock.sendall(str(file_exist).encode('utf-8'))

        if not file_exist:
            file_data = sock.recv(1024)
            filename = "remote" + file_name.decode('utf-8').capitalize()
            file = open(filename, "wb")
            file.write(file_data)
            file.close()
        # print("new child process handling connection from", addr)
        # while True:
        #     payload = framedReceive(sock, debug)
        #     if debug: print("rec'd: ", payload)
        #     if not payload:
        #         if debug: print("child exiting")
        #         sys.exit(0)
        #     payload += b"!"             # make emphatic!
        #     framedSend(sock, payload, debug)