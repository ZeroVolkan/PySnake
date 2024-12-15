from tkinter import Menu
from enum import Enum
import pyglet as pg

from snake import Direction, Snake
from apple import Apples
from pyglet.window import key


class StateGame(Enum):
    menu = 0
    play = 1


x, y = 48, 24
side = 40

window = pg.window.Window(x * side, y * side)
state = StateGame(0)

# STARUP
def init_game():
    global snake, apples, batch
    batch = pg.graphics.Batch()
    snake = Snake(x // 2, y // 2, side, batch)
    apples = Apples(x, y, side, batch)
    [apples.generate() for i in range(4)]

# INPUT KEYBOARD
@window.event
def on_key_press(symbol, modifiers):
    global state
    snake.direction = direction if (direction := Direction.from_key(symbol)) != Direction.none else snake.direction

    if symbol == key.R:
        init_game()
    if symbol == key.ENTER:
        init_game()
        state = state.play

# GAME LOOP
@window.event
def on_draw():
    global state
    match state:
        case state.menu:
            # TODO: CREATE MENU
            ...

        case state.play:
            if is_over():
                print("GAME OVER")
                state = state.menu

            eat_and_move()
            draw_game()


def draw_game():
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

    print(window.width, window.height, xsnake, ysnake)
    if not (0 < xsnake < window.width) or not (0 < ysnake < window.height):
        return True

    return False


if __name__  == "__main__":
    init_game()
    pg.app.run(interval=0.1)
