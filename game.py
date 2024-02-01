class Game():
    def __init__(self):

        self.p1Went = False #zahrál první hráč
        self.p2Went = False #zahrál druhý hráč
        self.ready = False #zda jsou oba hráči připojeni
        self.guessMove = [0, 0] #poličko, které jeden z hráčů vybral
        self.fullMoves = [[], []] #seznam políček každého z hráčů
        self.guessed = False #zda se uhodlo políčko
        self.turn = 0 #který hráč je na tahu
        self.winner = None #kdo vyhrál danou hru
        self.winningDirection = [] #směr ve kterém mám hledat sousední políčka
        self.winningPlacement = [] #krajní políčko, co se nachází ve vítězné n-tici
        self.wrongGuess = 0 #políčko, které jeden z hráčů hádal
        self.gameOver = False #zda se dohrálo

    def getTurn(self):
        return self.turn

    def getPlayerMove(self, p):
        return self.guessMove[p]

    def play(self, player, move):
        #monitoruje, zda již odehráli oba hráči
        self.guessMove[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
        if self.p1Went and self.p2Went:
            self.updateMoves()

    def bothChose(self):
        #zda zahráli oba hráči
        return self.p1Went and self.p2Went
    def connected(self):
        return self.ready


    def updateMoves(self):

        #zahrané kroky
        p1 = self.guessMove[0]
        p2 = self.guessMove[1]

        #políčko bylo uhodnuto, v tom případě přidáme políčko do seznamu druhého hráče
        if p1 == p2:
            #symbolPlayer je ten, komu si přidalo políčko v daném tahu
            symbolPlayer = not self.turn
            self.fullMoves[not self.turn].append(p1)
            self.guessed = True
            self.wrongGuess = 0

        else:
            symbolPlayer = self.turn
            self.fullMoves[self.turn].append(self.guessMove[self.turn])
            self.guessed = False
        #kontrolujeme, zda jeden z hráčů vyhrál
        self.check_win_conditions(self.guessMove[self.turn][0], self.guessMove[self.turn][1], symbolPlayer)
        #políčko nebylo uhodnuto, zobrazíme, kam druhý hráč hádal
        if not self.guessed:
            self.turn = not self.turn
            self.wrongGuess = self.guessMove[self.turn]



    def resetWent(self):

        self.p1Went = False
        self.p2Went = False
        self.guessMove[0] = 0
        self.guessMove[1] = 0




    def resetGame(self):
        self.resetWent()
        self.fullMoves = [[], []]
        self.gameOver = False
        self.turn = not self.winner
        self.wrongGuess = 0



    def check_win_conditions(self, last_x, last_y, player):
        """

        :param last_x: souřadnice x posledního umístěného symbolu
        :param last_y: souřadnice y posledního umístěného symbolu
        :param player: hráč 0 nebo 1
        """
        #možné směry, díváme se v obou směrech(nahoru a dolů, vlevo a vpravo, ...)
        bordering_coordinates = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for x, y in bordering_coordinates:
            #počet políček v řadě
            count = 0
            new_x = last_x + x
            new_y = last_y + y
            #jdeme nejvýš 4 políčka v jednom směru, například nahoru, pak jdu nejvýš 4krát dolů
            for _ in range(4):
                if [new_x, new_y] in self.fullMoves[player]:
                    new_x = new_x + x
                    new_y = new_y + y
                    count += 1
                else:
                    break
            new_x = last_x - x
            new_y = last_y - y
            for _ in range(4):
                if [new_x, new_y] in self.fullMoves[player]:
                    new_x = new_x - x
                    new_y = new_y - y
                    count += 1
                else:
                    break
            #máme aspoň 5 políček v řadě, takže daný hráč vyhrál
            if count >= 4:
                self.winningDirection = [x, y]
                self.winningPlacement = [new_x, new_y]
                self.winner = player
                self.gameOver = True

