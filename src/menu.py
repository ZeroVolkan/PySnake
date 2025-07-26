from __future__ import annotations
from enum import Enum
from typing import Callable

import pyglet as pg

from pyglet.window import key
from state import StateGame, StateEnum


class StateMenu(StateGame):
    def __init__(self, game):
        self.game = game
        self.menu: Menu = Menu(self.game.window, 75)
        self._bind()

    def _bind(self):
        self.menu.bind(Select.GENERAL, 0, self._to_play)
        self.menu.bind(Select.GENERAL, 1, self._to_settings)
        self.menu.bind(Select.GENERAL, 2, exit)

    def _to_play(self):
        self.game.set_state(StateEnum.play)

    def _to_settings(self):
        self.menu.change_select(Select.SETTINGS)

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


class Select(Enum):
    GENERAL = 0
    SETTINGS = 1
    EXIT = 2

class Choose:
    def __init__(self, name: str, callback: Callable | None = None):
        self.name = name
        self.callback = callback

defaultMenu: dict[Select, dict[int, Choose]] = {
    Select.GENERAL: {
        0: Choose("Start"),
        1: Choose("Settings"),
        2: Choose("Exit")
    },
    Select.SETTINGS: {
        0: Choose("Return"),
        1: Choose("..."),
    }
}

class Menu:
    def __init__(self, window, side, pattern=defaultMenu):
        self.menu = pattern

        self.batch = pg.graphics.Batch()
        self.window = window
        self.side = side

        self.select = Select.GENERAL
        self.chosen = 0

        self.labels = [
            pg.text.Label(
                choose.name,
                font_name='League Spartan',
                font_size=36,
                x = self.window.width // 2,
                y = self.window.height - self.window.height // 4 - self.side * idx,
                anchor_x='center', anchor_y='center',
                color = (255, 255, 255, 255),
                batch=self.batch
            )
            for idx, (position, choose) in enumerate(sorted(self.menu[self.select].items()))
        ]

    def draw(self):
        self.labels[self.chosen].color = (255, 0, 0, 255)
        self.batch.draw()
        self.labels[self.chosen].color = (255, 255, 255, 255)

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
        if self.menu[self.select][self.chosen].callback:
            self.menu[self.select][self.chosen].callback()
        else:
            print("Don't have method")

    def bind(self, select: Select, choose: int, callback: Callable):
        self.menu[select][choose].callback = callback
