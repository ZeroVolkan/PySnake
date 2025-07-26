from __future__ import annotations

import pyglet as pg

from state import StateGame, state_factory, StateEnum
from setting import Setting

class Game():
    def __init__(self, setting):
        self.settings = Setting('setting.toml')
        self._register_states()

        self.xlen, self.ylen = self.settings.data["xlen"], self.settings.data["ylen"]
        self.side = self.settings.data["side"]

        self.window = pg.window.Window(self.xlen * self.side, self.ylen * self.side)
        self.batch = pg.graphics.Batch()

        self.fps = self.settings.data["fps"]

        self.state: StateGame = state_factory.create(StateEnum.menu, self)

        self.window.set_handlers(
            on_key_press=self._on_key_press,
            on_draw=self._on_draw,
        )

    def _register_states(self):
        from play import StatePlay
        from menu import StateMenu
        from game_over import StateGameOver

        state_factory.register(StateEnum.menu, StateMenu)
        state_factory.register(StateEnum.play, StatePlay)
        state_factory.register(StateEnum.game_over, StateGameOver)

    def set_state(self, state: StateGame | int | StateEnum, **kwargs):
        if isinstance(state, int) or isinstance(state, StateEnum):
            # Если передана строка - создаем состояние через фабрику
            new_state = state_factory.create(state, self, **kwargs)
            self.state = new_state
        elif isinstance(state, StateGame):
            # Если передан объект состояния - используем его напрямую
            self.state = state
        else:
            raise TypeError(f"state должен быть int или объектом StateGame или StateEnum, получен: {type(state)}")


    def _on_key_press(self, symbol, modifiers):
        if hasattr(self.state, 'on_key_press'):
            self.state.on_key_press(symbol, modifiers)

    def _on_draw(self):
        if hasattr(self.state, 'on_draw'):
            self.state.on_draw()

    def run(self):
        pg.app.run(1 / self.fps)


if __name__ == "__main__":
    pg.font.load('League Spartan')

    game = Game(Setting("setting.toml"))
    game.run()
