import time as clock
def time():
    return clock.time()*1000 #all times in MS

class Stopwatch:
    def __init__(self):
        self.running = False
        self.startTime = -1
        self.stopTime = -1
    def start(self):
        self.startTime = time()
        self.running = True
    def elapsed(self):
        if self.running:
            return time()-self.startTime
        else:
            return self.stopTime - self.startTime
    def stop(self):
        self.stopTime = time()
        self.running = False
