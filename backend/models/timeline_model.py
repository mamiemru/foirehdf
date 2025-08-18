
from enum import StrEnum
from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field

from backend.models.annotated import DATETIME_VALIDATION, OPTIONAL_STR


class TimelineItemType(StrEnum):
    """
    Describe a timeline item type.

    Args:
        enum (_type_): _description_

    """

    FAIR_START = "fair_start"
    FAIR_END = "fair_end"
    RIDE_AVAILABLE = "ride_available"
    RIDE_LEAVING = "ride_leaving"

class TimelineItem(BaseModel):
    """Describe an item in a timeline structure."""

    type: TimelineItemType | None = Field(default=None)
    title: str = Field(...)
    ride: OPTIONAL_STR = Field(default=None)
    description: OPTIONAL_STR = Field(default=None)
    date: DATETIME_VALIDATION = Field(...)

class Timeline(BaseModel):
    """Describe all events of a fair."""

    line: Annotated[list[TimelineItem], AfterValidator(lambda l: sorted(l, key=lambda i: i.date, reverse=True))] = Field(default_factory=list)
