import socket
import time
class IDBClient:

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self. client_socket.connect(('localhost', 12345))
        print self.client_socket.recv(1024)

    def sendRequest(self, msg):
        self.client_socket.send(msg)
        resp = self.client_socket.recv(1024)
        print resp
        return resp

    def setObserverForObject(self, distname):
        self.client_socket.send("0x8-MAINCONSOLE-"+distname)
        self.resp = self.client_socket.recv(1024)
        while self.resp.find("-0") != -1:
            self.client_socket.send("0x8-MAINCONSOLE-"+distname)
            self.resp = self.receive()
            print self.resp.split("-")[2]
            time.sleep(0.2)
        return True       

    def receive(self):
        resp = self.client_socket.recv(1024)
        return resp

