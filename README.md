# SnakeBook
We keep your contacts close and your notes closer

A CLI address book — keep your contacts and their birthdays organised.

A CLI address book bot that manages contacts with phone numbers, birthdays, emails, and addresses. Data is persisted to disk between sessions using a SQLite database.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 address_book.py
```

The bot loads contacts from `addressbook.db` on startup and saves them automatically after every change.

## Project Structure

```
address_book/
├── __init__.py          # public exports
├── field.py             # abstract Field base class
├── book.py              # AddressBook (UserDict)
├── handlers.py          # BookHandlers + input_error decorator
├── database.py          # SQLite persistence
└── record/
    ├── record.py        # Record (single contact)
    └── fields/
        ├── name.py      # Name field
        ├── phone.py     # Phone field
        ├── birthday.py  # Birthday field
        ├── email.py     # Email field
        └── address.py   # Address field
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
| `add-email` | `<name> <email>` | Add an email address to a contact |
| `change-email` | `<name> <email>` | Update a contact's email address |
| `remove-email` | `<name>` | Remove a contact's email address |
| `add-address` | `<name> <address>` | Add a postal address to a contact |
| `change-address` | `<name> <address>` | Update a contact's postal address |
| `remove-address` | `<name>` | Remove a contact's postal address |
| `close` / `exit` | — | Save and exit the bot |

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
| `AddressBook` | `address_book/book.py` | Extends `UserDict`. The main collection of `Record`s, keyed by name. Supports adding, finding, deleting records, listing contacts with birthdays in the next 7 days, and partial/multi-criteria search across name, phones, email, and address. |
| `BookHandlers` | `address_book/handlers.py` | Maps CLI commands to their handler methods. Each method validates arguments, delegates to `AddressBook`/`Record`, and prints results. Decorated with `input_error` to handle exceptions gracefully. |
| `Database` | `address_book/database.py` | Handles persistence via SQLite. Saves and loads an `AddressBook` to/from `addressbook.db`. Contacts are stored in a `contacts` table; phones in a separate `phones` table with a foreign-key cascade on delete. |

## TODO

### Core

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
