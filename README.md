# SnakeBook
We keep your contacts close and your notes closer

A CLI address book — keep your contacts and their birthdays organised.

A CLI address book bot that manages contacts with phone numbers and birthdays. Data is persisted to disk between sessions using pickle serialization.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 address_book.py
```

The bot loads contacts from `addressbook.pkl` on startup and saves them automatically when you exit.

## Project Structure

```
address_book/
├── __init__.py          # public exports
├── field.py             # abstract Field base class
├── book.py              # AddressBook (UserDict)
├── handlers.py          # BookHandlers + input_error decorator
├── dumper.py            # pickle persistence
└── record/
    ├── record.py        # Record (single contact)
    └── fields/
        ├── name.py      # Name field
        ├── phone.py     # Phone field
        └── birthday.py  # Birthday field
```

## Commands

| Command | Arguments | Description |
|---|---|---|
| `hello` | — | Greet the bot |
| `add` | `<name> <phone>` | Add a phone to a new or existing contact |
| `change` | `<name> <old_phone> <new_phone>` | Replace a phone number for an existing contact |
| `remove-phone` | `<name> <phone>` | Remove a specific phone from a contact |
| `delete` | `<name>` | Remove a contact entirely |
| `phone` | `<name>` | Show a contact's phones |
| `all` | — | List all contacts |
| `add-birthday` | `<name> <DD.MM.YYYY>` | Add a birthday to a contact |
| `show-birthday` | `<name>` | Show a contact's birthday |
| `birthdays` | — | List contacts with birthdays in the next 7 days |
| `close` / `exit` | — | Save and exit the bot |

## Classes

| Class | File | Description |
|---|---|---|
| `input_error`, `print_done`, `print_error` | `address_book/handlers.py` | Shared utilities: `input_error` wraps handlers to catch common exceptions and display errors; `print_done`/`print_error` print colour-coded output. |
| `Field` | `address_book/field.py` | Base class for all contact fields. Stores a single value with a property getter/setter. |
| `Name` | `address_book/record/fields/name.py` | Extends `Field`. Stores a contact's name; validates it is at least 3 alphanumeric/`-`/`_` characters. |
| `Phone` | `address_book/record/fields/phone.py` | Extends `Field`. Stores a phone number; strips non-digit characters and requires at least 10 digits. |
| `Birthday` | `address_book/record/fields/birthday.py` | Extends `Field`. Stores a birthday string; validates it matches the `DD.MM.YYYY` format. |
| `Record` | `address_book/record/record.py` | Represents a single contact. Holds a `Name`, a list of `Phone`s, and an optional `Birthday`. Provides methods to add, edit, remove, and find phones, as well as computing the next congratulation date for upcoming birthdays. |
| `AddressBook` | `address_book/book.py` | Extends `UserDict`. The main collection of `Record`s, keyed by name. Supports adding, finding, deleting records, and listing contacts with birthdays in the next 7 days. |
| `BookHandlers` | `address_book/handlers.py` | Maps CLI commands to their handler methods. Each method validates arguments, delegates to `AddressBook`/`Record`, and prints results. Decorated with `input_error` to handle exceptions gracefully. |
| `Dumper` | `address_book/dumper.py` | Handles persistence. Saves and loads an `AddressBook` to/from a pickle file (`addressbook.pkl` by default). |

## TODO

### Core

- [ ] Add `Email` field to `Record` with format validation
- [ ] Add `Address` field to `Record`
- [ ] Improve contact search — partial/multi-criteria matching
- [ ] Implement `Notes` module — `Note` class with text content
- [ ] `add-note` command
- [ ] `show-note` / `show-notes` commands
- [ ] `edit-note` command
- [ ] `delete-note` command
- [ ] `search-note` command
- [ ] Persist notes to disk alongside contacts

### Bonus

- [ ] Add tags to notes
- [ ] `search-notes-by-tag` / sort notes by tag
- [ ] Intent recognition — predict command from free-text input

### Extra features
- [ ] Replace pickle with SQLite storage backend

info 1