#!/usr/bin/env python

import socket
from time import time as xxxtime
import threading, Queue
from os import system as run
#from numpy import abs,maximum



from socket import socket,AF_INET,SOCK_DGRAM
from numpy import ravel,minimum,maximum,zeros,random

xmit = zeros(174, 'ubyte')
xmit[:8], xmit[20:24] = [4, 1, 220, 74, 1, 0, 8, 1], [150, 0, 255, 15]

def connect(ip, port=6038):
   sock = socket(AF_INET, SOCK_DGRAM, 0)
   sock.connect((ip, port))
   return sock

def display(data, sock, chan=1):
   xmit[16], xmit[24:] = chan, minimum(maximum(256 * ravel(data), 0), 255)
   sock.sendall(xmit)


sockets = [connect('10.32.0.{0}'.format(i)) for i in ['47','48','49','50']]



def unnecessary():
  for s in sockets:
      display(0, s)
      display(0, s, 2)

  from time import sleep as wakeup
  wakeup(1)

  for s in sockets:
    display(50*[1,0,0],s)
    display(1,s,2)

buffer = zeros((100,4,3))
def doWithID(id):
   global buffer
   buffer *= .9
   buffer[int(id*12.5):int(id*12.5)+13] = random.rand(13*4*3).reshape((-1,4,3))
#  scaledx = x - min(x)
#  scaledx *= 8 / max(x)
#  scaledx -= .5
#  return [255,255,255] * maximum(1 - abs(lastid-scaledx)[:,None], 0)


q=Queue.Queue()

class ConsumerClass(threading.Thread):
  MPERIOD = 1
  def __init__(self,q):
    threading.Thread.__init__(self)
    self.q = q
    self.lastid = None

  def run(self):
   while True:
    datum = self.q.get()
    id = datum['SensorId']
    respt = datum['Responding']
    #diff=xxxtime()-respt
    #if not diff > self.MPERIOD:
    doWithID(id)
    self.q.task_done()

class ProducerClass(threading.Thread):
  def __init__(self,q):
    threading.Thread.__init__(self)
    self.q = q
    HOST = ''
    PORT = 3344
    self.sock = socket(AF_INET, SOCK_DGRAM)
    self.sock.bind((HOST, PORT))

    (self.data,self.address) = self.sock.recvfrom(1024)
    #self.lastt = xxxtime()
    self.addresses = set()

    self.t=ConsumerClass(self.q)
    self.t.setDaemon(True)
    self.t.start()

  def getLast(self):
    return self.t.lastid

  def run(self):
    c=0
    while self.data:
        c+=1
        #dt =( xxxtime()-self.lastt )
        if True: #dt > 1:
    #        print c/dt, " packets per second from", len(addresses), "unique addresses"
            c = 0
            self.addresses = set()
            #self.lastt = xxxtime()
        if 0:#address[-1]=='7':
            print self.parseBinarySensorPacket(self.data)
            #print list(map(parseBinarySensorPacket,data)), '\t', address
        elif 1:
            for datum in self.parseBinarySensorPacket(self.data):
                if type(datum) is dict and datum.has_key('SensorId'):
                   self.q.put(datum)
    #               print 'putting'
        (self.data, self.address) = self.sock.recvfrom(1024)
        self.addresses.add(self.address)

  def grabBits(self,p):
    return bin(ord(p))[2:].zfill(8) 

  def parseBinarySensorPacket(self,p):#, firstBitIndex):
    #print 'starting to parse'
    if len(p) != 5:
        print 'bad length'
    packet = []
    for i,hexByte in enumerate(p):
        bits = self.grabBits(hexByte)
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
            output.append({'SensorId':j, 'Responding':0})#xxxtime()})
            #print 'responding', j 
        #send output as necessary
    #print 'done parsing'
    return output

p=ProducerClass(q)
p.setDaemon(True)
p.start()
print "debug-module loaded"

#def display(x,y,t):
#  lastid = p.getLast()
#  scaledx = x - min(x)
#  scaledx *= 8 / max(x)
#  scaledx -= .5
#  return [255,255,255] * maximum(1 - abs(lastid-scaledx)[:,None], 0)

while 1:
   from time import sleep as xxxxxxx
   xxxxxxx(.05)
   global buffer
   buffer *= .9
   display(buffer[:50, 0], sockets[0], 1)
   display(buffer[:50, 1], sockets[0], 2)
   display(buffer[:50, 2], sockets[1], 1)
   display(buffer[:50, 3], sockets[1], 2)
   display(buffer[50:, 0], sockets[2], 1)
   display(buffer[50:, 1], sockets[2], 2)
   display(buffer[50:, 2], sockets[3], 1)
   display(buffer[50:, 3], sockets[3], 2)

