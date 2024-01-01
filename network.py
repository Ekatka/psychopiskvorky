import socket
import pickle

class Network:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 9999
        self.host = "172.18.0.1"
        self.connection = self.connect()

    def connect(self):
        try:
            self.s.connect((self.port, self.host))
            return self.s.recv(2048).decode()
        except:
            pass

    def send(self, state):
        data = pickle.dumps(state)
        self.s.send(data)