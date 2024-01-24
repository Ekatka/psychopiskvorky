import socket
import pickle

class Network:
    def __init__(self):
        self.players = 0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5555
        self.host = "localhost"
        self.numOfPlayer = int(self.connect())

        pass

    def getNumOfP(self):
        return self.numOfPlayer

    def get_players(self):
        return self.players

    def connect(self):
        # self.players+=1
        try:
            self.s.connect((self.host, self.port))
            return self.s.recv(2048*4).decode()
        except:
            print('AAAAAAAAAAAAAAAAAAAAAAAA!')

    def send(self, action):

        try:
            if isinstance(action, list):
                action = ' '.join(map(str, action))
            self.s.send(str.encode(action))
            data = self.s.recv(2048*4)
            return pickle.loads(data)
        except socket.error as e:
            print(e)
