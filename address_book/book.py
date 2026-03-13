from collections import UserDict


class AddressBook(UserDict):
    def __init__(self, db=None):
        super().__init__()
        self.db = db

    def add_record(self, record):
        self.data[record.name.value] = record
        if self.db:
            record.save(self.db)

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            record = self.data.pop(name)
            if self.db:
                self.db.delete_contact(record)
        else:
            raise ValueError(f"Contact {name} not found.")

    def get_upcoming_birthdays(self):
        output = []
        for r in self.data.values():
            congratulation_date = r.get_congratulation_date()
            if congratulation_date:
                output.append({
                    "name": r.name.value,
                    "congratulation_date": congratulation_date.strftime("%Y-%m-%d"),
                })
        return output
