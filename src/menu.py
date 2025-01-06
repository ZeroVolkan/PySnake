import pyglet as pg
from enum import Enum



class Menu:
    text = {
        0: "Start",
        1: "Settings",
        2: "Exit"
    }

    def __init__(self, window, side, batch):
        self.batch = batch
        self.window = window
        self.side = side
        self.chosen = 0

    def draw(self):
        for position, text in self.text.items():
            label = pg.text.Label(
                text,
                font_name='League Spartan',
                font_size=36,
                x = self.window.width // 2, y = self.window.height - self.window.height // 4 - self.side * position,
                anchor_x='center', anchor_y='center',
                color = (255, 0, 0) if position == self.chosen else (255, 255, 255)
            )

            label.draw()

    def up(self):
        if self.chosen <= 0:
            self.chosen = max(self.text.keys())
        else:
            self.chosen -= 1

    def down(self):
        if self.chosen >= max(self.text.keys()):
            self.chosen = -1
        self.chosen += 1

    def get(self):
        pass
