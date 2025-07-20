from __future__ import annotations

import pyglet as pg
from state import StateGame
from menu import StateMenu


class Game():
    def __init__(self, x, y, side):
        self.window = pg.window.Window(x * side, y * side)
        self.batch = pg.graphics.Batch()

        self.x, self.y = x, y
        self.side = side

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

    game = Game(48, 24, 60)
    game.run()
