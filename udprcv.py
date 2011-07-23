#!/usr/bin/env python
import util.TimeOps as timeOps
import socket
import time
HOST = ''
PORT = 3344
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

def grabBits(p):
    return bin(ord(p))[2:].zfill(8) 

def parseBinarySensorPacket(p):#, firstBitIndex):
    #print 'starting to parse'
    if len(p) != 5:
        print 'bad length'
    packet = []
    for i,hexByte in enumerate(p):
        bits = grabBits(hexByte)
        packet += bits
    output = []
    #print packet
    packet = map(int, packet)
    #print packet
    #print sum(packet)
    #import pdb; pdb.set_trace()
    for j,b in enumerate(packet):
        if b == 1:
            #sensorId = firstBitIndex + i*8 + j
            output.append({'SensorId':j, 'Responding':timeOps.time()})
            #print 'responding', j 
        #send output as necessary
    #print 'done parsing'
    return output

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
        print parseBinarySensorPacket(data)
        #print list(map(parseBinarySensorPacket,data)), '\t', address
    (data, address) = sock.recvfrom(1024)
    addresses.add(address)
