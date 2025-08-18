


from datetime import date, datetime
from typing import Annotated

from pydantic import BeforeValidator, HttpUrl


def datetime_validation_func(value: float | str | date | datetime) -> datetime:
    """
    Parse any date format int datetime.

    Args:
        value (float | str | date | datetime): the date to parse

    Raises:
        ValueError: the date content is wrong
        TypeError: the date format is not supported

    Returns:
        datetime: the parsed date in datetime

    """
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str):
        if not value:
            msg = f"Empty datetime string: {value!r}"
            raise ValueError(msg)
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            msg = f"Invalid datetime string: {value!r}"
            raise ValueError(msg)
    if isinstance(value, (int, float)):
        if value <= 0:
            msg = "Timestamp must be positive"
            raise ValueError(msg)
        return datetime.fromtimestamp(value)
    msg = f"Invalid type for timestamp: {type(value).__name__}"
    raise ValueError(msg)


URL_VALIDATION = Annotated[HttpUrl | None, BeforeValidator(lambda url: url or None)]
URLS_VALIDATION = Annotated[list[HttpUrl], BeforeValidator(lambda urls: [url for url in urls if url])]
DATETIME_VALIDATION = Annotated[datetime, BeforeValidator(datetime_validation_func)]
OPTIONAL_STR = Annotated[str | None, BeforeValidator(lambda s: str(s) if s else None)]
