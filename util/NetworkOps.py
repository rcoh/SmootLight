import socket
def getConnectedSocket(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print (ip, port)
    sock.connect((ip, port))
    return sock
