class Apples:
    def __init__(self, xlen, ylen, side):
        self.apples: list[tuple[int, int]]

        self.xlen = xlen
        self.ylen = ylen
        self.side = side

    def collision(self, x, y):
        for apple in self.apples:
            if apple == (x, y):
                pass

    def remove(self, x, y):
        self.apples.remove((x, y))

    def generate(self):
        ...
