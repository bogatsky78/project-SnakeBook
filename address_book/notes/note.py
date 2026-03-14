from datetime import datetime, timezone

from colorama import Fore, Style


class Note:
    def __init__(self, key, text, created_at=None):
        self.key = key
        self.text = text
        self.created_at = created_at or datetime.now(timezone.utc).isoformat(timespec="microseconds")

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        value = value.strip()
        if not value or any(char.isspace() for char in value):
            raise ValueError("Note key must be a single word.")
        self._key = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Note text cannot be empty.")
        self._text = value

    def edit_text(self, new_text):
        self.text = new_text

    def save(self, db):
        db.save_note(self)

    def formatted_created_at(self):
        created_at = datetime.fromisoformat(self.created_at)
        return created_at.strftime("%b %d, %Y at %H:%M UTC")

    def __str__(self):
        label_style = Style.DIM
        key_style = Style.BRIGHT + Fore.CYAN
        time_style = Fore.YELLOW
        text_style = Style.NORMAL + Fore.WHITE

        return (
            f"{label_style}Note key:{Style.RESET_ALL} {key_style}{self.key}{Style.RESET_ALL}, "
            f"{label_style}created at:{Style.RESET_ALL} {time_style}{self.formatted_created_at()}{Style.RESET_ALL}, "
            f"{label_style}text:{Style.RESET_ALL} {text_style}{self.text}{Style.RESET_ALL}"
        )
