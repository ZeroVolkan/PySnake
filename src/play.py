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

        self.foreground = pg.graphics.Group(order=1)
        self.background = pg.graphics.Group(order=0)

        self.snake = Snake(24, 12, game.side, self.game.batch, group=self.foreground)
        self.apples = Apples(48, 24, game.side, self.game.batch, group=self.background)

        [self.apples.generate() for i in range(4)]

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
        self._eat_and_move()
        self.game.batch.draw()

        if self._is_over():
            self.game.set_state(StateGameOver(self.game))



    def _eat_and_move(self):
        grid = self.snake.position_grid()

        if self.apples.collision(*grid):
            self.apples.remove(*grid)
            self.snake.move(apple=True)
            self.apples.generate()
        else:
            self.snake.move()

    def _is_over(self):
        xsnake, ysnake = self.snake.position()

        if not self.snake.check_me():
            return True

        if not (0 <= xsnake < self.game.window.width) or not (0 <= ysnake < self.game.window.height):
            return True

        return False
