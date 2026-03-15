import sys
import threading
import time

from .ui import print_done, print_error


class ChangeEventsWatcher:
    def __init__(self, db, interval_seconds=1.0, prompt=""):
        self.db = db
        self.interval_seconds = interval_seconds
        self.prompt = prompt
        self._last_event_id = 0
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._last_event_id = self.db.latest_event_id(source="mcp")
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)

    def _run(self):
        while not self._stop_event.is_set():
            events = self.db.fetch_events(after_id=self._last_event_id, source="mcp")
            for event in events:
                self._last_event_id = max(self._last_event_id, event["id"])
                sys.stdout.write("\r\033[K")  # clear current input line
                if event["level"] == "error":
                    print_error(event["message"])
                else:
                    print_done(event["message"])
                sys.stdout.write(self.prompt)
                sys.stdout.flush()
            time.sleep(self.interval_seconds)