import random
from typing import TypeVar


T = TypeVar('T')

class RotatingList:
#doc strings
    def __init__(self, base_list: list[T]) -> None:
        self._base_list = base_list
        self._index = random.randint(0, len(self._base_list) - 1)
        
    @property
    def next(self) -> T:
        self._rotate_index()
        return self._base_list[self._index]

    def _rotate_index(self) -> None:
        self._index += 1
        if self._index == len(self._base_list):
            self._index = 0