import sys
sys.path.append("../lib")
import re, socket, params, os
from os.path import exists
from threading import Thread, enumerate, Lock
global filelock
filelock = Lock()
switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50002),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)
activeFiles = []


def check_file_name(filename, sock):
    if filename in activeFiles:
        print("Already in the server: " + filename)
        sock.sendall("True".encode('utf-8'))
        return True
    else:
        activeFiles.append(filename)
        sock.sendall("False".encode('utf-8'))
        print(activeFiles)
        return False


def remove_file_name(filename):
    activeFiles.remove(filename)


class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr

    def run(self):
        print("[+] Client connected", self.addr)
        print("new thread handling connection from", self.addr)
        file_name = self.sock.recv(1024)

        filelock.acquire()
        file_exist = check_file_name(file_name.decode("utf-8"), self.sock)
        filelock.release()

        if not file_exist:
            file_data = self.sock.recv(1024)
            remote_filename = "remote" + file_name.decode('utf-8').capitalize()
            file = open(remote_filename, "wb")
            file.write(file_data)
            remove_file_name(file_name.decode('utf-8'))


 # Establish connection with client


while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()