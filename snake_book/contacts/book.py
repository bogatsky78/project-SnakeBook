from collections import UserDict

from ..notes import NotesBook


class AddressBook(UserDict):
    def __init__(self, db=None):
        super().__init__()
        self.db = db
        self.notes = NotesBook(db=db)

    def add_record(self, record):
        self.data[record.name.value] = record
        if self.db:
            record.save(self.db)

    def find(self, name):
        if self.db:
            return self.db.find_contact(name)
        return self.data.get(name)

    def all_records(self):
        if self.db:
            return self.db.all_contacts()
        return list(self.data.values())

    def delete(self, name):
        if name in self.data:
            record = self.data.pop(name)
            if self.db:
                self.db.delete_contact(record)
        else:
            raise ValueError(f"Contact {name} not found.")

    def get_upcoming_birthdays(self):
        output = []
        for r in self.all_records():
            congratulation_date = r.get_congratulation_date()
            if congratulation_date:
                output.append({
                    "name": r.name.value,
                    "congratulation_date": congratulation_date.strftime("%Y-%m-%d"),
                })
        return output
    
    def search(self, query):
        return self.db.search_contacts(query)
                
