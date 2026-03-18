import re
import random
from datetime import date, timedelta
from faker import Faker
from .contacts.record import Record
from .contacts.handlers import ContactHandlers
from .notes import Note
from .notes.handlers import NotesHandlers
from .ui import print_done, print_error, input_error, print_help_section

_HELP_CATEGORIES = [
    ("Contacts",   ["contacts", "contact-add", "contact-change",
                    "contact-remove", "contact-show", "contact-search"]),
    ("Phones",     ["phone-add", "phone-remove"]),
    ("Birthdays",  ["birthdays", "add-birthday"]),
    ("Emails",     ["email-add", "email-change", "email-remove"]),
    ("Addresses",  ["address-add", "address-change", "address-remove"]),
    ("Notes",      ["notes", "note-add", "note-show",
                    "note-edit", "note-remove", "note-search"]),
    ("General",    ["help", "hello", "clear-all",
                    "generate-test-data", "exit / close"]),
]


class AssistantHandlers(ContactHandlers, NotesHandlers):
    def __init__(self, book):
        self.book = book
        self._handlers = {

            "contacts":           (self.show_all_contacts,   "List all contacts"),
            "contact-add":        (self.add_contact,         "<name> <phone> [birthday] [email] [address...] — Add contact (use '-' to skip a field)"),
            "contact-change":     (self.change_contact,      "<name> <old_phone> <new_phone> — Change a phone"),
            "contact-remove":     (self.delete_contact,      "<name> — Delete a contact"),
            "contact-show":       (self.show_contact_info,   "<name> — Show contact details"),
            "contact-search":     (self.search_contact,      "<query> — Search contacts by any field"),

            "phone-add":          (self.add_phone,           "<name> <phone> — Add phone to contact"),
            "phone-remove":       (self.remove_phone,        "<name> <phone> — Remove phone from contact"),

            "birthdays":          (self.birthdays,           "Show upcoming birthdays (next 7 days)"),
            "add-birthday":       (self.add_birthday,        "<name> <DD.MM.YYYY> — Set birthday"),

            "email-add":          (self.add_email,           "<name> <email> — Add email"),
            "email-change":       (self.change_email,        "<name> <email> — Change email"),
            "email-remove":       (self.remove_email,        "<name> — Remove email"),

            "address-add":        (self.add_address,         "<name> <address> — Add address"),
            "address-change":     (self.change_address,      "<name> <address> — Change address"),
            "address-remove":     (self.remove_address,      "<name> — Remove address"),

            "notes":              (self.show_notes,          "List all notes"),
            "note-add":           (self.add_note,            "<text> — Add a note"),
            "note-show":          (self.show_note,           "<id> — Show a note"),
            "note-edit":          (self.edit_note,           "<id> <text> — Edit a note"),
            "note-remove":        (self.delete_note,         "<id> — Delete a note"),
            "note-search":        (self.search_note,         "<query> — Search notes"),

            "help":               (self.show_help,           "Show this help message"),
            "hello":              (self.show_welcome_message,"Show welcome message"),
            "clear-all":          (self.clear_all,           "Delete all contacts and notes"),
            "generate-test-data": (self.generate_test_data,  "Populate with random test data"),
            "exit":               (None,                     "Exit the assistant"),
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
            handler, _ = self._handlers[cmd]
            handler(args)
            return True

        print_error("Invalid command.")
        return None

    def show_help(self, _args=None):
        exit_desc = self._handlers["exit"][1]
        synthetic = {"exit / close": (None, exit_desc)}

        for label, cmds in _HELP_CATEGORIES:
            rows = []
            for cmd in cmds:
                handler_tuple = self._handlers.get(cmd) or synthetic.get(cmd)
                if handler_tuple is None:
                    continue
                raw_desc = handler_tuple[1]
                if " — " in raw_desc:
                    usage, description = raw_desc.split(" — ", 1)
                else:
                    usage, description = "", raw_desc
                rows.append([cmd, usage, description])
            if rows:
                print_help_section(label, rows)

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
            for _ in range(random.randint(0, 10)):
                self.book.notes.add_note(Note(None, fake.sentence()))
        print_done(f"{count} test contacts generated.")

    @input_error
    def clear_all(self, _args=None):
        if self.book.db:
            self.book.db.clear_all()
        else:
            self.book.data.clear()
            self.book.notes.data.clear()
        print_done("All contacts deleted.")
