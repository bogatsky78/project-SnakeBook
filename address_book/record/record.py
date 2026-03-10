from datetime import date, datetime, timedelta

from .fields.name import Name
from .fields.phone import Phone
from .fields.birthday import Birthday


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        p = self.find_phone(phone)
        if p:
            self.phones.remove(p)
        else:
            raise ValueError(f"Phone {phone} not found.")

    def edit_phone(self, old_phone, new_phone):
        p = self.find_phone(old_phone)
        if p:
            p.value = Phone(new_phone).value
        else:
            raise ValueError(f"Phone {old_phone} not found.")

    def find_phone(self, phone):
        normalized = ''.join(filter(str.isdigit, phone))
        return next((p for p in self.phones if p.value == normalized), None)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def get_congratulation_date(self):
        if not self.birthday:
            return None
        birthday = datetime.strptime(self.birthday.value, "%d.%m.%Y")
        today = datetime.today().date()

        birthday_this_year = date(today.year, birthday.month, birthday.day)
        if birthday_this_year < today:
            birthday_next = date(today.year + 1, birthday.month, birthday.day)
        else:
            birthday_next = birthday_this_year

        if today <= birthday_next <= today + timedelta(days=7):
            if birthday_next.weekday() >= 5:
                days_to_add = 7 - birthday_next.weekday()
                return birthday_next + timedelta(days=days_to_add)
            else:
                return birthday_next

        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"
