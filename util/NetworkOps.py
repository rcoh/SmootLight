import socket
def getConnectedSocket(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect((ip, port))
    except:
        print 'network down'
    return sock
