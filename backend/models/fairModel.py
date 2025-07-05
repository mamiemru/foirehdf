
import enum
from datetime import date, datetime
from typing import Annotated

from bson.objectid import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, HttpUrl

from .location_model import LocationBase


class FairStatus(enum.StrEnum):
    """
    Describe the status of a fair.

    Args:
        enum (_type_): _description_

    """

    INCOMING = "incoming"
    CURRENTLY_AVAILABLE = "currently available"
    DONE = "done"

def timestamp_to_datetime(value: float | str | date | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        # Convert date (which has no time) to datetime
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            raise TypeError(f"Invalid timestamp string: {value!r}")
    if isinstance(value, (int, float)):
        if value <= 0:
            raise ValueError("Timestamp must be positive")
        return datetime.fromtimestamp(value)
    raise TypeError(f"Invalid type for timestamp: {type(value).__name__}")

TimestampDatetime = Annotated[
    datetime,
    BeforeValidator(timestamp_to_datetime),
]

class FairBase(BaseModel):
    """
    A fair base is a fair with the strict minimal of datas to make something usefull.

    They are also stored in different table unlike regular fair,
    fairBase are not displayed in the list of fair, there only purpose is to keep track
    of rides when outside the 62-59 (postal code).
    No one know in the future i would include belgium or 02 (postal code).
    """

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.timestamp()},
    )

    id: str = Field(default_factory=lambda:str(ObjectId()), description="id")
    name: str = Field(..., description="Name of the fair", min_length=3)
    locations: list[LocationBase] = Field(default_factory=list, description="locations")
    start_date: TimestampDatetime = Field(..., description="Start timestamp of the fair")
    end_date: TimestampDatetime = Field(..., description="End timestamp of the fair")
    attractions: list[str] = Field(..., description="List of ids of attractions")

    @property
    def fair_status(self) -> FairStatus:
        """Tell what is the status of a fair right now."""
        if self.fair_available_today:
            return FairStatus.CURRENTLY_AVAILABLE
        if self.fair_incoming:
            return FairStatus.INCOMING
        return FairStatus.DONE

    @property
    def fair_available_today(self) -> bool:
        """Tell if a fair is available right now."""
        return self.start_date < datetime.now() < self.end_date

    @property
    def fair_incoming(self) -> bool:
        """Tell if a fair is comming soon."""
        return datetime.now() < self.start_date

    @property
    def fair_done(self) -> bool:
        """Tell if a fair is done."""
        return self.end_date < datetime.now()

    @property
    def days_before_start_date(self) -> int | None:
        """Tell how many days to wait before a fair open from right now. else None."""
        if self.fair_incoming:
            return ((self.start_date - datetime.now()).days)+1
        return None

    @property
    def days_before_end_date(self) -> int | None:
        """Tell how many days the fair will stay available from right now, else None."""
        if self.fair_available_today:
            return (self.end_date - datetime.now()).days
        return None


class Fair(FairBase):
    """Describe a Fair with sources."""

    city_event_page: HttpUrl | None = Field(default=None, description="city event page")
    official_ad_page: HttpUrl | None = Field(default=None, description="official_ad_page")
    walk_tour_video: HttpUrl | None = Field(default=None, description="walk_tour_video")
    facebook_event_page: HttpUrl | None = Field(default=None, description="facebook_event_page")
    sources: list[HttpUrl] = Field(default_factory=list, description="Useful sources of the event")
    images: list[str] = Field(default_factory=list)
