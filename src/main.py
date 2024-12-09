import pyglet as pg

from snake import Direction, Snake
from apple import Apples

x, y = 48, 24
side = 40

window = pg.window.Window(x * side, y * side)
batch = pg.graphics.Batch()
snake = Snake(x // 2, y // 2, side, batch)
apples = Apples(x, y, side, batch)
[apples.generate() for i in range(4)]

@window.event
def on_key_press(symbol, modifiers):
    snake.direction = direction if (direction := Direction.from_key(symbol)) != Direction.none else snake.direction

# GAME LOOP
@window.event
def on_draw():
    if apples.collision(*snake.position()):
        apples.remove(*map(lambda i: i // 40, snake.position()))
        snake.move(True)
        apples.generate()
    else:
        snake.move()

    window.clear()
    apples.draw()
    snake.draw()


pg.app.run(interval=0.1)
