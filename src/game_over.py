import pyglet as pg

from state import StateGame

class GameOver:
    def __init__(self, batch, window, side):
        self.batch = batch
        self.window = window
        self.side = side

        self.label = pg.text.Label(
            text="Game Over",
            font_name="League Spartan",
            font_size=36,
            x=self.window.width // 2,
            y=self.window.height // 2,
            anchor_x="center",
            anchor_y="center",
        )

    def draw(self):
        self.label.draw()


class StateGameOver(StateGame):
    def __init__(self, game):
        self.game = game
        self.game_over = GameOver(self.game.batch, self.game.window, self.game.side)

    def on_key_press(self, symbol, modifiers):
        print("Key pressed")

    def on_draw(self):
        self.game.window.clear()
        self.game_over.draw()
