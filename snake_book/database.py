import sqlite3
from .contacts.book import AddressBook
from .contacts.database import ContactsDatabase
from .notes.database import NotesDatabase


class Database(ContactsDatabase, NotesDatabase):
    def __init__(self, filename="personal_assistant.db"):
        self.filename = filename
        self._init_db()

    def _init_db(self):
        self._init_contacts_tables()
        self._init_notes_table()

    def clear_all(self):
        with sqlite3.connect(self.filename) as conn:
            self.clear_contacts()
            self.clear_notes()

    def load(self):
        book = AddressBook(db=self)
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            for record in self.load_contacts(conn):
                book.data[record.name.value] = record
            book.notes.data.update(self.load_notes(conn))
        return book
