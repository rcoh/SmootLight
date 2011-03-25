from operationscore.Renderer import *
import util.TimeOps as timeops
import util.ComponentRegistry as compReg
import threading, socket, re, struct, hashlib, json

class WebsocketRenderer(Renderer):
    """Renders frame data over a websocket.
        Specify: Hostname -- the hostname of the webserver providing the containing page
        Page: Static page to serve (if using builtin webserver)
        SourcePort: Port from which static page is serverd
        Port: Websocket listen port
    """
    
    def initRenderer(self):
        self.hostname = self.argDict['Hostname']
        self.port = int(self.argDict['Port'])
        
        if 'SourcePort' in self.argDict:
            self.orig_port = int(self.argDict['SourcePort'])
        else:
            self.orig_port = compReg.getComponent('Webserver').getPort()
        
        self.clients = []
        self.clients_lock = threading.Lock()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
        self.sock.listen(1)
        
        self.connection_thread = threading.Thread(target=self.handle_connections)
        self.connection_thread.daemon = True
        self.connection_thread.start()
            
    def handle_connections(self):
        while True:
            client, addr = self.sock.accept()
            print 'Accepted websocket connection from %s' % str(addr)
            header = ''
            while not re.search("\r?\n\r?\n.{8}", header): # Receive headers + 8 bytes data
                header += client.recv(1024)
            
            key1 = re.search("Sec-WebSocket-Key1: (.*)$", header, re.M).group(1)
            key2 = re.search("Sec-WebSocket-Key2: (.*)$", header, re.M).group(1)

            data = header[-8:]

            key1n = int(re.sub("[^\d]", '', key1))
            key1ns = key1.count(' ')
            n1 = key1n // key1ns

            key2n = int(re.sub("[^\d]", '', key2))
            key2ns = key2.count(' ')
            n2 = key2n // key2ns

            s = struct.pack("!II", n1, n2) + data
            respkey = hashlib.md5(s).digest()
            
            if self.orig_port == 80:
                origin = 'http://'+self.hostname
            else:
                origin = 'http://'+self.hostname+':'+str(self.orig_port)
            
            resp = \
                "HTTP/1.1 101 Web Socket Protocol Handshake\r\n" + \
                "Upgrade: WebSocket\r\n" + \
                "Connection: Upgrade\r\n" + \
                "Sec-WebSocket-Origin:"+ origin + "\r\n" + \
                "Sec-WebSocket-Location: ws://"+self.hostname+":"+ \
                    str(self.port)+"/\r\n" + \
                "Sec-WebSocket-Protocol: ledweb\r\n\r\n" + \
                respkey + "\r\n"

            client.send(resp)
            self.clients_lock.acquire()
            self.clients.append(client)
            self.clients_lock.release()
    
    def render(self, lightSystem, currentTime=timeops.time()):
        json_frame = [0]*len(lightSystem)
        i = 0
        for (loc, c) in lightSystem:
            if all(c < 0.05):
                continue
            cs = 'rgb({0},{1},{2})'.format(*map(int, c*255))
            json_frame[i] = (map(int, loc), cs)
            i += 1

        json_frame = json_frame[0:i]
        size = compReg.getComponent('Screen').size
        
        json_data = json.dumps(dict(status='ok', size=map(int, size), frame=json_frame))
        self.client_push(json_data)
        
    def client_push(self, data):
        self.clients_lock.acquire()
        dead_clients = []
        for i in range(len(self.clients)):
            try:
                self.clients[i].send("\x00")
                self.clients[i].send(data)
                self.clients[i].send("\xff")
            except socket.error:
                dead_clients.append(i)
        
        for i in range(len(dead_clients)):
            self.close_sock(self.clients[dead_clients[i]-i])
            del self.clients[dead_clients[i]-i]
        self.clients_lock.release()
    
    def close_sock(self, s):
        try:
            c.shutdown(socket.SHUT_RDWR)
            c.close()
        except Exception:
            pass
        
