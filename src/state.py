from abc import ABC, abstractmethod

class StateGame(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def on_key_press(self, symbol, modifiers):
        ...

    @abstractmethod
    def on_draw(self):
        ...
