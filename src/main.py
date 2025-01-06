from enum import Enum
from pyglet.window import key

import pyglet as pg

from snake import Direction, Snake
from apple import Apples
from menu import Menu


class StateGame(Enum):
    menu = 0
    play = 1
    init_menu = 2
    init_play = 3


x, y = 48, 24
side = 40

window = pg.window.Window(x * side, y * side)
state = StateGame(2)


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
    snake.direction = direction if (direction := Direction.from_key(symbol)) != Direction.none else snake.direction

    if symbol == key.R:
        init_play()
    if symbol == key.ENTER:
        init_play()
        state = state.play

    if state == state.menu:
        print(menu.chosen)
        if symbol == key.W:
            menu.up()
        if symbol == key.S:
            menu.down()


# GAME LOOP
@window.event
def on_draw():
    global state, menu


    match state:
        case state.play:
            if is_over():
                print("GAME OVER")
                state = state.menu

            eat_and_move()
            draw_play()

        case state.menu:
            menu.draw()

        case state.init_play:
            state = state.play
            init_play()

        case state.init_menu:
            state = state.menu
            init_menu()



def draw_play():
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
    init_play()
    pg.app.run(interval=0.1)
