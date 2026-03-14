import re
from ...field import Field

class Email(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.fullmatch(pattern, val):
            raise ValueError("Некоректний формат електронної пошти. Використовуйте формат: name@domain.com")
        self._value = val
