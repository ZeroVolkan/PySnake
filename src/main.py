from __future__ import annotations
from abc import ABC
import pyglet as pg

from pyglet.window import key

from snake import Direction, Snake
from apple import Apples
from menu import Menu, Select
from sys import exit

from abc import ABC, abstractmethod


class Game():
    def __init__(self, x, y, side):
        self.window = pg.window.Window(x * side, y * side)
        self.batch = pg.graphics.Batch()

        self.x, self.y = x, y
        self.side = side

        self.state: StateGame = StateMenu(self)
        self.set_state(self.state)

    def set_state(self, state: StateGame):
        self.state = state
        self.eventing()

    def eventing(self):
        self.window.set_handlers(
            on_key_press=self.state.on_key_press,
            on_draw=self.state.on_draw
        )


class StateGame(ABC):
    def __init__(self, game: Game):
        self.game: Game = game

    @abstractmethod
    def on_key_press(self, symbol, modifiers):
        ...

    @abstractmethod
    def on_draw(self):
        ...

class StateMenu(StateGame):
    def __init__(self, game):
        self.game = game
        self.menu = Menu(self.game.window, 75, self.game.batch)
        self._bind()

    def _bind(self):
        self.menu.bind(Select.GENERAL, 0, lambda: self._change())
        self.menu.bind(Select.GENERAL, 2, lambda: exit(0))

    def _change(self):
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

class StatePlay(StateGame):
    def __init__(self, game):
        self.game = game
        self.snake = Snake(24, 12, 40, self.game.batch)
        self.apples = Apples(48, 24, 40, self.game.batch)



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
            self.game.set_state(StateMenu(self.game))

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


if __name__  == "__main__":
    game = Game(48, 24, 40)
    pg.app.run(interval=0.1)
