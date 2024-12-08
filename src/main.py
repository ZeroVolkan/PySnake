import pyglet as pg

from snake import Direction, Snake
from pyglet.window import key

window = pg.window.Window(1280, 720)
batch = pg.graphics.Batch()
snake = Snake(8, 8, 40, batch)
apple_test = False

@window.event
def on_key_press(symbol, modifiers):
    snake.direction = direction if (direction := Direction.from_key(symbol)) != Direction.none else snake.direction
    if key.G == symbol:
        global apple_test
        apple_test = not apple_test


@window.event
def on_draw():
    snake.move(apple_test)
    window.clear()
    snake.draw()


pg.app.run(interval=0.1)
