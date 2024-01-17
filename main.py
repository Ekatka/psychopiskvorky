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


    def get_cell_size(self):
        return int(self.cell_size)

    def get_grid_size(self):
        return int(self.grid_size)

    def get_window_size(self):
        return int(self.window_size)

    def on_draw(self):
        arcade.start_render()
        draw_grid(self.game, self, self.state)
        if self.game_over:
            draw_end_game(self.game, self)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        cell_x = x // self.cell_size
        cell_y = y // self.cell_size
        self.newMove = True

        self.moves = [cell_x, cell_y]

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
        player = self.player  # Assuming self.player is set to the current player's number

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
    draw_grid(game, playground)

    x = game.winningPlacement[0]
    y = game.winningPlacement[1]

    cur_x = x + game.winningDirection[0]
    cur_y = y + game.winningDirection[1]

    if (cur_x, cur_y) in game.symbols[game.winner]:
        while (cur_x, cur_y) in game.symbols[game.winner]:
            cur_x = cur_x + game.winningDirection[0]
            cur_y = cur_y + game.winningDirection[1]
        print(game.winningDirection)
        start_x = (x + game.winningDirection[0]) * playground.get_cell_size + playground.get_cell_size // 2
        start_y = (y + game.winningDirection[1]) * playground.get_cell_size + playground.get_cell_size // 2
        end_x = (cur_x - game.winningDirection[0]) * playground.get_cell_size + playground.get_cell_size // 2
        end_y = (cur_y - game.winningDirection[1]) * playground.get_cell_size + playground.get_cell_size // 2
        arcade.draw_line(start_x, start_y, end_x, end_y, color=arcade.color.RED, line_width=3)


def draw_grid(game, playground, state):
    grid_offset = 100

    for x in range(playground.get_grid_size()+1):
        start_x = x * playground.get_cell_size() + grid_offset/2
        end_x = x * playground.get_cell_size() + grid_offset/2
        start_y = grid_offset
        end_y = playground.get_window_size()
        arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.BLACK)

    for y in range(playground.get_grid_size()+1):
        start_x = grid_offset/2
        end_x = playground.get_window_size() - grid_offset/2
        start_y = y * playground.get_cell_size() + grid_offset
        # end_y = y * playground.get_cell_size()
        end_y = start_y
        arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.BLACK)

    for symbol in game.fullMoves[0]:
        # x_cor = symbol[0] * self.cell_size
        # y_cor = symbol[1] * self.cell_size
        x_cor = symbol[0] * playground.get_cell_size() + playground.get_cell_size() / 2
        y_cor = symbol[1] * playground.get_cell_size() + playground.get_cell_size() / 2
        arcade.draw_text('O', x_cor, y_cor, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
    for symbol in game.fullMoves[1]:
        x_cor = symbol[0] * playground.get_cell_size() + playground.get_cell_size() / 2
        y_cor = symbol[1] * playground.get_cell_size() + playground.get_cell_size() / 2
        arcade.draw_text('X', x_cor, y_cor, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

    if game.p1Went and game.p2Went:
        x_cor = game.wrongGuess[0] * playground.get_cell_size() + playground.get_cell_size() / 2
        y_cor = game.wrongGuess[1] * playground.get_cell_size() + playground.get_cell_size() / 2
        arcade.draw_text('.', x_cor, y_cor, arcade.color.RED, font_size=20, anchor_x='center', anchor_y="center")

    if state == 0:
        text = 'Initializing'
    elif state == 1:
        text = 'Select a square'
    elif state == 2:
        text = 'Select a square, the opponent has already chosen one'
    elif state == 3:
        text = 'Waiting for the opponents move'
    elif state ==4:
        text = 'Guess a square that the opponent will play'
    elif state == 5:
        text = 'Guess a square, the opponet has already chosen one'
    elif state == 6:
        text = 'Waiting for the opponents move'

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
    # while gameOn:
    #     try:
    #         game = n.send('get')
    #         playground.game = game
    #
    #
    #     except:
    #
    #         # gameOn = False
    #         print("Hra nejde načíst")
    #         break
        #
        # turn = game.getTurn()
        # if turn == player:
        #     print('Your turn')
        #     if game.guess[player] == 0 and game.quess[int(not player)] == 0:
        #         state = 1
        #     elif game.guess[player] == 0 and game.quess[int(not player)] != 0:
        #         state = 2
        #     elif game.guess[player] != 0 and game.quess[int(not player)] == 0:
        #         state = 3
        #
        # else:
        #     print('Wait for the opponent')
        #     if game.guess[player] == 0 and game.quess[int(not player)] == 0:
        #         state = 4
        #     elif game.guess[player] == 0 and game.quess[int(not player)] != 0:
        #         state = 5
        #     elif game.guess[player] != 0 and game.quess[int(not player)] == 0:
        #         state = 6
        # playground = Playground(state, title=f'You are a player {player}', game=game)

        # if playground.newMove():
        #     while not game.bothChose():
        #         playground.symbols = game.fullMoves

    # game = Playground(title='Player 1')


if __name__ == "__main__":
    main()

"""
Co to zatim dela, umi se pripojit jeden hrac, a ten bude dostavat game. 
Game umi prijmout souradnice, ale to neni implementovany
Pak umim nakreslit X a O, a cervenou tecku, kdyz si druhy hrac tipne spatne.
Musim pridat text, co rika, kdo kdy hraje a pripojit druheho hrace. 

TODO zadavat user click do game. vymyslet jak 
"""
"""
state 1, jsem umistujici symbol hrac, jeste jsem si nikdo nevybral, 'vyberte si policko'
state 2, jsem umistujici symbol hrac, jeste jsem si nevybral, ale souper jo, 'souper uz odehral'
state 3, jsem umistujici symbol hrac, uz si vybral, 'ceka se na druheho hrace'
state 4, jsem hadajici hrac, jeste si nekdo nebral, 'hadejte, co zahrajej souper'
state 5, jsem hadajici hrac, souper uz hral, 'souper uz odehral'
state 6, jsem hadajici hrac, uz si vybral, 'ceja se na soupere'
"""
