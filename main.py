import arcade

class Playground(arcade.Window):
    def __init__(self, title, cell_size=30, grid_size=25):
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.window_size = self.grid_size * self.cell_size
        super().__init__(self.window_size, self.window_size, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.added_symbols = []
        self.game_over = False


    def on_draw(self):
        if not self.game_over:
            arcade.start_render()
            self.draw_grid()
        # else:
        #     self.draw_end_game()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        cell_x = x//self.cell_size
        cell_y = y//self.cell_size

        self.added_symbols.append((cell_x, cell_y, 'X'))
        direction = self.check_win_conditions(cell_x, cell_y, 'X')
        if direction:
            self.game_over = True
            self.draw_end_game(direction, cell_x, cell_y)




    def draw_end_game(self, direction, x, y):
        self.draw_grid()
        fin_x = x+direction[0]*4
        fin_y = y+direction[1]*4
        # maybe TODO allign line for horizontal
        print(direction)
        # arcade.draw_line((x-direction[0])*self.cell_size, (y-direction[1])*self.cell_size, fin_x*self.cell_size, fin_y*self.cell_size, color=arcade.color.RED, line_width=3 )
        arcade.draw_line((x+1)*self.cell_size, (y+1)*self.cell_size, fin_x*self.cell_size, fin_y*self.cell_size, color=arcade.color.RED, line_width=3 )


    def check_win_conditions(self, last_x, last_y, symbol = 'X'):

        bordering_coordinates = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for x, y in bordering_coordinates:
            count = 0
            new_x = last_x+x
            new_y = last_y+y
            for _ in range (4):
                if (new_x, new_y, symbol) in self.added_symbols:
                    new_x = new_x + x
                    new_y = new_y + y
                    count +=1
                else:
                    break
            if count ==4:
                return (x, y)
        return False

    def draw_grid(self):
        for x in range(self.grid_size):
            start_x = x * self.cell_size
            end_x = x * self.cell_size
            start_y = 0
            end_y = self.window_size
            arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.BLACK)

        for y in range(self.grid_size):
            start_x = 0
            end_x = self.window_size
            start_y = y * self.cell_size
            end_y = y * self.cell_size
            arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.BLACK)

        for symbol in self.added_symbols:
            # x_cor = symbol[0] * self.cell_size
            # y_cor = symbol[1] * self.cell_size
            x_cor = symbol[0] * self.cell_size + self.cell_size / 2
            y_cor = symbol[1] * self.cell_size + self.cell_size / 2
            arcade.draw_text(symbol[2], x_cor, y_cor, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

    # def put_symbol(self, pos_x, pos_y, symbol):
    #     x_cor = pos_x* self.cell_size
    #     y_cor = pos_y* self.cell_size
    #     arcade.draw_text(symbol, x_cor, y_cor)
def main():
    game = Playground(title='Player 1')
    arcade.run()


if __name__ == "__main__":
    main()
