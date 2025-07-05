import gettext
import locale
from pathlib import Path

locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

locale_path = Path(__file__).parent.parent / "locales"
language = gettext.translation("messages", localedir=locale_path, languages=["fr"])
language.install()

_ = language.gettext
