# SnakeBook
We keep your contacts close and your notes closer

A CLI personal assistant for contacts and standalone notes.

A CLI personal assistant that manages contacts with phone numbers, birthdays, emails, addresses, and standalone notes. Notes are independent from contacts and are not tied to postal addresses. Data is persisted to disk between sessions using a SQLite database.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 personal_assistant.py
```

The assistant loads contacts and notes from `personal_assistant.db` on startup and saves them automatically after every change.

## Project Structure

```
address_book/
├── __init__.py          # public exports
├── field.py             # abstract Field base class
├── book.py              # ContactsBook (UserDict)
├── handlers.py          # AssistantHandlers + input_error decorator
├── database.py          # SQLite persistence
└── record/
    ├── record.py        # Record (single contact)
    └── fields/
        ├── name.py      # Name field
        ├── phone.py     # Phone field
        ├── birthday.py  # Birthday field
        ├── email.py     # Email field
        └── address.py   # Address field

assistant_notes/
├── __init__.py          # Note + NotesBook exports
├── note.py              # Note model
└── notes_book.py        # NotesBook collection
```

## Commands

| Command | Arguments | Description |
|---|---|---|
| `hello` | — | Greet the assistant |
| `add-contact` | `<name> <phone>` | Add a phone to a new or existing contact |
| `change-contact` | `<name> <old_phone> <new_phone>` | Replace a phone number for an existing contact (alias: `change`) |
| `remove-contact-phone` | `<name> <phone>` | Remove a specific phone from a contact (alias: `remove-phone`) |
| `show-contact-phone` | `<name>` | Show a contact's phones (alias: `phone`) |
| `delete-contact` | `<name>` | Remove a contact entirely (alias: `delete`) |
| `show-contacts` | — | List all contacts (alias: `all`) |
| `add-contact-birthday` | `<name> <DD.MM.YYYY>` | Add a birthday to a contact (alias: `add-birthday`) |
| `show-contact-birthday` | `<name>` | Show a contact's birthday (alias: `show-birthday`) |
| `show-upcoming-birthdays` | — | List contacts with birthdays in the next 7 days (alias: `birthdays`) |
| `add-contact-email` | `<name> <email>` | Add an email address to a contact (alias: `add-email`) |
| `change-contact-email` | `<name> <email>` | Update a contact's email address (alias: `change-email`) |
| `remove-contact-email` | `<name>` | Remove a contact's email address (alias: `remove-email`) |
| `add-contact-address` | `<name> <address>` | Add a postal address to a contact (alias: `add-address`) |
| `change-contact-address` | `<name> <address>` | Update a contact's postal address (alias: `change-address`) |
| `remove-contact-address` | `<name>` | Remove a contact's postal address (alias: `remove-address`) |
| `add-note` | `<key> <text>` | Add a standalone note |
| `show-note` | `<key>` | Show a single note |
| `show-notes` | — | List all notes, newest first |
| `edit-note` | `<key> <text>` | Update a note's text |
| `delete-note` | `<key>` | Delete a note |
| `search-note` | `<query>` | Search notes by key or text |
| `close` / `exit` | — | Save and exit the assistant |

## Classes

| Class | File | Description |
|---|---|---|
| `input_error`, `print_done`, `print_error` | `address_book/handlers.py` | Shared utilities: `input_error` wraps handlers to catch common exceptions and display errors; `print_done`/`print_error` print colour-coded output. |
| `Field` | `address_book/field.py` | Base class for all contact fields. Stores a single value with a property getter/setter. |
| `Name` | `address_book/record/fields/name.py` | Extends `Field`. Stores a contact's name; validates it is at least 3 alphanumeric/`-`/`_` characters. |
| `Phone` | `address_book/record/fields/phone.py` | Extends `Field`. Stores a phone number; strips non-digit characters and requires at least 10 digits. |
| `Birthday` | `address_book/record/fields/birthday.py` | Extends `Field`. Stores a birthday string; validates it matches the `DD.MM.YYYY` format. |
| `Email` | `address_book/record/fields/email.py` | Extends `Field`. Stores an email address; validates it matches standard email format. |
| `Address` | `address_book/record/fields/address.py` | Extends `Field`. Stores a postal address; requires at least 3 characters. |
| `Record` | `address_book/record/record.py` | Represents a single contact. Holds a `Name`, a list of `Phone`s, and optional `Birthday`, `Email`, and `Address`. Provides methods to add, edit, and remove each field, as well as computing the next congratulation date for upcoming birthdays. |
| `Note` | `assistant_notes/note.py` | Represents a standalone note with a unique key, text content, and creation timestamp. |
| `NotesBook` | `assistant_notes/notes_book.py` | Extends `UserDict`. Stores notes keyed by note key, supports add/find/edit/delete/search operations, and lists notes newest first. |
| `ContactsBook` | `address_book/book.py` | Extends `UserDict`. The contact collection of `Record`s, keyed by name. Supports adding, finding, deleting records, listing contacts with birthdays in the next 7 days, and partial/multi-criteria search across name, phones, email, and address. |
| `AssistantHandlers` | `address_book/handlers.py` | Maps CLI commands to handler methods. Each method validates arguments, delegates to `ContactsBook`/`NotesBook`/`Record`, and prints results. Decorated with `input_error` to handle exceptions gracefully. |
| `Database` | `address_book/database.py` | Handles persistence via SQLite. Loads contacts and notes into separate collections from `personal_assistant.db`. Contacts are stored in a `contacts` table, phones in a separate `phones` table with a foreign-key cascade on delete, and notes in a `notes` table. |

## TODO

### Core

- [x] Implement `Notes` module — `Note` class with text content
- [x] `add-note` command
- [x] `show-note` / `show-notes` commands
- [x] `edit-note` command
- [x] `delete-note` command
- [x] `search-note` command
- [x] Persist notes to disk alongside contacts

### Bonus

- [ ] Add tags to notes
- [ ] `search-notes-by-tag` / sort notes by tag
- [ ] Intent recognition — predict command from free-text input
