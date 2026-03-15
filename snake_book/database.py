import sqlite3
from datetime import datetime, timezone
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
        self._init_events_table()

    def _init_events_table(self):
        with sqlite3.connect(self.filename) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS change_events (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    source     TEXT NOT NULL,
                    level      TEXT NOT NULL,
                    message    TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def clear_all(self):
        with sqlite3.connect(self.filename) as conn:
            self.clear_contacts()
            self.clear_notes()

    def log_event(self, message, source="system", level="done"):
        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with sqlite3.connect(self.filename) as conn:
            conn.execute(
                "INSERT INTO change_events (source, level, message, created_at) VALUES (?, ?, ?, ?)",
                (source, level, message, created_at),
            )

    def fetch_events(self, after_id=0, source=None):
        query = "SELECT id, source, level, message, created_at FROM change_events WHERE id > ?"
        params = [after_id]
        if source:
            query += " AND source = ?"
            params.append(source)
        query += " ORDER BY id ASC"

        with sqlite3.connect(self.filename) as conn:
            rows = conn.execute(query, params).fetchall()

        return [
            {
                "id": row[0],
                "source": row[1],
                "level": row[2],
                "message": row[3],
                "created_at": row[4],
            }
            for row in rows
        ]

    def latest_event_id(self, source=None):
        query = "SELECT COALESCE(MAX(id), 0) FROM change_events"
        params = []
        if source:
            query += " WHERE source = ?"
            params.append(source)
        with sqlite3.connect(self.filename) as conn:
            (value,) = conn.execute(query, params).fetchone()
        return value

    def load(self):
        book = AddressBook(db=self)
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            for record in self.load_contacts(conn):
                book.data[record.name.value] = record
            book.notes.data.update(self.load_notes(conn))
        return book
