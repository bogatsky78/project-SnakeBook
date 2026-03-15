import re
from ...field import Field

class Name(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if not re.fullmatch(r"[a-zA-Z0-9_-]{3,}", val):
            raise ValueError("Name must be at least 3 characters (letters, digits, '-', '_').")
        self._value = val
