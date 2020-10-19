#! /usr/bin/env python3

import sys
import os
sys.path.append("../file-transfer-lab/lib")       # for params
import re, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
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

if __name__ == '__main__':
    while True:
        save_flags = False
        sock, addr = lsock.accept()  # Establish connection with client
        print("[+] Client connected", addr)
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

    # file = framedReceive(sock, debug)
    # newfile = file.decode()
    # newfile = "new" + newfile
    # print("'%s' has been saved to server files as: '%s'." % (file, newfile))

