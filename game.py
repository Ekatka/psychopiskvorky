class Game():
    def __init__(self):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.guessMove = [0, 0]
        self.fullMoves = [[], []]
        self.guessed = False
        self.turn = 0


    def getPlayerMove(self, p):

        return self.guessMove[p]
    def player(self, player, move):
         self.guessMove[0] = move
         if player == 0:
             self.p1Went = True
         else:
             self.p2Went = True
    def connected(self):
        return self.ready

    def bothChose(self):
        return self.p1Went and self.p2Went

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

    def resetWent(self):
        if not self.guessed:
            self.turn = not self.turn
        self.p1Went = False
        self.p2Went = False




