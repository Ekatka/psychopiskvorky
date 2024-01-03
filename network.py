import socket
import pickle

class Network:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 9999
        self.host = "localhost"
        self.numOfPlayer = int(self.connect())

    def getNumOfP(self):
        return self.numOfPlayer

    def connect(self):
        try:
            self.s.connect((self.host, self.port))
            return self.s.recv(2048).decode()
        except:
            print('AAAAAAAAAAAAAAAAAAAAAAAA!')

    def send(self, action):
        try:
            self.s.send(str.encode(action))
            return pickle.loads(self.s.recv(2048*2))
        except socket.error as e:
            print(e)
