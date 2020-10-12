import socket                   # Import socket module


s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 8082                    # Reserve a port for your service.
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print('Server listening....')
conn, addr = s.accept()
print(addr, "Has connected to the server.")
file_name = input(str("Enter the the filename of the file to be transfer:  "))
file = open(file_name, "rb")
file_data = file.read(1024)
conn.send(file_data)
print("Data has been sent successfully!")


# while True:
#     conn, addr = s.accept()     # Establish connection with client.
#     print('Got connection from', addr)
#     data = conn.recv(1024)
#     print('Server received', repr(data))
#
#     filename='mytext.txt'
#     f = open(filename,'rb')
#     l = f.read(1024)
#     while (l):
#        conn.send(l)
#        print('Sent ',repr(l))
#        l = f.read(1024)
#     f.close()
#
#     print('Done sending')
#     conn.send('Thank you for connecting')
#     conn.close()
