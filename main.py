import arcade
from network import Network


class Playground(arcade.Window):
    def __init__(self, player, title, game, network, cell_size=30, grid_size=25, grid_offset=100):
        '''
        :param player: číslo hráče
        :param title: text v záhlaví
        :param game: objekt hry
        :param network: objekt síťe
        :param cell_size: rozměr políčka
        :param grid_size: počet políček
        '''
        self.player = player
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.window_size = self.grid_size * self.cell_size + grid_offset
        super().__init__(self.window_size, self.window_size, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.game = game
        self.move = []  # jeden tah
        self.n = network
        self.state = 0  # stav hry, podle něj se vypisuje text pod hracím oknem
        self.grid_offset = grid_offset
        self.waiting = False

    def get_cell_size(self):
        return int(self.cell_size)

    def get_grid_size(self):
        return int(self.grid_size)

    def get_window_size(self):
        return int(self.window_size)

    def get_grid_offset(self):
        return int(self.grid_offset)

    def on_draw(self):

        arcade.start_render()
        self.game = self.n.send('get')
        # kontroluju, jestli se již dohrálo, pokud ano, kreslím jiné hrací pole
        if self.game.gameOver and self.game.ready:
            draw_end_game(self.game, self)
        else:
            draw_grid(self.game, self, self.state)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):

        if self.game.gameOver:
            # dohrálo se a po kliknutí začne nová hra
            self.n.send('resetGame')

        else:
            # waiting blokuje vybrání jiného políčka po zahrání
            if self.game.guessMove == [0, 0] or self.game.guessMove[not self.player] != 0:
                self.waiting = False
            # souřadnice se upraví a převedou se na souřadnice v tabulce
            if not self.waiting and self.game.ready:
                cell_x = (x - self.grid_offset // 2) // self.cell_size
                cell_y = (y - self.grid_offset) // self.cell_size
                # kontroluju, že dané políčko je prázdné a je v rozshahu tabulky
                if not [cell_x, cell_y] in self.game.fullMoves[0] or [cell_x, cell_y] in self.game.fullMoves[1]:
                    if cell_x >= 0 and cell_x < 25 and cell_y >= 0 and cell_y < 25:
                        self.move = [cell_x, cell_y]
                        self.game = self.n.send(self.move)
                        # když si vybrali oba, vynuluju kroky
                        if self.game.bothChose():
                            self.waiting = False
                            self.n.send('resetWent')



    def update(self, delta_time: float):
        self.game = self.n.send('get')
        self.manage_states()

    def manage_states(self):
        turn = self.game.getTurn()
        player = self.player
        #všechna políčka jsou zaplněná
        if len(self.game.fullMoves[0]) + len(self.game.fullMoves[1]) == self.grid_size ** 2:
            self.state = 10
            self.game.gameOver = True
        # nejsou připojeni oba hráči, ale hra už začala
        elif not self.game.ready and self.game.gameOver:
            self.state = 9
        # nejsou připojeni oba hřáči
        elif not self.game.ready:
            self.state = 7
        # jeden z hráčů vyhrál
        elif self.game.gameOver == True and self.game.ready:
            self.state = 8

        else:

            if turn == player:
                # možné stavy toho, kdo už odehrál, podle nich se pak generuje text
                if self.game.guessMove[player] == 0 and self.game.guessMove[int(not player)] == 0:
                    self.state = 1
                elif self.game.guessMove[player] == 0 and self.game.guessMove[int(not player)] != 0:
                    self.state = 2
                elif self.game.guessMove[player] != 0 and self.game.guessMove[int(not player)] == 0:
                    self.state = 3
            else:

                if self.game.guessMove[player] == 0 and self.game.guessMove[int(not player)] == 0:
                    self.state = 4
                elif self.game.guessMove[player] == 0 and self.game.guessMove[int(not player)] != 0:
                    self.state = 5
                elif self.game.guessMove[player] != 0 and self.game.guessMove[int(not player)] == 0:
                    self.state = 6


def draw_grid(game, playground, state):
    grid_offset = playground.get_grid_offset()
    # kreslí se tabulka
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
        end_y = start_y
        arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.BLACK)

    # zakreslují se již umístěné symboly
    for symbol in game.fullMoves[0]:
        x_cor = symbol[0] * playground.get_cell_size() + playground.get_cell_size() // 2 + grid_offset // 2
        y_cor = symbol[1] * playground.get_cell_size() + playground.get_cell_size() // 2 + grid_offset
        arcade.draw_text('O', x_cor, y_cor, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
    for symbol in game.fullMoves[1]:
        x_cor = symbol[0] * playground.get_cell_size() + playground.get_cell_size() // 2 + grid_offset // 2
        y_cor = symbol[1] * playground.get_cell_size() + playground.get_cell_size() // 2 + grid_offset
        arcade.draw_text('X', x_cor, y_cor, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
    # ukazuje se, kam posledně hádal soupeř
    if game.wrongGuess != 0:
        x_cor = game.wrongGuess[0] * playground.get_cell_size() + playground.get_cell_size() // 2 + grid_offset // 2
        y_cor = game.wrongGuess[1] * playground.get_cell_size() + playground.get_cell_size() // 2 + grid_offset + 22
        arcade.draw_text('.', x_cor, y_cor, arcade.color.RED, font_size=50, anchor_x='center', anchor_y="center")

    # podle stavů se vypisuje text
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
    elif state == 9:
        text = 'Opponent disconnected, game over'
    elif state == 10:
        text = 'Game over, no one won'

    if state != 8:
        text_x = playground.width / 2
        text_y = grid_offset - 40
        arcade.draw_text(text, text_x, text_y, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

    else:
        text = f'Game over, the winner is player {int(game.winner)}.'
        text2 = 'Click anywhere to start a new game.'
        text_x = playground.width / 2
        text_y = grid_offset - 35
        arcade.draw_text(text, text_x, text_y, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
        text_y = grid_offset - 65
        arcade.draw_text(text2, text_x, text_y, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")


def draw_end_game(game, playground):
    grid_offset = playground.get_grid_offset()
    # nakreslím tabulku
    draw_grid(game, playground, state=8)

    # najdu si souřadnice uloženého políčka
    x = game.winningPlacement[0]
    y = game.winningPlacement[1]
    # najdu si sousední políčko
    cur_x = x + game.winningDirection[0]
    cur_y = y + game.winningDirection[1]

    # procházím, dokud jsou políčka v seznamu zahraných, těma pak vedu červenou úsečku
    # x a y jsou souřadnice krajního políčka, to znamená, že když se budu pohybovat ve správném směru, najdu všechna
    if [cur_x, cur_y] in game.fullMoves[game.winner]:
        while [cur_x, cur_y] in game.fullMoves[game.winner]:
            cur_x = cur_x + game.winningDirection[0]
            cur_y = cur_y + game.winningDirection[1]

        start_x = ((x + game.winningDirection[0]) * playground.get_cell_size()
                   + playground.get_cell_size() // 2 + grid_offset // 2)
        start_y = ((y + game.winningDirection[1]) * playground.get_cell_size()
                   + playground.get_cell_size() // 2 + grid_offset)
        end_x = ((cur_x - game.winningDirection[0]) * playground.get_cell_size()
                 + playground.get_cell_size() // 2 + grid_offset // 2)
        end_y = ((cur_y - game.winningDirection[1]) * playground.get_cell_size()
                 + playground.get_cell_size() // 2 + grid_offset)
        arcade.draw_line(start_x, start_y, end_x, end_y, color=arcade.color.RED, line_width=3)


def main():
    n = Network()
    # přiradím hráči číslo
    player = n.getNumOfP()
    try:
        game = n.send('get')


    except ConnectionError:
        exit()

    playground = Playground(player, title=f'You are a player {player}', game=game, network=n)
    arcade.run()


if __name__ == "__main__":
    main()
