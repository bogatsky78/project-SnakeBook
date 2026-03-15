import inspect
from functools import wraps

from .database import Database
from .services import SnakeBookService

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("Missing dependency: install 'mcp' to run the MCP server.") from exc


mcp = FastMCP("SnakeBook")


def _run_with_service(fn=None, *, log_changes=False):
    def decorator(inner_fn):
        @wraps(inner_fn)
        def wrapper(*args, **kwargs):
            db = Database(filename="addressbook.db")
            book = db.load()
            service = SnakeBookService(book)
            try:
                result = inner_fn(service, *args, **kwargs)
                if log_changes:
                    db.log_event(result.message, source="mcp", level="done")
                return {
                    "status": result.status,
                    "message": result.message,
                    "payload": result.payload,
                }
            except (IndexError, TypeError, ValueError, KeyError) as exc:
                return {
                    "status": "error",
                    "message": str(exc),
                    "payload": None,
                }

        # Strip the first 'service' parameter so FastMCP doesn't expose it
        sig = inspect.signature(inner_fn)
        params = list(sig.parameters.values())
        if params and params[0].name == "service":
            params = params[1:]
        wrapper.__signature__ = sig.replace(parameters=params)

        return wrapper

    if fn is None:
        return decorator
    return decorator(fn)


@mcp.tool()
@_run_with_service
def contacts_list(service):
    return service.list_contacts()


@mcp.tool()
@_run_with_service
def contact_show(service, name: str):
    return service.get_contact(name)


@mcp.tool()
@_run_with_service
def contacts_search(service, query: str):
    return service.search_contacts(query)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_add(service, name: str, phone: str, birthday: str | None = None, email: str | None = None, address: str | None = None):
    return service.add_contact(name, phone, birthday=birthday, email=email, address=address)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_change_phone(service, name: str, old_phone: str, new_phone: str):
    return service.change_contact_phone(name, old_phone, new_phone)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_remove(service, name: str):
    return service.remove_contact(name)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_add_phone(service, name: str, phone: str):
    return service.add_phone(name, phone)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_remove_phone(service, name: str, phone: str):
    return service.remove_phone(name, phone)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_add_birthday(service, name: str, birthday: str):
    return service.add_birthday(name, birthday)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_add_email(service, name: str, email: str):
    return service.add_email(name, email)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_change_email(service, name: str, email: str):
    return service.change_email(name, email)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_remove_email(service, name: str):
    return service.remove_email(name)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_add_address(service, name: str, address: str):
    return service.add_address(name, address)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_change_address(service, name: str, address: str):
    return service.change_address(name, address)


@mcp.tool()
@_run_with_service(log_changes=True)
def contact_remove_address(service, name: str):
    return service.remove_address(name)


@mcp.tool()
@_run_with_service
def notes_list(service):
    return service.list_notes()


@mcp.tool()
@_run_with_service
def note_show(service, note_id: int):
    return service.get_note(note_id)


@mcp.tool()
@_run_with_service
def notes_search(service, query: str):
    return service.search_notes(query)


@mcp.tool()
@_run_with_service(log_changes=True)
def note_add(service, text: str):
    return service.add_note(text)


@mcp.tool()
@_run_with_service(log_changes=True)
def note_edit(service, note_id: int, text: str):
    return service.edit_note(note_id, text)


@mcp.tool()
@_run_with_service(log_changes=True)
def note_remove(service, note_id: int):
    return service.remove_note(note_id)


def main():
    mcp.run()


if __name__ == "__main__":
    main()