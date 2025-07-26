from abc import ABC, abstractmethod
from typing import Callable
from enum import Enum


class StateEnum(Enum):
    menu = 0,
    play = 1,
    game_over = 2


class StateGame(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def on_key_press(self, symbol, modifiers):
        ...

    @abstractmethod
    def on_draw(self):
        ...


class StateFactory():
    """Фабрика для создания состояний игры без циклических импортов"""
    def __init__(self):
        self.states: dict[StateEnum, Callable] = {}

    def register(self, state_id: StateEnum | int, creator_func: Callable):
        """Регистрирует функцию создания состояния"""
        self.states[StateEnum(state_id)] = creator_func

    def create(self, state_id: StateEnum | int, game, **kwargs):
        """Создает состояние по имени"""
        if state_id not in self.states:
            raise ValueError(f"Неизвестное состояние: {state_id}")

        return self.states[state_id](game, **kwargs)



state_factory = StateFactory()
