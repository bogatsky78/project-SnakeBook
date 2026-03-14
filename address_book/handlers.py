import re
import random
from colorama import Fore, Style
from tabulate import tabulate
from faker import Faker
from .record.record import Record
from .notes import Note

def print_done(message):
    print(Fore.GREEN + message + Style.RESET_ALL)

def print_error(message):
    print(Fore.RED + message + Style.RESET_ALL)

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, TypeError, ValueError, KeyError) as e:
            print_error(str(e))
    return wrapper

class BookHandlers:
    def __init__(self, book):
        self.book = book
        self._handlers = {
            "add": self.add_contact,
            "change": self.change_contact,
            "remove-phone": self.remove_phone,
            "phone": self.show_phone,
            "delete": self.delete_contact,
            "all": self.show_all_contacts,
            "add-birthday": self.add_birthday,
            "show-birthday": self.show_birthday,
            "birthdays": self.birthdays,
            "add-email": self.add_email,
            "change-email": self.change_email,
            "remove-email": self.remove_email,
            "add-address": self.add_address,
            "change-address": self.change_address,
            "remove-address": self.remove_address,
            "add-note": self.add_note,
            "show-note": self.show_note,
            "show-notes": self.show_notes,
            "edit-note": self.edit_note,
            "delete-note": self.delete_note,
            "search-note": self.search_note,
            "generate-test-data": self.generate_test_data,
            "clear-all": self.clear_all,
            "info": self.show_contact_info,
            "hello": self.show_welcome_message
        }

    def show_welcome_message(self, _args=None):
        print_done("Welcome to the assistant bot!")

    def show_goodbye_message(self, _args=None):
        print_done("Good bye!")

    def handle(self, cmd, args):
        if cmd in ("close", "exit"):
            self.show_goodbye_message()
            return False
        if cmd in self._handlers:
            self._handlers[cmd](args)
            return True
        
        print_error("Invalid command.")
        return None

    @input_error
    def add_contact(self, args):
        if len(args) < 2:
            raise ValueError("Provide name and phone number.")
        name, phone = args[0], args[1]
        record = self.book.find(name)
        if record:
            record.add_phone(phone)
            print_done("Phone added to existing contact.")
            if self.book.db:
                record.save(self.book.db)
        else:
            from .record.record import Record
            record = Record(name)
            record.add_phone(phone)
            self.book.add_record(record)  # auto-saves via AddressBook
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
    def show_birthday(self, args):
        if len(args) < 1:
            raise ValueError("Provide a name.")
        record = self.book.find(args[0])
        if not record:
            raise ValueError("Contact not found.")
        if not record.birthday:
            raise ValueError("Birthday not set.")
        print_done(f"{record.name.value}'s birthday: {record.birthday.value}")

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
        print(args);
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
    def generate_test_data(self, _args=None):
        self.clear_all()
        fake = Faker()
        count = random.randint(5, 7)
        for _ in range(count):
            name = re.sub(r"[^a-zA-Z0-9_-]", "_", fake.name()).strip("_")
            record = Record(name)
            for _ in range(random.randint(1, 3)):
                digits = ''.join(filter(str.isdigit, fake.numerify('##########')))
                record.add_phone(digits)
            from datetime import date, timedelta
            today = date.today()
            target_day = today + timedelta(days=random.randint(-15, 15))
            birth_year = today.year - random.randint(18, 80)
            try:
                birthday = date(birth_year, target_day.month, target_day.day)
            except ValueError:
                birthday = date(birth_year, target_day.month, target_day.day - 1)
            record.add_birthday(birthday.strftime("%d.%m.%Y"))
            record.add_email(fake.email())
            record.add_address(fake.address().replace("\n", ", "))
            self.book.add_record(record)
        print_done(f"{count} test contacts generated.")

    @input_error
    def clear_all(self, _args=None):
        if self.book.db:
            self.book.db.clear_all()
        self.book.data.clear()
        print_done("All contacts deleted.")

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
        print(tabulate(table, tablefmt="grid"))

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

    @input_error
    def add_note(self, args):
        if len(args) < 2:
            raise ValueError("Provide note key and text.")
        note = Note(args[0], " ".join(args[1:]))
        self.book.notes.add_note(note)
        print_done("Note added.")

    @input_error
    def show_note(self, args):
        if len(args) < 1:
            raise ValueError("Provide a note key.")
        note = self.book.notes.find(args[0])
        if not note:
            raise ValueError("Note not found.")
        print_done(str(note))

    @input_error
    def show_notes(self, _args=None):
        notes = self.book.notes.all_notes()
        if not notes:
            raise ValueError("No notes found.")
        for note in notes:
            print_done(str(note))

    @input_error
    def edit_note(self, args):
        if len(args) < 2:
            raise ValueError("Provide note key and new text.")
        self.book.notes.edit(args[0], " ".join(args[1:]))
        print_done("Note updated.")

    @input_error
    def delete_note(self, args):
        if len(args) < 1:
            raise ValueError("Provide a note key.")
        self.book.notes.delete(args[0])
        print_done("Note deleted.")

    @input_error
    def search_note(self, args):
        if len(args) < 1:
            raise ValueError("Provide a search query.")
        notes = self.book.notes.search(" ".join(args))
        if not notes:
            raise ValueError("No notes found.")
        for note in notes:
            print_done(str(note))
