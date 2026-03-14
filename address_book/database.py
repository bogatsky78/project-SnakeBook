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
                "INSERT OR REPLACE INTO contacts (name, birthday, email, address) VALUES (?, ?, ?, ?)",
                (
                    record.name.value,
                    record.birthday.value if record.birthday else None,
                    record.email.value if record.email else None,
                    record.address.value if record.address else None,
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

    def clear_all(self):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = OFF")
            conn.execute("DELETE FROM phones")
            conn.execute("DELETE FROM contacts")
            conn.execute("PRAGMA foreign_keys = ON")

    def load(self):
        book = AddressBook(db=self)
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            for name, birthday, email, address in conn.execute("SELECT name, birthday, email, address FROM contacts"):
                record = Record(name)
                if birthday:
                    record.add_birthday(birthday)
                if email:
                    record.add_email(email)
                if address:
                    record.add_address(address)
                for (phone,) in conn.execute(
                    "SELECT phone FROM phones WHERE contact_name = ?", (name,)
                ):
                    record.add_phone(phone)
                book.data[record.name.value] = record  # bypass auto-save on load
        return book
