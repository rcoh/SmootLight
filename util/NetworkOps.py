import socket
from logger import main_log, exception_log
def getConnectedSocket(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect((ip, port))
        return sock
    except Exception as inst:
        main_log.error('Network down.  All network based renderers and sensors will not function.',
            inst)

def getBroadcastSocket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return s
