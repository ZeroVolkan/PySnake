from enum import Enum
from typing import Callable
from collections import namedtuple

import pyglet as pg

from pyglet.window import key
from state import StateGame

class StateMenu(StateGame):
    def __init__(self, game):
        self.game = game
        self.menu = Menu(self.game.window, 75, self.game.batch)
        self._bind()


    def _bind(self):
        self.menu.bind(Select.GENERAL, 0, lambda: self._change())
        self.menu.bind(Select.GENERAL, 2, lambda: exit(0))

    def _change(self):
        from play import StatePlay
        self.game.set_state(StatePlay(self.game))

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            self.menu.use()
        elif symbol == key.W or symbol == key.UP:
            self.menu.up()
        elif symbol == key.S or symbol == key.DOWN:
            self.menu.down()

    def on_draw(self):
        self.game.window.clear()
        self.menu.draw()
        self.game.window.flip()


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
