import socket
from logger import main_log, exception_log
def getConnectedSocket(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect((ip, port))
    except Exception as inst:
        main_log.error('Network down.  All network based renderers and sensors will not function.',
            inst)
    return sock
