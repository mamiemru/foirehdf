
from datetime import date, datetime
from enum import StrEnum
from typing import Annotated

from bson.objectid import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, HttpUrl, field_validator

from .location_model import LocationBase


class FairStatus(StrEnum):
    """
    Describe the status of a fair.

    Args:
        enum (_type_): _description_

    """

    INCOMING = "incoming"
    CURRENTLY_AVAILABLE = "currently available"
    DONE = "done"

def timestamp_to_datetime(value: float | str | date | datetime) -> datetime:
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
        # Convert date (which has no time) to datetime
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            msg = f"Invalid timestamp string: {value!r}"
            raise TypeError(msg)
    if isinstance(value, (int, float)):
        if value <= 0:
            msg = "Timestamp must be positive"
            raise ValueError(msg)
        return datetime.fromtimestamp(value)
    msg = f"Invalid type for timestamp: {type(value).__name__}"
    raise TypeError(msg)

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

    id: Annotated[str, Field(default_factory=lambda:str(ObjectId()), description="id")]
    name: Annotated[str, Field(..., description="Name of the fair", min_length=3)]
    locations: Annotated[list[LocationBase], Field(default_factory=list, description="locations")]
    start_date: TimestampDatetime = Field(..., description="Start timestamp of the fair")
    end_date: TimestampDatetime = Field(..., description="End timestamp of the fair")
    rides: Annotated[list[str], Field(default_factory=list, description="List of ids of rides")]

    @property
    def fair_status(self) -> FairStatus | str:
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

    city_event_page: Annotated[HttpUrl | None, Field(default=None, description="city event page")]
    official_ad_page: Annotated[HttpUrl | None, Field(default=None, description="official_ad_page")]
    walk_tour_video: Annotated[HttpUrl | None, Field(default=None, description="walk_tour_video")]
    facebook_event_page: Annotated[HttpUrl | None, Field(default=None, description="facebook_event_page")]
    sources: Annotated[list[HttpUrl], Field(default_factory=list, description="Useful sources of the event")]
    images: Annotated[list[str], Field(default_factory=list)]

    @field_validator("city_event_page", "official_ad_page", "walk_tour_video", "facebook_event_page")
    def valide_optional_url(v) -> HttpUrl | None:
        """Make sure the value is a valid url otherwise None."""
        return HttpUrl(v) if v else None
