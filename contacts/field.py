from abc import ABC, abstractmethod


class Field(ABC):
    def __init__(self, value):
        self.value = value

    @property
    @abstractmethod
    def value(self):
        ...

    @value.setter
    @abstractmethod
    def value(self, val):
        ...

    def __str__(self):
        return str(self.value)
