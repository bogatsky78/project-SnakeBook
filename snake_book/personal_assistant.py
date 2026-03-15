from colorama import Fore
from . import AssistantHandlers, Database

def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.strip().lower(), *args


def main():
    dumper = Database(filename="addressbook.db")
    book = dumper.load()
    h = AssistantHandlers(book)
    h.show_welcome_message()

    while True:
        command = input(Fore.BLUE + "Enter a command: " + Fore.RESET).strip()
        if not command:
            continue

        cmd, *args = parse_input(command)

        result = h.handle(cmd, args)
        if result is False:
            break


if __name__ == "__main__":
    main()
