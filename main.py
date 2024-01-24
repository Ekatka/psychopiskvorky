import arcade
from network import Network


class Playground(arcade.Window):
    def __init__(self, player, title, game, network, cell_size=30, grid_size=25):
        self.player = player
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.window_size = self.grid_size * self.cell_size + 100
        super().__init__(self.window_size, self.window_size, title)
        arcade.set_background_color(arcade.color.WHITE)
        # self.added_symbols = []
        self.game = game
        self.game_over = False
        self.moves = []
        self.newMove = False
        self.n = network
        self.state = 0
        self.grid_offset = 100
        self.waiting = False

    def get_cell_size(self):
        return int(self.cell_size)

    def get_grid_size(self):
        return int(self.grid_size)

    def get_window_size(self):
        return int(self.window_size)

    def on_draw(self):
        arcade.start_render()
        self.game = self.n.send('get')
        if self.game.gameOver:
            draw_end_game(self.game, self)
        else:
            draw_grid(self.game, self, self.state)


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        print('waiting',self.waiting)
        print('game ready', self.game.ready)

        if self.game.guessMove == [0,0] or self.game.guessMove[not self.player] != 0:
            self.waiting = False

        if not self.waiting and self.game.ready:
            cell_x = (x - self.grid_offset // 2) // self.cell_size
            cell_y = (y - self.grid_offset) // self.cell_size
            self.newMove = True

            self.moves = [cell_x, cell_y]
            print(self.moves)
            # self.game.guessMove[self.player] = self.moves
            # print(self.game.guessMove)
            self.game = self.n.send(self.moves)
            if self.game.bothChose():
                # self.game.updateMoves()
                self.waiting = False
                self.n.send('resetWent')



        # direction, last_elements = self.check_win_conditions(cell_x, cell_y, 'X')
        # if last_elements:
        #     self.game_over = True
        #     self.draw_end_game(direction, last_elements)

    def get_moves(self):
        return self.moves

    def update(self, delta_time: float):
        self.game = self.n.send('get')
        self.manage_states()

    def manage_states(self):
        turn = self.game.getTurn()
        player = self.player
        if not self.game.ready:
            self.state = 7
        elif self.game.gameOver == True:
            self.state = 8


        else:

            if turn == player:
                # print('Your turn')
                if self.game.guessMove[player] == 0 and self.game.guessMove[int(not player)] == 0:
                    self.state = 1
                elif self.game.guessMove[player] == 0 and self.game.guessMove[int(not player)] != 0:
                    self.state = 2
                elif self.game.guessMove[player] != 0 and self.game.guessMove[int(not player)] == 0:
                    self.state = 3
            else:
                # print('Wait for the opponent')
                if self.game.guessMove[player] == 0 and self.game.guessMove[int(not player)] == 0:
                    self.state = 4
                elif self.game.guessMove[player] == 0 and self.game.guessMove[int(not player)] != 0:
                    self.state = 5
                elif self.game.guessMove[player] != 0 and self.game.guessMove[int(not player)] == 0:
                    self.state = 6


def draw_end_game(game, playground):
    grid_offset = 100
    draw_grid(game, playground, state=8)

    x = game.winningPlacement[0]
    y = game.winningPlacement[1]

    cur_x = x + game.winningDirection[0]
    cur_y = y + game.winningDirection[1]

    if (cur_x, cur_y) in game.fullMoves[game.winner]:
        while (cur_x, cur_y) in game.fullMoves[game.winner]:
            cur_x = cur_x + game.winningDirection[0]
            cur_y = cur_y + game.winningDirection[1]
        print(game.winningDirection)
        start_x = (x + game.winningDirection[0]) * playground.get_cell_size + playground.get_cell_size // 2 + grid_offset // 2
        start_y = (y + game.winningDirection[1]) * playground.get_cell_size + playground.get_cell_size // 2 + grid_offset
        end_x = (cur_x - game.winningDirection[0]) * playground.get_cell_size + playground.get_cell_size // 2 + grid_offset // 2
        end_y = (cur_y - game.winningDirection[1]) * playground.get_cell_size + playground.get_cell_size // 2 + grid_offset
        arcade.draw_line(start_x, start_y, end_x, end_y, color=arcade.color.RED, line_width=3)


def draw_grid(game, playground, state):
    # game = network.send('get')
    grid_offset = 100

    for x in range(playground.get_grid_size() + 1):
        start_x = x * playground.get_cell_size() + grid_offset // 2
        end_x = x * playground.get_cell_size() + grid_offset // 2
        start_y = grid_offset
        end_y = playground.get_window_size()
        arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.BLACK)

    for y in range(playground.get_grid_size() + 1):
        start_x = grid_offset // 2
        end_x = playground.get_window_size() - grid_offset // 2
        start_y = y * playground.get_cell_size() + grid_offset
        # end_y = y * playground.get_cell_size()
        end_y = start_y
        arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.BLACK)

    for symbol in game.fullMoves[0]:
        # x_cor = symbol[0] * self.cell_size
        # y_cor = symbol[1] * self.cell_size
        x_cor = symbol[0] * playground.get_cell_size() + playground.get_cell_size() // 2 + grid_offset // 2
        y_cor = symbol[1] * playground.get_cell_size() + playground.get_cell_size() // 2 + grid_offset
        arcade.draw_text('O', x_cor, y_cor, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
    for symbol in game.fullMoves[1]:
        x_cor = symbol[0] * playground.get_cell_size() + playground.get_cell_size() // 2 + grid_offset // 2
        y_cor = symbol[1] * playground.get_cell_size() + playground.get_cell_size() // 2+ grid_offset
        arcade.draw_text('X', x_cor, y_cor, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
    if game.wrongGuess != 0:
        x_cor = game.wrongGuess[0] * playground.get_cell_size() + playground.get_cell_size() // 2 + grid_offset // 2
        y_cor = game.wrongGuess[1] * playground.get_cell_size() + playground.get_cell_size() // 2 + grid_offset + 22
        arcade.draw_text('.', x_cor, y_cor, arcade.color.RED, font_size=50, anchor_x='center', anchor_y="center")

    if state == 0:
        text = 'Initializing'
    elif state == 1:
        text = 'Select a square'
    elif state == 2:
        text = 'Select a square, the opponent has already chosen one'
    elif state == 3:
        text = 'Waiting for the opponents move'
    elif state == 4:
        text = 'Guess a square that the opponent will play'
    elif state == 5:
        text = 'Guess a square, the opponent has already chosen one'
    elif state == 6:
        text = 'Waiting for the opponents move'
    elif state == 7:
        text = 'Waiting for the opponent to connect'
    elif state == 8:
        text = 'Game over'

    text_x = playground.width / 2
    text_y = grid_offset - 50
    arcade.draw_text(text, text_x, text_y, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")


def main():
    n = Network()
    gameOn = True
    player = n.getNumOfP()
    print(player)

    try:
        game = n.send('get')

        print(game)
    except:
        # gameOn = False
        print("Cannot find the game")
        exit()

    playground = Playground(player, title=f'You are a player {player}', game=game, network=n)
    arcade.run()


if __name__ == "__main__":
    main()

"""
opravit uhodnuti,  
nastavit hezci krizky?

"""