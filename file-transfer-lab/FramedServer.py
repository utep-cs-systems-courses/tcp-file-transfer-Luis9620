import sys
import socket
import params
from os.path import exists
from framedSock import framedSend, framedReceive
sys.path.append("../lib")  # for params

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", True),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)


paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # listener socket
binding_address = ("127.0.0.1", listenPort)
listener_socket.bind(binding_address)
listener_socket.listen(5)
print("Listening on:", binding_address)

sock, addr = listener_socket

print("connection rec'd from", addr)


while True:
    payload = framedReceive(sock, debug)
    if debug:
        print("rec'd: ", payload)
    if not payload:
        break
    payload += b"!"  # make emphatic!
    framedSend(sock, payload, debug)

    output_file = input("Type the output file name: ")

    if exists(output_file):
        user_input = input("File already exists. Do you want to overwrite the file you entered? ")
        if user_input == 'yes':
            output = open(output_file, 'w')
            payload = payload.decode('utf8')
            output.write(payload)
        else:
            pass
    else:
        output = open(output_file, 'w')
        payload = payload.decode('utf8')
        output.write(payload)