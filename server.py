import socket
from _thread import *
import pickle
from game import Game

# uživatel zadá svoji IP adresu, pak se čeká na připojení
server = input('Enter your IP address')
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)
    exit()

print('Server is running, waiting for connection')


def ThreadedClient(conn, numOfPlayer, game):
    conn.send(str.encode(str(numOfPlayer)))
    while True:
        try:
            # pro každého z klientu kontrolujeme data
            data = conn.recv(2048).decode()
            if not data:
                break
            else:
                # kontrolujeme obsah dat, připadně provedeme přikazy
                if data == 'resetWent':
                    game.resetWent()
                elif data == 'resetGame':
                    game.resetGame()
                # když data nejsou get ani jiný z příkazů, tak to musí být zahraný krok
                elif data != 'get':
                    data = data.split(' ')
                    data = [int(i) for i in data]
                    game.play(numOfPlayer, data)
                # vrátíme současnou hru
                conn.sendall(pickle.dumps(game))


        except:
            break

    game.ready = False
    game.gameOver = True
    conn.sendall(pickle.dumps(game))
    conn.close()


s.listen(2)
numOfPlayers = 0
while True:
    # Čekáme na dvě připojení
    if numOfPlayers < 2:
        conn, addr = s.accept()
        print("Connected to:", addr)

        if numOfPlayers == 0:
            numOfPlayers += 1
            game = Game()

        else:
            game.ready = True
            numOfPlayers += 1

        start_new_thread(ThreadedClient, (conn, numOfPlayers - 1, game))
