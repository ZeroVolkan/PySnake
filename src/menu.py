from enum import Enum
from typing import Callable
from collections import namedtuple


import pyglet as pg

class Select(Enum):
    GENERAL = 0
    SETTINGS = 1

Choose = namedtuple("Choose", ["name", "callable"])

defaultMenu: dict[Select, dict[int, Choose]] = {
    Select.GENERAL: {
        0: Choose("Start", None),
        1: Choose("Settings", None),
        2: Choose("Exit", None)
    },
    Select.SETTINGS: {
        0: Choose("Return", None),
        1: Choose("...", None),
    }
}

class Menu:
    def __init__(self, window, side, batch, pattern=defaultMenu, default: bool=True):
        self.menu = pattern

        self.batch = batch
        self.window = window
        self.side = side

        self.select = Select.GENERAL
        self.chosen = 0

        if default:
            self.bind(
                Select.GENERAL, 1,
                lambda: self.change_select(Select.SETTINGS)
            )

            self.bind(
                Select.SETTINGS, 0,
                lambda: self.change_select(Select.GENERAL)
            )

    def draw(self):
        for position, choose in self.menu[self.select].items():
            label = pg.text.Label(
                choose.name,
                font_name='League Spartan',
                font_size=36,
                x = self.window.width // 2, y = self.window.height - self.window.height // 4 - self.side * position,
                anchor_x='center', anchor_y='center',
                color = (255, 0, 0) if position == self.chosen else (255, 255, 255)
            )

            label.draw()

    def up(self):
        if self.chosen <= 0:
            self.chosen = max(self.menu[self.select].keys())
        else:
            self.chosen -= 1

    def down(self):
        if self.chosen >= max(self.menu[self.select].keys()):
            self.chosen = -1
        self.chosen += 1

    def get(self):
        return self.menu[self.select][self.chosen]

    def change_select(self, select: Select):
        self.select = select
        self.chosen = 0

    def use(self):
        self.menu[self.select][self.chosen].callable()

    def bind(self, select: Select, choose: int, callable: Callable):
        self.menu[select][choose] = Choose(
            self.menu[select][choose].name,
            callable
        )

    def unbind(self, select: Select, choose: int):
        self.menu[select][choose] = Choose(
            self.menu[select][choose].name,
            None
        )
