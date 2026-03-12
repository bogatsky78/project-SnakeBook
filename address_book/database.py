import sqlite3
from .book import AddressBook
from .record.record import Record


class Database:
    def __init__(self, filename="addressbook.db"):
        self.filename = filename
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    name     TEXT PRIMARY KEY,
                    birthday TEXT,
                    email    TEXT,
                    address  TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS phones (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    contact_name  TEXT NOT NULL REFERENCES contacts(name) ON DELETE CASCADE,
                    phone         TEXT NOT NULL
                )
            """)

    def save_contact(self, record):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute(
                "INSERT OR REPLACE INTO contacts (name, birthday) VALUES (?, ?)",
                (
                    record.name.value,
                    record.birthday.value if record.birthday else None,
                )
            )

    def save_phones(self, record):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute(
                "DELETE FROM phones WHERE contact_name = ?",
                (record.name.value,)
            )
            for phone in record.phones:
                conn.execute(
                    "INSERT INTO phones (contact_name, phone) VALUES (?, ?)",
                    (record.name.value, phone.value)
                )

    def delete_contact(self, record):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute(
                "DELETE FROM contacts WHERE name = ?",
                (record.name.value,)
            )

    def save(self, book):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("DELETE FROM phones")
            conn.execute("DELETE FROM contacts")
        for record in book.data.values():
            self.save_contact(record)
            self.save_phones(record)

    def load(self):
        book = AddressBook()
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            for name, birthday in conn.execute("SELECT name, birthday FROM contacts"):
                record = Record(name)
                if birthday:
                    record.add_birthday(birthday)
                for (phone,) in conn.execute(
                    "SELECT phone FROM phones WHERE contact_name = ?", (name,)
                ):
                    record.add_phone(phone)
                book.add_record(record)
        return book
