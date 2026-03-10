from ...field import Field


class Phone(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        digits = ''.join(filter(str.isdigit, val))
        if len(digits) < 10:
            raise ValueError("Phone number must contain at least 10 digits.")
        self._value = digits
