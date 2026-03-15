from colorama import Fore, Style


def print_done(message):
    print(Fore.GREEN + message + Style.RESET_ALL)


def print_error(message):
    print(Fore.RED + message + Style.RESET_ALL)


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, TypeError, ValueError, KeyError) as e:
            print_error(str(e))
    return wrapper
