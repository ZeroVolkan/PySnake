from enum import Enum
from pyglet.window import key

import pyglet as pg

from snake import Direction, Snake
from apple import Apples
from menu import Menu


class StateGame(Enum):
    menu = 0
    play = 1

    def change(self):
        match self:
            case StateGame.menu:
                self = StateGame(1)
                init_play()
            case StateGame.play:
                self = StateGame(0)
                init_menu()
            case _:
                self = StateGame(0)
                init_menu()

        return self



x, y = 48, 24
side = 40

window = pg.window.Window(x * side, y * side)
state = StateGame(0)


# STARUP
def init_play():
    global snake, apples, batch
    batch = pg.graphics.Batch()
    snake = Snake(x // 2, y // 2, side, batch)
    apples = Apples(x, y, side, batch)
    [apples.generate() for i in range(4)]


def init_menu():
    global menu, batch
    batch = pg.graphics.Batch()
    menu = Menu(window, 75, batch)


# INPUT KEYBOARD
@window.event
def on_key_press(symbol, modifiers):
    global state, menu

    match state:
        case state.menu:
            if symbol == key.ENTER:
                if menu.chosen == 0:
                    state = state.change()
                elif menu.chosen == 1:
                    pass
                elif menu.chosen == 2:
                    pg.app.exit()

            if symbol == key.W or symbol == key.UP:
                menu.up()
            elif symbol == key.S or symbol == key.DOWN:
                menu.down()
            return

        case state.play:
            snake.direction = direction if (direction := Direction.from_key(symbol)) != Direction.none else snake.direction
            return

# GAME LOOP
@window.event
def on_draw():
    global state, menu

    match state:
        case state.play:
            eat_and_move()
            draw()

            if is_over():
                state = state.change()

        case state.menu:
            menu.draw()


def draw():
    window.clear()
    apples.draw()
    snake.draw()


def eat_and_move():
    if apples.collision(*snake.position()):
        apples.remove(*map(lambda i: i // side, snake.position()))
        snake.move(apple=True)
        apples.generate()
    else:
        snake.move()


def is_over():
    xsnake, ysnake = snake.position()

    if not snake.check_me():
        return True

    if not (0 <= xsnake < window.width) or not (0 <= ysnake < window.height):
        return True

    return False


if __name__  == "__main__":
    state = state.menu
    init_menu()
    pg.app.run(interval=0.1)
