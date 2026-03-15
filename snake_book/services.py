from dataclasses import dataclass

from .contacts.record import Record
from .messages import (
    ADDRESS_ADDED,
    ADDRESS_REMOVED,
    ADDRESS_UPDATED,
    BIRTHDAY_ADDED,
    CONTACT_ADDED,
    CONTACT_DELETED,
    CONTACT_UPDATED,
    EMAIL_ADDED,
    EMAIL_REMOVED,
    EMAIL_UPDATED,
    NOTE_ADDED,
    NOTE_DELETED,
    NOTE_UPDATED,
    PHONE_ADDED,
    PHONE_REMOVED,
)
from .notes.note import Note


@dataclass
class OperationResult:
    status: str
    message: str
    payload: dict | None = None


class SnakeBookService:
    def __init__(self, book):
        self.book = book

    def add_contact(self, name, phone, birthday=None, email=None, address=None):
        record = Record(name)
        record.add_phone(phone)
        if birthday and birthday != "-":
            record.add_birthday(birthday)
        if email and email != "-":
            record.add_email(email)
        if address and address != "-":
            record.add_address(address)
        self.book.add_record(record)
        return OperationResult("ok", CONTACT_ADDED, {"name": record.name.value})

    def list_contacts(self):
        contacts = [self._serialize_record(r) for r in self.book.data.values()]
        return OperationResult("ok", "Contacts loaded.", {"contacts": contacts})

    def get_contact(self, name):
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        return OperationResult("ok", "Contact loaded.", {"contact": self._serialize_record(record)})

    def search_contacts(self, query):
        records = self.book.search(query)
        return OperationResult(
            "ok",
            "Contacts loaded.",
            {"contacts": [self._serialize_record(r) for r in records]},
        )

    def change_contact_phone(self, name, old_phone, new_phone):
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.edit_phone(old_phone, new_phone)
        if self.book.db:
            record.save(self.book.db)
        return OperationResult("ok", CONTACT_UPDATED, {"name": record.name.value})

    def remove_contact(self, name):
        self.book.delete(name)
        return OperationResult("ok", CONTACT_DELETED, {"name": name})

    def add_phone(self, name, phone):
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.add_phone(phone)
        if self.book.db:
            record.save(self.book.db)
        return OperationResult("ok", PHONE_ADDED, {"name": name})

    def remove_phone(self, name, phone):
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.remove_phone(phone)
        if self.book.db:
            record.save(self.book.db)
        return OperationResult("ok", PHONE_REMOVED, {"name": name})

    def add_birthday(self, name, birthday):
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.add_birthday(birthday)
        if self.book.db:
            record.save(self.book.db)
        return OperationResult("ok", BIRTHDAY_ADDED, {"name": name})

    def add_email(self, name, email):
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.add_email(email)
        if self.book.db:
            record.save(self.book.db)
        return OperationResult("ok", EMAIL_ADDED, {"name": name})

    def change_email(self, name, email):
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.edit_email(email)
        if self.book.db:
            record.save(self.book.db)
        return OperationResult("ok", EMAIL_UPDATED, {"name": name})

    def remove_email(self, name):
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.remove_email()
        if self.book.db:
            record.save(self.book.db)
        return OperationResult("ok", EMAIL_REMOVED, {"name": name})

    def add_address(self, name, address):
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.add_address(address)
        if self.book.db:
            record.save(self.book.db)
        return OperationResult("ok", ADDRESS_ADDED, {"name": name})

    def change_address(self, name, address):
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.edit_address(address)
        if self.book.db:
            record.save(self.book.db)
        return OperationResult("ok", ADDRESS_UPDATED, {"name": name})

    def remove_address(self, name):
        record = self.book.find(name)
        if not record:
            raise ValueError("Contact not found.")
        record.remove_address()
        if self.book.db:
            record.save(self.book.db)
        return OperationResult("ok", ADDRESS_REMOVED, {"name": name})

    def list_notes(self):
        notes = [self._serialize_note(n) for n in self.book.notes.all_notes()]
        return OperationResult("ok", "Notes loaded.", {"notes": notes})

    def get_note(self, note_id):
        note = self.book.notes.find(note_id)
        if not note:
            raise ValueError("Note not found.")
        return OperationResult("ok", "Note loaded.", {"note": self._serialize_note(note)})

    def add_note(self, text):
        note = Note(None, text)
        self.book.notes.add_note(note)
        return OperationResult("ok", f"{NOTE_ADDED} (ID: {note.id}).", {"note": self._serialize_note(note)})

    def edit_note(self, note_id, text):
        note = self.book.notes.edit(note_id, text)
        return OperationResult("ok", NOTE_UPDATED, {"note": self._serialize_note(note)})

    def remove_note(self, note_id):
        self.book.notes.delete(note_id)
        return OperationResult("ok", NOTE_DELETED, {"id": note_id})

    def search_notes(self, query):
        notes = [self._serialize_note(n) for n in self.book.notes.search(query)]
        return OperationResult("ok", "Notes loaded.", {"notes": notes})

    @staticmethod
    def _serialize_record(record):
        return {
            "name": record.name.value,
            "phones": [p.value for p in record.phones],
            "birthday": record.birthday.value if record.birthday else None,
            "email": record.email.value if record.email else None,
            "address": record.address.value if record.address else None,
        }

    @staticmethod
    def _serialize_note(note):
        return {
            "id": note.id,
            "text": note.text,
            "created_at": note.created_at,
            "created_at_formatted": note.formatted_created_at(),
        }