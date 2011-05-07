import socket
import time
HOST = ''
PORT = 3344
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

(data,address) = sock.recvfrom(1024)
lastt = time.time()
c=0
addresses = set()
while data:
    c+=1
    dt =( time.time()-lastt )
    if dt > 1:
	print c/dt, " packets per second from", len(addresses), "unique addresses"
        c = 0
        addresses = set()
        lastt = time.time()
    if 1:#address[-1]=='7':
        print list(map(ord,data)), '\t', address
    (data, address) = sock.recvfrom(1024)
    addresses.add(address)
