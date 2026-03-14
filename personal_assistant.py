from colorama import Fore
from assistant_core import AssistantHandlers, Database


def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.strip().lower(), *args


def main():
    dumper = Database(filename="personal_assistant.db")
    contacts_book, notes_book = dumper.load()
    handlers = AssistantHandlers(contacts_book, notes_book)
    handlers.show_welcome_message()

    while True:
        command = input(Fore.BLUE + "Enter a command: " + Fore.RESET).strip()
        if not command:
            continue

        cmd, *args = parse_input(command)

        result = handlers.handle(cmd, args)
        if result is False:
            break


if __name__ == "__main__":
    main()
