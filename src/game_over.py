import pyglet as pg

from state import StateGame
from menu import StateMenu


class GameOver:
    def __init__(self, batch, window, side):
        self.batch = batch
        self.window = window
        self.side = side

        texts = ["Game Over", "press R to restart", "press ENTER to menu"]

        self.labels = [
            pg.text.Label(
                text=texts[i],
                font_name="League Spartan",
                font_size=36 if i == 0 else 30,
                x = self.window.width // 2,
                y = self.window.height - self.window.height // 4 - self.side * i,
                anchor_x="center",
                anchor_y="center",
                color=(255, 255, 255, 255) if i != 0 else (255, 0, 0, 255),
                batch=self.batch
            )
            for i in range(3)
        ]

    def draw(self):
        self.batch.draw()


class StateGameOver(StateGame):
    def __init__(self, game):
        self.game = game
        self.game_over = GameOver(self.game.batch, self.game.window, self.game.side)

    def on_key_press(self, symbol, modifiers):
        if symbol == pg.window.key.R:
            from play import StatePlay
            self.game.set_state(StatePlay(self.game))
        elif symbol == pg.window.key.ENTER:
            self.game.set_state(StateMenu(self.game))

    def on_draw(self):
        self.game.window.clear()
        self.game_over.draw()
