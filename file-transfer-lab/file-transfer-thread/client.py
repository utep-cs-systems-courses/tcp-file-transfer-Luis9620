import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 8082                    # Reserve a port for your service.
s.connect((host, port))
print("Connected...")
filename = input(str("Please enter a filename for the incoming file: "))
file = open(filename, "wb")
file_data = s.recv(1024)
file.write(file_data)
file.close()
print("File received successfully.")

# with open('received_file', 'wb') as f:
#     print('file opened')
#     while True:
#         print('receiving data...')
#         data = s.recv(1024)
#         print('data=%s', (data))
#         if not data:
#             break
#         # write data to a file
#         f.write(data)
#
# f.close()
# print('Successfully get the file')
# s.close()
# print('connection closed')