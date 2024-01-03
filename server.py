import socket
from _thread import *
import pickle
from game import Game

server = "localhost"
port = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)



print('Server spuštěn, čekám na připojení')

def ThreadedClient(conn, numOfPlayer, game):
    conn.send(str.encode(str(numOfPlayer)))
    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                break
            else:
                if data == 'resetWent':
                    game.resetWent()
                elif data == 'resetGame':
                    game.resetGame()
                elif data != 'get':
                    game.play(numOfPlayer, data)

                conn.sendall(pickle.dumps(game))


        except:
            break

    print("Ztráta připojení")
    conn.close()

s.listen(2)
numOfPlayers = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    numOfPlayers +=1
    if numOfPlayers == 1:
        game = Game()
    else:
        game.ready = True

        start_new_thread(ThreadedClient(conn, numOfPlayers, game))






