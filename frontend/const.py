import gettext
import locale
from pathlib import Path

locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

locale_path = Path(__file__).parent.parent / "locales"
language = gettext.translation("messages", localedir=locale_path, languages=["fr"])
language.install()

_ = language.gettext


def mandatory_field_value(value: str) -> str:
    """Return a translated field with an asterix meaning the field is required."""
    return f"{_(value)}*"


def field_value(value: str) -> str:
    """Return a translated field."""
    return f"{_(value)}"
