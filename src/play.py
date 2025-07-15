from __future__ import annotations

from pyglet.window import key

from apple import Apples
from snake import Snake, Direction
from state import StateGame
from menu import StateMenu
from game_over import StateGameOver

class StatePlay(StateGame):
    def __init__(self, game):
        self.game = game
        self.snake = Snake(24, 12, game.side, self.game.batch)
        self.apples = Apples(48, 24, game.side, self.game.batch)

        [self.apples.generate() for i in range(4)]

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.game.set_state(StateMenu(self.game))

        if (direction := Direction.from_key(symbol)) != Direction.none:
            self.snake.direction = direction

    def on_draw(self):
        self.game.window.clear()

        self.snake.draw()
        self._eat_and_move()
        if self._is_over():
            self.game.set_state(StateGameOver(self.game))

        self.apples.draw()


    def _eat_and_move(self):
        if self.apples.collision(*self.snake.position()):
            self.apples.remove(*map(lambda i: i // self.game.side, self.snake.position()))
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
