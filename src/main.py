import pyglet as pg

from pyglet.window import key
from enum import Enum

from snake import Direction, Snake
from apple import Apples
from menu import Menu, Select
from sys import exit


class State(Enum):
    menu = 0
    play = 1

x, y = 48, 24
side = 40

window = pg.window.Window(x * side, y * side)
state = State(0)

def change():
    global state
    state = State(1) if state.value == 0 else State(0)
    if state == State.play:
        init_play()
    else:
        init_menu()


# STARUP
def init_play():
    global snake, apples, batch
    batch = pg.graphics.Batch()
    snake = Snake(x // 2, y // 2, side, batch)
    apples = Apples(x, y, side, batch)
    [apples.generate() for i in range(4)]


def init_menu():
    global menu, batch, state

    batch = pg.graphics.Batch()
    menu = Menu(window, 75, batch)

    menu.bind(Select.GENERAL, 0, lambda: change())
    menu.bind(Select.GENERAL, 2, lambda: exit(0))


# INPUT KEYBOARD
@window.event
def on_key_press(symbol, modifiers):
    global state, menu

    match state:
        case State.menu:
            if symbol == key.ENTER:
                menu.use()
            if symbol == key.W or symbol == key.UP:
                menu.up()
            elif symbol == key.S or symbol == key.DOWN:
                menu.down()
            return

        case State.play:
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
                change()

        case state.menu:
            window.clear()
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
