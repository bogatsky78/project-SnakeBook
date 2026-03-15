# SnakeBook
We keep your contacts close and your notes closer

A CLI personal assistant that manages contacts with phone numbers, birthdays, emails, and addresses — plus standalone notes. All data is persisted between sessions using a SQLite database.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 -m snake_book
```

The assistant loads all data from `personal_assistant.db` on startup and saves automatically after every change.

## Project Structure

```
snake_book/
├── __init__.py              # public exports
├── __main__.py              # entry point
├── personal_assistant.py    # main loop
├── field.py                 # abstract Field base class
├── ui.py                    # print_done, print_error, input_error
├── handlers.py              # AssistantHandlers — command dispatcher
├── database.py              # Database — SQLite entry point
├── contacts/
│   ├── __init__.py          # Record export
│   ├── book.py              # AddressBook collection
│   ├── record.py            # Record (single contact)
│   ├── handlers.py          # ContactHandlers mixin
│   ├── database.py          # ContactsDatabase mixin
│   └── fields/
│       ├── __init__.py
│       ├── name.py
│       ├── phone.py
│       ├── birthday.py
│       ├── email.py
│       └── address.py
└── notes/
    ├── __init__.py          # Note + NotesBook exports
    ├── note.py              # Note model
    ├── notes_book.py        # NotesBook collection
    ├── handlers.py          # NotesHandlers mixin
    └── database.py          # NotesDatabase mixin
```

## Commands

### General

| Command | Arguments | Description |
|---|---|---|
| `help` | — | Show all available commands |
| `hello` | — | Show welcome message |
| `clear-all` | — | Delete all contacts and notes |
| `generate-test-data` | — | Populate with 5–7 random contacts and notes |
| `exit` / `close` | — | Exit the assistant |

### Contacts

| Command | Arguments | Description |
|---|---|---|
| `contacts` | — | List all contacts |
| `contact-add` | `<name> <phone> [birthday] [email] [address...]` | Add a new contact. Use `-` to skip optional fields. Address spans all remaining words. |
| `contact-change` | `<name> <old_phone> <new_phone>` | Replace a phone number |
| `contact-remove` | `<name>` | Delete a contact |
| `contact-show` | `<name>` | Show all details for a contact |
| `contact-search` | `<query>` | Search across name, phones, birthday, email, and address |

### Phones

| Command | Arguments | Description |
|---|---|---|
| `phone-add` | `<name> <phone>` | Add a phone to an existing contact |
| `phone-remove` | `<name> <phone>` | Remove a phone from a contact |

### Birthdays

| Command | Arguments | Description |
|---|---|---|
| `birthdays` | — | List contacts with birthdays in the next 7 days |
| `add-birthday` | `<name> <DD.MM.YYYY>` | Set a contact's birthday |

### Email

| Command | Arguments | Description |
|---|---|---|
| `email-add` | `<name> <email>` | Add an email |
| `email-change` | `<name> <email>` | Update an email |
| `email-remove` | `<name>` | Remove an email |

### Address

| Command | Arguments | Description |
|---|---|---|
| `address-add` | `<name> <address...>` | Add a postal address (all words after name are joined) |
| `address-change` | `<name> <address...>` | Update a postal address |
| `address-remove` | `<name>` | Remove a postal address |

### Notes

| Command | Arguments | Description |
|---|---|---|
| `notes` | — | List all notes, newest first |
| `note-add` | `<text>` | Add a note |
| `note-show` | `<id>` | Show a single note |
| `note-edit` | `<id> <text>` | Update a note's text |
| `note-remove` | `<id>` | Delete a note |
| `note-search` | `<query>` | Search notes by text |

## Classes

| Class | File | Description |
|---|---|---|
| `Field` | `snake_book/field.py` | Base class for all contact fields. Stores a single validated value. |
| `Name` | `contacts/fields/name.py` | Validates name is at least 3 alphanumeric/`-`/`_` characters. |
| `Phone` | `contacts/fields/phone.py` | Strips non-digits, requires at least 10 digits. |
| `Birthday` | `contacts/fields/birthday.py` | Validates `DD.MM.YYYY` format. |
| `Email` | `contacts/fields/email.py` | Validates standard email format. |
| `Address` | `contacts/fields/address.py` | Requires at least 3 characters. |
| `Record` | `contacts/record.py` | Single contact: one `Name`, many `Phone`s, optional `Birthday`/`Email`/`Address`. |
| `AddressBook` | `contacts/book.py` | `UserDict` of `Record`s. Handles add/find/delete and multi-field search. |
| `Note` | `notes/note.py` | A note with an auto-assigned id, text, and creation timestamp. |
| `NotesBook` | `notes/notes_book.py` | `UserDict` of `Note`s. Supports add/find/edit/delete/search, sorted newest-first. |
| `ContactHandlers` | `contacts/handlers.py` | Mixin with all contact-related command handlers. |
| `NotesHandlers` | `notes/handlers.py` | Mixin with all note-related command handlers. |
| `AssistantHandlers` | `snake_book/handlers.py` | Inherits both mixins. Owns the command registry and dispatches input. |
| `ContactsDatabase` | `contacts/database.py` | Mixin — contacts and phones table init, CRUD, and bulk load. |
| `NotesDatabase` | `notes/database.py` | Mixin — notes table init, CRUD, and bulk load. |
| `Database` | `snake_book/database.py` | Inherits both DB mixins. Owns `_init_db`, `load`, and `clear_all`. |

## TODO

### Bonus

- [ ] Add tags to notes
- [ ] `search-notes-by-tag` / sort notes by tag
- [ ] Intent recognition — predict command from free-text input
