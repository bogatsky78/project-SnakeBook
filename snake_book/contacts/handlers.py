from tabulate import tabulate
from .record import Record
from ..ui import print_done, print_error, input_error


class ContactHandlers:
    @input_error
    def add_contact(self, args):
        if len(args) < 2:
            raise ValueError("Provide name and phone (use '-' to skip birthday/email/address).")
        name     = args[0]
        phone    = args[1]
        birthday = args[2] if len(args) > 2 else None
        email    = args[3] if len(args) > 3 else None
        address  = " ".join(args[4:]) if len(args) > 4 else None

        record = Record(name)
        record.add_phone(phone)
        if birthday and birthday != "-":
            record.add_birthday(birthday)
        if email and email != "-":
            record.add_email(email)
        if address and address != "-":
            record.add_address(address)
        self.book.add_record(record)
        print_done("Contact added.")

    @input_error
    def change_contact(self, args):
        if len(args) < 3:
            raise ValueError("Provide name, old phone number, and new phone number.")
        name, old_phone, new_phone = args[0], args[1], args[2]
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.edit_phone(old_phone, new_phone)
        print_done("Contact updated.")
        if self.book.db:
            record.save(self.book.db)

    @input_error
    def show_phone(self, args):
        if len(args) < 1:
            raise ValueError("Provide a name.")
        record = self.book.find(args[0])
        if not record:
            raise ValueError("Contact not found.")
        phones = "; ".join(p.value for p in record.phones)
        table = [[record.name.value, phones]]
        print(tabulate(table, headers=["Name", "Phones"], tablefmt="grid"))

    @input_error
    def add_phone(self, args):
        if len(args) < 2:
            raise ValueError("Provide name and phone number.")
        name, phone = args[0], args[1]
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.add_phone(phone)
        print_done("Phone added.")
        if self.book.db:
            record.save(self.book.db)

    @input_error
    def remove_phone(self, args):
        if len(args) < 2:
            raise ValueError("Provide name and phone number.")
        name, phone = args[0], args[1]
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.remove_phone(phone)
        print_done("Phone removed.")
        if self.book.db:
            record.save(self.book.db)

    @input_error
    def delete_contact(self, args):
        if len(args) < 1:
            raise ValueError("Provide a name.")
        name = args[0]
        self.book.delete(name)  # auto-deletes from db via AddressBook
        print_done("Contact deleted.")

    @input_error
    def add_birthday(self, args):
        if len(args) < 2:
            raise ValueError("Provide name and birthday (DD.MM.YYYY).")
        name, birthday = args[0], args[1]
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.add_birthday(birthday)
        print_done("Birthday added.")
        if self.book.db:
            record.save(self.book.db)

    @input_error
    def birthdays(self, _args):
        upcoming = self.book.get_upcoming_birthdays()
        if not upcoming:
            print_done("No birthdays in the next 7 days.")
            return
        table = [[entry['name'], entry['congratulation_date']] for entry in upcoming]
        print(tabulate(table, headers=["Name", "Congratulation Date"], tablefmt="grid"))

    @input_error
    def add_email(self, args):
        if len(args) < 2:
            raise ValueError("Provide name and email.")
        record = self.book.find(args[0])
        if not record:
            raise ValueError("Contact not found.")
        record.add_email(args[1])
        print(args)
        print_done("Email added.")
        if self.book.db:
            record.save(self.book.db)

    @input_error
    def change_email(self, args):
        if len(args) < 2:
            raise ValueError("Provide name and new email.")
        record = self.book.find(args[0])
        if not record:
            raise ValueError("Contact not found.")
        record.edit_email(args[1])
        print_done("Email updated.")
        if self.book.db:
            record.save(self.book.db)

    @input_error
    def remove_email(self, args):
        if len(args) < 1:
            raise ValueError("Provide a name.")
        record = self.book.find(args[0])
        if not record:
            raise ValueError("Contact not found.")
        record.remove_email()
        print_done("Email removed.")
        if self.book.db:
            record.save(self.book.db)

    @input_error
    def add_address(self, args):
        if len(args) < 2:
            raise ValueError("Provide name and address.")
        record = self.book.find(args[0])
        if not record:
            raise ValueError("Contact not found.")
        record.add_address(" ".join(args[1:]))
        print_done("Address added.")
        if self.book.db:
            record.save(self.book.db)

    @input_error
    def change_address(self, args):
        if len(args) < 2:
            raise ValueError("Provide name and new address.")
        record = self.book.find(args[0])
        if not record:
            raise ValueError("Contact not found.")
        record.edit_address(" ".join(args[1:]))
        print_done("Address updated.")
        if self.book.db:
            record.save(self.book.db)

    @input_error
    def remove_address(self, args):
        if len(args) < 1:
            raise ValueError("Provide a name.")
        record = self.book.find(args[0])
        if not record:
            raise ValueError("Contact not found.")
        record.remove_address()
        print_done("Address removed.")
        if self.book.db:
            record.save(self.book.db)

    @input_error
    def show_contact_info(self, args):
        if len(args) < 1:
            raise ValueError("Provide a name.")
        record = self.book.find(args[0])
        if not record:
            raise ValueError("Contact not found.")
        phones = "; ".join(p.value for p in record.phones)
        birthday = record.birthday.value if record.birthday else ""
        email = record.email.value if record.email else ""
        address = record.address.value if record.address else ""
        table = [
            ["Name", record.name.value],
            ["Phones", phones],
            ["Birthday", birthday],
            ["Email", email],
            ["Address", address],
        ]
        print("Contact Info")
        print(tabulate(table, tablefmt="grid"))

    @input_error
    def search_contact(self, args):
        if len(args) < 1:
            raise ValueError("Provide a search query.")
        results = self.book.search(" ".join(args))
        if not results:
            raise ValueError("No contacts found.")
        table = []
        for record in results:
            phones = "; ".join(p.value for p in record.phones)
            birthday = record.birthday.value if record.birthday else ""
            email = record.email.value if record.email else ""
            address = record.address.value if record.address else ""
            table.append([record.name.value, phones, birthday, email, address])
        print(tabulate(table, headers=["Name", "Phones", "Birthday", "Email", "Address"], tablefmt="grid"))

    @input_error
    def show_all_contacts(self, _args=None):
        if not self.book.data:
            raise ValueError("No contacts found.")
        table = []
        for record in self.book.data.values():
            phones = "; ".join(p.value for p in record.phones)
            birthday = record.birthday.value if record.birthday else ""
            email = record.email.value if record.email else ""
            address = record.address.value if record.address else ""
            table.append([record.name.value, phones, birthday, email, address])
        print(tabulate(table, headers=["Name", "Phones", "Birthday", "Email", "Address"], tablefmt="grid"))
