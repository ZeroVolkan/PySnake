from __future__ import annotations

from pyglet.window import key
import pyglet as pg

from apple import Apples
from snake import Snake, Direction
from state import StateGame
from menu import StateMenu
from game_over import StateGameOver

class StatePlay(StateGame):
    def __init__(self, game):
        self.game = game

        self.time_accumulator = 0
        self.moving_per_second = game.settings.data["moving_per_second"]
        self.speed_per_apple = game.settings.data["speed_per_apple"]

        pg.clock.schedule_interval(self._update, 1 / self.moving_per_second)

        self.foreground = pg.graphics.Group(order=1)
        self.background = pg.graphics.Group(order=0)

        self.snake  = Snake(game.xlen // 2, game.ylen // 2, game.side, game.batch, group=self.foreground)
        self.apples = Apples(game.xlen, game.ylen, game.side, game.batch, group=self.background)

        for i in range(game.settings.data["start_apples"]):
            self.apples.generate()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.game.set_state(StateMenu(self.game))

        if (direction := Direction.from_key(symbol)) == Direction.none:
            return
        if direction == self.snake.direction.reverse():
            return
        self.snake.direction = direction

    def on_draw(self):
        self.game.window.clear()
        self.game.batch.draw()


    def _update(self, dt):
        if self._eat_and_move():
            self.moving_per_second = self.moving_per_second + self.speed_per_apple * len(self.snake.parts)
            pg.clock.unschedule(self._update)
            pg.clock.schedule_interval(self._update, 1 / self.moving_per_second)

        if self._is_over():
           self.game.set_state(StateGameOver(self.game))

    def _eat_and_move(self) -> bool:
        grid = self.snake.position_grid()

        if self.apples.collision(*grid):
            self.apples.remove(*grid)
            self.snake.move(apple=True)
            self.apples.generate()
            return True

        self.snake.move()
        return False

    def _is_over(self):
        xsnake, ysnake = self.snake.position()

        if not self.snake.check_me():
            return True

        if not (0 <= xsnake < self.game.window.width) or not (0 <= ysnake < self.game.window.height):
            return True

        return False
