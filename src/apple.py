import pyglet as pg
import random as rm

class Apples:
    "Создает поле со сторонами xlen и ylen, side указывает на размер яблока"
    def __init__(self, xlen: int, ylen: int, side: int, batch: pg.graphics.Batch, group: pg.graphics.Group | None=None):
        self.apples: list[pg.shapes.Rectangle] = []

        self.xlen = xlen
        self.ylen = ylen
        self.side = side

        self.batch = batch
        self.group = group

    def collision(self, x, y) -> bool:
        "Проверяет столкновение с яблоком"
        for rect in self.apples:
            if rect.x == x * self.side and rect.y == y * self.side:
                return True
        return False

    def remove(self, x, y) -> None:
        "Удаляет яблоко по координатам"
        for i, rect in enumerate(self.apples):
            if rect.x == x * self.side and rect.y == y * self.side:
                rect.delete()
                self.apples.pop(i)
                break

    def add(self, x, y) -> None:
        """Добавляет яблоко по координатам"""
        rect = pg.shapes.Rectangle(
            x * self.side, y * self.side,
            self.side, self.side,
            batch=self.batch,
            group=self.group,
            color=(255, 0, 0)
        )

        self.apples.append(rect)

    def generate(self) -> None:
        """Генерирует яблоко на поле со сторонами xlen и ylen"""
        while True:
            x, y = rm.randint(0, self.xlen), rm.randint(0, self.ylen)
            if self.collision(x, y):
                continue
            self.add(x, y)

            break

    def draw(self):
        self.batch.draw()
