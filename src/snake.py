from enum import Enum
from dataclasses import dataclass

import pyglet as pg
from pyglet.window import key


class Direction(Enum):
    "Направление движения змейки"
    up    = 0, 1
    down  = 0, -1
    right = 1, 0
    left  = -1, 0
    none = 0, 0

    @classmethod
    def from_key(cls, symbol):
        "Превращает символ в направление движения змейки"
        match symbol:
            case key.W:
                return cls.up
            case key.D:
                return cls.right
            case key.A:
                return cls.left
            case key.S:
                return cls.down
            case _:
                return cls.none

    def multiply(self, by) -> tuple[int, int]:
        return self.value[0] * by, self.value[1] * by


@dataclass
class SnakePart:
    "Часть змейки"
    body: pg.shapes.Rectangle
    direction: Direction


class Snake:
    """x, y указывает на координаты головы змейки,
    side - размер квадратной клетки,
    batch - пакет для рисования,
    direction - направление движения змейки"""
    def __init__(self, x: int, y: int, side: int, batch: pg.graphics.Batch, direction=Direction.none) -> None:
        self.head = pg.shapes.Rectangle(x * side, y * side, side, side, batch=batch)
        self.parts: list[SnakePart] = []
        self.batch: pg.graphics.Batch = batch
        self.side: int = side
        self.direction: Direction = direction

    def move(self, apple: bool = False) -> None:
        transform = self.direction.multiply(self.side)

        if apple:
            self.parts.append(
                SnakePart(
                    pg.shapes.Rectangle(self.head.x, self.head.y, self.side, self.side, batch=self.batch),
                    self.direction
                )
            )

        self.head.x += transform[0]
        self.head.y += transform[1]

        if apple:
            return

        new_direction = self.direction
        for part in reversed(self.parts):
            transform = part.direction.multiply(self.side)

            part.body.x += transform[0]
            part.body.y += transform[1]

            part.direction, new_direction = new_direction, part.direction

    def draw(self):
        self.head.draw()

        for part in self.parts:
            part.body.draw()

    def position(self):
        return self.head.x, self.head.y

    def position_grid(self):
        return tuple(map(lambda i: i // self.side, self.position()))

    def check_me(self):
        x, y = self.position()

        for part in self.parts:
            if part.body.x == x and part.body.y == y:
                return False
        return True
