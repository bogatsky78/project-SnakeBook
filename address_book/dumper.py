import pickle
from .book import AddressBook


class Dumper:
    def __init__(self, filename="addressbook.pkl"):
        self.filename = filename

    def save(self, book):
        with open(self.filename, "wb") as f:
            pickle.dump(book, f)

    def load(self):
        try:
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()
