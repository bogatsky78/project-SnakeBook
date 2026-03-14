import sqlite3
from .book import AddressBook
from .notes import Note
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
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    text         TEXT NOT NULL,
                    created_at   TEXT NOT NULL,
                    contact_name TEXT
                )
            """)
            # Migrate old schema (note_key TEXT PRIMARY KEY) to new (id INTEGER AUTOINCREMENT)
            cols = [row[1] for row in conn.execute("PRAGMA table_info(notes)").fetchall()]
            if "note_key" in cols:
                conn.execute("""
                    CREATE TABLE notes_new (
                        id           INTEGER PRIMARY KEY AUTOINCREMENT,
                        text         TEXT NOT NULL,
                        created_at   TEXT NOT NULL,
                        contact_name TEXT
                    )
                """)
                conn.execute("""
                    INSERT INTO notes_new (text, created_at, contact_name)
                    SELECT text, created_at, contact_name FROM notes
                """)
                conn.execute("DROP TABLE notes")
                conn.execute("ALTER TABLE notes_new RENAME TO notes")

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
                "DELETE FROM notes WHERE contact_name = ?",
                (record.name.value,)
            )
            conn.execute(
                "DELETE FROM contacts WHERE name = ?",
                (record.name.value,)
            )

    def save_note(self, note):
        with sqlite3.connect(self.filename) as conn:
            if note.id is None:
                # New note: insert and capture the auto-assigned id
                cursor = conn.execute(
                    "INSERT INTO notes (text, created_at, contact_name) VALUES (?, ?, ?)",
                    (note.text, note.created_at, note.contact_name)
                )
                note.id = cursor.lastrowid
            else:
                # Existing note: update in place
                conn.execute(
                    "UPDATE notes SET text=?, created_at=?, contact_name=? WHERE id=?",
                    (note.text, note.created_at, note.contact_name, note.id)
                )

    def delete_note(self, id):
        with sqlite3.connect(self.filename) as conn:
            conn.execute(
                "DELETE FROM notes WHERE id = ?",
                (id,)
            )

    def clear_all(self):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = OFF")
            conn.execute("DELETE FROM phones")
            conn.execute("DELETE FROM contacts")
            conn.execute("DELETE FROM notes")
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
            for id, text, created_at, contact_name in conn.execute(
                "SELECT id, text, created_at, contact_name FROM notes ORDER BY created_at DESC"
            ):
                book.notes.data[id] = Note(id, text, created_at, contact_name)
        return book
