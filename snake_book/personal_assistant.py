import colorama
from colorama import Fore
from . import AssistantHandlers, Database
from .events import ChangeEventsWatcher

PROMPT = Fore.BLUE + "Enter a command: " + Fore.RESET


def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.strip().lower(), *args


def main():
    colorama.init()
    dumper = Database(filename="addressbook.db")
    book = dumper.load()
    h = AssistantHandlers(book)
    watcher = ChangeEventsWatcher(dumper, prompt=PROMPT)
    watcher.start()
    h.show_welcome_message()

    try:
        while True:
            command = input(PROMPT).strip()
            if not command:
                continue

            cmd, *args = parse_input(command)

            result = h.handle(cmd, args)
            if result is False:
                break
    finally:
        watcher.stop()


if __name__ == "__main__":
    main()
