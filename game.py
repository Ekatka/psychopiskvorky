class Game():
    def __init__(self):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.guessMove = [0, 0]
        self.fullMoves = [[], []]
        self.guessed = False
        self.turn = 0
        self.winner = None
        self.winningDirection = []
        self.winningPlacement = []
        self.wrongGuess = 0
        self.waiting = False
        '''
        
        '''

    def getTurn(self):
        return self.turn

    def getPlayerMove(self, p):

        return self.guessMove[p]

    def play(self, player, move):
        self.guessMove[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
        if self.p1Went and self.p2Went:
            self.waiting = False
            self.updateMoves()

        else:
            self.waiting = True

    def connected(self):
        return self.ready

    def bothChose(self):
        return self.guessMove[0] != 0 and self.guessMove[1] != 0

    def updateMoves(self):
        """

        :param turn: who is the main player, 1, 0
        :return:
        """

        p1 = self.guessMove[0]
        p2 = self.guessMove[1]

        if p1 == p2:
            self.fullMoves[not self.turn].append(p1)
            self.guessed = True

        else:
            self.fullMoves[self.turn].append(self.guessMove[self.turn])

        if not self.guessed:
            self.turn = not self.turn
            self.wrongGuess = self.guessMove[self.turn]

    def resetWent(self):

        self.p1Went = False
        self.p2Went = False
        self.guessMove[0] = 0
        self.guessMove[1] = 0
        self.waiting = False
        # self.bothChose = False

    def resetGame(self):
        self.fullMoves = [[], []]

    def check_win_conditions(self, last_x, last_y, player):
        """

        :param last_x: last added x, and y by which player
        :param last_y:
        :param player: [0, 1]
        :return:
        """

        bordering_coordinates = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for x, y in bordering_coordinates:
            count = 0
            new_x = last_x + x
            new_y = last_y + y
            for _ in range(4):
                if (new_x, new_y) in self.fullMoves[player]:
                    new_x = new_x + x
                    new_y = new_y + y
                    count += 1
                else:
                    break
            new_x = last_x - x
            new_y = last_y - y
            for _ in range(4):
                if (new_x, new_y) in self.fullMoves[player]:
                    new_x = new_x - x
                    new_y = new_y - y
                    count += 1
                else:
                    break

            if count >= 4:
                self.winningDirection = [x, y]
                self.winningPlacement = [new_x, new_y]
                self.winner = player
        self.winningDirection = False
        self.winningPlacement = False
