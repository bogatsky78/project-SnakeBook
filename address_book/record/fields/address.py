import re
from ...field import Field

class Address(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if not val or len(val.strip()) < 3:
            raise ValueError("Адреса занадто коротка! введіть коректну адресу.")
        self._value = val