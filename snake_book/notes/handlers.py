from tabulate import tabulate
from .note import Note
from ..messages import NOTE_ADDED, NOTE_DELETED, NOTE_UPDATED
from ..ui import print_done, print_error, input_error


class NotesHandlers:
    @input_error
    def add_note(self, args):
        if len(args) < 1:
            raise ValueError("Provide note text.")
        note = Note(None, " ".join(args))
        self.book.notes.add_note(note)
        print_done(f"{NOTE_ADDED} (ID: {note.id}).")

    @input_error
    def show_note(self, args):
        if len(args) < 1:
            raise ValueError("Provide a note ID.")
        note = self.book.notes.find(int(args[0]))
        if not note:
            raise ValueError("Note not found.")
        table = [[note.id, note.formatted_created_at(), note.text]]
        print(tabulate(table, headers=["ID", "Created At", "Text"], tablefmt="grid"))

    @input_error
    def show_notes(self, _args=None):
        notes = self.book.notes.all_notes()
        if not notes:
            raise ValueError("No notes found.")
        table = [[note.id, note.formatted_created_at(), note.text] for note in notes]
        print(tabulate(table, headers=["ID", "Created At", "Text"], tablefmt="grid"))

    @input_error
    def edit_note(self, args):
        if len(args) < 2:
            raise ValueError("Provide note ID and new text.")
        self.book.notes.edit(int(args[0]), " ".join(args[1:]))
        print_done(NOTE_UPDATED)

    @input_error
    def delete_note(self, args):
        if len(args) < 1:
            raise ValueError("Provide a note ID.")
        self.book.notes.delete(int(args[0]))
        print_done(NOTE_DELETED)

    @input_error
    def search_note(self, args):
        if len(args) < 1:
            raise ValueError("Provide a search query.")
        notes = self.book.notes.search(" ".join(args))
        if not notes:
            raise ValueError("No notes found.")
        table = [[note.id, note.formatted_created_at(), note.text] for note in notes]
        print(tabulate(table, headers=["ID", "Created At", "Text"], tablefmt="grid"))
