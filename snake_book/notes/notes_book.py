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
        return self.data.get(id)

    def edit(self, id, text):
        note = self.find(id)
        if not note:
            raise ValueError(f"Note {id} not found.")
        note.edit_text(text)
        if self.db:
            note.save(self.db)
        return note

    def delete(self, id):
        if id not in self.data:
            raise ValueError(f"Note {id} not found.")
        note = self.data.pop(id)
        if self.db:
            self.db.delete_note(note.id)

    def search(self, query):
        query = query.lower()
        return [
            note
            for note in self.all_notes()
            if query in note.text.lower()
        ]

    def notes_for_contact(self, contact_name):
        return sorted(
            [note for note in self.data.values() if note.contact_name == contact_name],
            key=lambda note: note.created_at,
            reverse=True,
        )

    def all_notes(self):
        return sorted(
            self.data.values(),
            key=lambda note: note.created_at,
            reverse=True,
        )
