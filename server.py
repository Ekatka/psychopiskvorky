import socket
from _thread import *
import pickle
from game import Game

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
except socket.error as e:
    print(e)
    # exit()



print('Server is running, waiting for connection')

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
                    print('AAAAAAAAAA')
                    print(game.fullMoves)
                elif data != 'get':
                    data = data.split(' ')
                    data = [int(i) for i in data]
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


    if numOfPlayers == 0:
        numOfPlayers += 1
        game = Game()

    else:
        game.ready = True
        numOfPlayers +=1

    print(game)

    start_new_thread(ThreadedClient, (conn, numOfPlayers-1, game))







