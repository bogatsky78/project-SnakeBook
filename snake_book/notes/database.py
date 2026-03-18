import sqlite3
from .note import Note


class NotesDatabase:
    def _init_notes_table(self):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    text       TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

    def clear_notes(self):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA foreign_keys = OFF")
            conn.execute("DELETE FROM notes")
            conn.execute("PRAGMA foreign_keys = ON")

    def save_note(self, note):
        with sqlite3.connect(self.filename) as conn:
            if note.id is None:
                cursor = conn.execute(
                    "INSERT INTO notes (text, created_at) VALUES (?, ?)",
                    (note.text, note.created_at)
                )
                note.id = cursor.lastrowid
            else:
                conn.execute(
                    "UPDATE notes SET text=?, created_at=? WHERE id=?",
                    (note.text, note.created_at, note.id)
                )

    def delete_note(self, id):
        with sqlite3.connect(self.filename) as conn:
            conn.execute(
                "DELETE FROM notes WHERE id = ?",
                (id,)
            )

    def find_note(self, id):
        with sqlite3.connect(self.filename) as conn:
            row = conn.execute(
                "SELECT id, text, created_at FROM notes WHERE id = ?", (id,)
            ).fetchone()
            if row is None:
                return None
            return Note(row[0], row[1], row[2])

    def all_notes_from_db(self):
        with sqlite3.connect(self.filename) as conn:
            notes = self.load_notes(conn)
        return sorted(notes.values(), key=lambda n: n.created_at, reverse=True)

    def load_notes(self, conn):
        notes = {}
        for id, text, created_at in conn.execute(
            "SELECT id, text, created_at FROM notes ORDER BY created_at DESC"
        ):
            notes[id] = Note(id, text, created_at)
        return notes
