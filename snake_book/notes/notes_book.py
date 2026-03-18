from collections import UserDict

class NotesBook(UserDict):
    def __init__(self, db=None):
        super().__init__()
        self.db = db

    def add_note(self, note):
        if self.db:
            # Save first so the DB assigns the auto-increment id
            note.save(self.db)
        else:
            # No database: assign a simple sequential in-memory id
            note.id = (max(self.data.keys(), default=0) + 1)
        self.data[note.id] = note

    def find(self, id):
        if self.db:
            return self.db.find_note(id)
        return self.data.get(id)

    def edit(self, id, text):
        note = self.find(id)
        if not note:
            raise ValueError(f"Note {id} not found.")
        note.edit_text(text)
        if self.db:
            note.save(self.db)
        else:
            self.data[id] = note
        return note

    def delete(self, id):
        note = self.find(id)
        if not note:
            raise ValueError(f"Note {id} not found.")
        if self.db:
            self.db.delete_note(id)
        else:
            self.data.pop(id)

    def search(self, query):
        query = query.lower()
        return [
            note
            for note in self.all_notes()
            if query in note.text.lower()
        ]

    def all_notes(self):
        if self.db:
            return self.db.all_notes_from_db()
        return sorted(
            self.data.values(),
            key=lambda note: note.created_at,
            reverse=True,
        )
