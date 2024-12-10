import pyglet as pg
import random as rm

class Apples:
    def __init__(self, xlen, ylen, side, batch):
        self.apples: list[tuple[int, int]] = []

        self.xlen = xlen
        self.ylen = ylen
        self.side = side

        self.batch = batch

    def collision(self, x, y) -> bool:
        for apple in self.apples:
            if apple[0] * self.side == x and apple[1] * self.side == y:
                return True
        return False

    def remove(self, x, y) -> None:
        self.apples.remove((x, y))

    def add(self, x, y) -> None:
        self.apples.append((x, y))

    def generate(self) -> None:
        while True:
            x, y = rm.randint(0, self.xlen), rm.randint(0, self.ylen)
            if self.collision(x, y):
                continue
            self.add(rm.randint(0, self.xlen), rm.randint(0, self.ylen))

            break

    def draw(self):
        for apple in self.apples:
            pg.shapes.Rectangle(
                apple[0] * self.side, apple[1] * self.side,
                self.side,
                self.side,
                batch=self.batch,
                color=(255, 0, 0)
            ).draw()
