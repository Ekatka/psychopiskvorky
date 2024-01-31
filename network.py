import socket
import pickle

class Network:
    def __init__(self):
        self.players = 0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5555
        self.host = input('Enter server IP address')
        self.numOfPlayer = int(self.connect())


    def getNumOfP(self):
        return self.numOfPlayer

    def connect(self):
        #funkce na připojení
        try:
            self.s.connect((self.host, self.port))
            return self.s.recv(2048*4).decode()
        except Exception as e:
            raise ConnectionError("Failed to connect to the server") from e

    def send(self, action):
        #odeslání dat
        try:
            if isinstance(action, list):
                action = ' '.join(map(str, action))
            self.s.send(str.encode(action))
            data = self.s.recv(2048*4)
            return pickle.loads(data)
        except socket.error as e:
            print(e)
