import pyglet as pg

from snake import Direction, Snake
from apple import Apples

x, y = 48, 24
side = 40

window = pg.window.Window(x * side, y * side)
batch = pg.graphics.Batch()
snake = Snake(x // 2, y // 2, side, batch)
apples = Apples(x, y, side)


@window.event
def on_key_press(symbol, modifiers):
    snake.direction = direction if (direction := Direction.from_key(symbol)) != Direction.none else snake.direction


@window.event
def on_draw():
    snake.move()
    window.clear()
    snake.draw()


pg.app.run(interval=0.1)
