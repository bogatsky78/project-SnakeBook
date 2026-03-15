from datetime import datetime, timezone
from colorama import Fore, Style

class Note:
    def __init__(self, id, text, created_at=None):
        self.id = id  # None for new notes; assigned by the DB after the first save
        self.text = text
        self.created_at = created_at or datetime.now(timezone.utc).isoformat(timespec="microseconds")

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
        id_style = Style.BRIGHT + Fore.CYAN
        time_style = Fore.YELLOW
        text_style = Style.NORMAL + Fore.WHITE

        return (
            f"{label_style}Note ID:{Style.RESET_ALL} {id_style}{self.id}{Style.RESET_ALL}, "
            f"{label_style}created at:{Style.RESET_ALL} {time_style}{self.formatted_created_at()}{Style.RESET_ALL}, "
            f"{label_style}text:{Style.RESET_ALL} {text_style}{self.text}{Style.RESET_ALL}"
        )
