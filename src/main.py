from __future__ import annotations

import pyglet as pg
from state import StateGame
from menu import StateMenu
from setting import Setting

class Game():
    def __init__(self, setting):
        self.settings = Setting('setting.toml')

        self.xlen, self.ylen = self.settings.data["xlen"], self.settings.data["ylen"]
        self.side = self.settings.data["side"]

        self.window = pg.window.Window(self.xlen * self.side, self.ylen * self.side)
        self.batch = pg.graphics.Batch()

        self.state: StateGame = StateMenu(self)

        self.window.set_handlers(
            on_key_press=self._on_key_press,
            on_draw=self._on_draw,
        )

    def set_state(self, state: StateGame):
        self.state = state

    def _on_key_press(self, symbol, modifiers):
        if hasattr(self.state, 'on_key_press'):
            self.state.on_key_press(symbol, modifiers)

    def _on_draw(self):
        if hasattr(self.state, 'on_draw'):
            self.state.on_draw()

    def run(self):
        pg.app.run(interval=0.1)


if __name__ == "__main__":
    pg.font.load('League Spartan')

    game = Game(Setting("setting.toml"))
    game.run()
