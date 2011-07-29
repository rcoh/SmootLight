#!/usr/bin/env python
import util.TimeOps as timeOps
import socket
import time
import threading, Queue
from os import system as run

HOST = ''
PORT = 3344
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
q=Queue.Queue()
class ThreadClass(threading.Thread):
  voice = "female1"
  MPERIOD = 1
  def __init__(self,q):
    threading.Thread.__init__(self)
    self.q = q

  def say(self,text):
    print text
    run('espeak -v %s -w tmp.wav "%s"'%(self.voice,text))
    run('aplay -q tmp.wav')


  def run(self):
   while True:
    datum = self.q.get()
    id = datum['SensorId']
    respt = datum['Responding']
    diff=time.time()-respt
    if not diff > self.MPERIOD:
      if id == 25:
          self.say("Warning, collision imminent")
      elif id == 26:
          self.say("Danger, perimeter breached")
    self.q.task_done()
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
            output.append({'SensorId':j, 'Responding':time.time()})
            #print 'responding', j 
        #send output as necessary
    #print 'done parsing'
    return output

(data,address) = sock.recvfrom(1024)
lastt = time.time()
c=0
addresses = set()

t=ThreadClass(q)
t.setDaemon(True)
t.start()

while data:
    c+=1
    dt =( time.time()-lastt )
    if dt > 1:
#        print c/dt, " packets per second from", len(addresses), "unique addresses"
        c = 0
        addresses = set()
        lastt = time.time()
    if 0:#address[-1]=='7':
        print parseBinarySensorPacket(data)
        #print list(map(parseBinarySensorPacket,data)), '\t', address
    elif 1:
        for datum in parseBinarySensorPacket(data):
            if type(datum) is dict and datum.has_key('SensorId'):
               q.put(datum)
               print 'putting'
    (data, address) = sock.recvfrom(1024)
    addresses.add(address)

