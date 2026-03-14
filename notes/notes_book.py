from collections import UserDict


class NotesBook(UserDict):
    def __init__(self, db=None):
        super().__init__()
        self.db = db

    def add_note(self, note):
        if note.key in self.data:
            raise ValueError(f"Note {note.key} already exists.")
        self.data[note.key] = note
        if self.db:
            note.save(self.db)

    def find(self, key):
        return self.data.get(key)

    def edit(self, key, text):
        note = self.find(key)
        if not note:
            raise ValueError(f"Note {key} not found.")
        note.edit_text(text)
        if self.db:
            note.save(self.db)
        return note

    def delete(self, key):
        if key not in self.data:
            raise ValueError(f"Note {key} not found.")
        note = self.data.pop(key)
        if self.db:
            self.db.delete_note(note.key)

    def search(self, query):
        query = query.lower()
        return [
            note
            for note in self.all_notes()
            if query in note.key.lower() or query in note.text.lower()
        ]

    def all_notes(self):
        return sorted(
            self.data.values(),
            key=lambda note: note.created_at,
            reverse=True,
        )
