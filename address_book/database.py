import sqlite3
from .book import ContactsBook
from .notes import Note, NotesBook
from .record.record import Record


class Database:
    def __init__(self, filename="personal_assistant.db"):
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
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    note_key   TEXT PRIMARY KEY,
                    text       TEXT NOT NULL,
                    created_at TEXT NOT NULL
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

    def save_note(self, note):
        with sqlite3.connect(self.filename) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO notes (note_key, text, created_at) VALUES (?, ?, ?)",
                (note.key, note.text, note.created_at)
            )

    def delete_note(self, key):
        with sqlite3.connect(self.filename) as conn:
            conn.execute(
                "DELETE FROM notes WHERE note_key = ?",
                (key,)
            )

    def load(self):
        contacts_book = ContactsBook(db=self)
        notes_book = NotesBook(db=self)
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
                contacts_book.data[record.name.value] = record  # bypass auto-save on load
            for note_key, text, created_at in conn.execute(
                "SELECT note_key, text, created_at FROM notes ORDER BY created_at DESC"
            ):
                note = Note(note_key, text, created_at)
                notes_book.data[note.key] = note
        return contacts_book, notes_book
