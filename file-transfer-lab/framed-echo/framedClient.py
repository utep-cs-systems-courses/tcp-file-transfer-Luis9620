#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../file-transfer-lab/lib")       # for params
import params

from framedSock import framedSend, framedReceive, send_file




switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

if __name__ == '__main__':
    while True:
        file_name = input("Please enter the name of the file to send: ")
        file_name_encode = file_name.encode('utf-8')
        s.sendall(file_name_encode)
        send_check = True if (s.recv(1024)).decode('utf-8').lower() == "true" else False
        if send_check:
            print("The file already exist.")
            sys.exit(0)
        else:
            send_file(s, file_name)


# framedSend(s, b"hello world", debug)

# print("received:", framedReceive(s, debug))
#
# print("sending hello world")
# framedSend(s, b"hello world", debug)
# print("received:", framedReceive(s, debug))

