from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
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
    
    def search(self, query):
        result = []
        query = query.lower
        for record in self.data.values():
            field_to_search = [
                record.name.value.lower(),
                *(phone.value for phone in record.phones)
            ]
            if hasattr(record, email) and record.email:
                field_to_search.append(record.email.value.lower())
            if hasattr(record, address) and record.address:
                field_to_search.append(record.address.value.lower())
            if any(query in field for field in fields_to_search):
                results.append(record)
        return result
                
