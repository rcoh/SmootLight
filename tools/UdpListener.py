import socket

HOST = ''
PORT = 3344
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

(data,address) = sock.recvfrom(1024)
while data:
    print data, ' @', address
    (data, address) = sock.recvfrom(1024)
