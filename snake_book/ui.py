import re
from colorama import Fore, Style
from tabulate import tabulate


def print_done(message):
    print(Fore.GREEN + message + Style.RESET_ALL)


def print_error(message):
    print(Fore.RED + message + Style.RESET_ALL)


def print_table(headers, rows):
    print(tabulate(rows, headers=headers, tablefmt="simple"))


def print_kv_table(title, rows):
    print(Fore.CYAN + Style.BRIGHT + f"  {title}" + Style.RESET_ALL)
    print(tabulate(rows, tablefmt="plain"))
    print()


def print_help_section(label, rows):
    print(Fore.CYAN + Style.BRIGHT + f"  {label}" + Style.RESET_ALL)
    table_str = tabulate(rows, headers=["⌨️  Command", "▸ Usage", "💬 Description"], tablefmt="simple")
    table_str = re.sub(
        r"(<[^|>\n]+>|\[[^\]\n]+\])",
        Fore.YELLOW + r"\1" + Style.RESET_ALL,
        table_str,
    )
    print(table_str)
    print()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, TypeError, ValueError, KeyError) as e:
            print_error(str(e))
    return wrapper
