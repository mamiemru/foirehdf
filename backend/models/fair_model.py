
from datetime import date, datetime
from enum import StrEnum
from typing import Annotated, Any

from bson.objectid import ObjectId
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from backend.models.annotated import DATETIME_VALIDATION, URL_VALIDATION, URLS_VALIDATION
from backend.models.timeline_model import Timeline

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
    start_date: DATETIME_VALIDATION = Field(..., description="Start timestamp of the fair")
    end_date: DATETIME_VALIDATION = Field(..., description="End timestamp of the fair")
    rides: Annotated[list[str], Field(default_factory=list, description="List of ids of rides")]
    timeline: Timeline | None = Field(default=None)

    def locations_str(self) -> list[str]:
        """
        Return a list of each locations in string.

        Returns:
            list[str]: list of locations in string.

        """
        return [location.location_to_str() for location in self.locations]

    def first_location_str(self) -> str:
        """Return the first location in string."""
        if not self.locations:
            msg = "A fait has no locations"
            raise ValueError(msg)
        return self.locations[0].location_to_str()

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

    city_event_page: URL_VALIDATION = Field(default=None, description="city event page")
    official_ad_page: URL_VALIDATION = Field(default=None, description="official_ad_page")
    walk_tour_video:  URL_VALIDATION = Field(default=None, description="walk_tour_video")
    facebook_event_page:  URL_VALIDATION = Field(default=None, description="facebook_event_page")
    sources: URLS_VALIDATION = Field(default_factory=list, description="Useful sources of the event")
    images: list[str] = Field(default_factory=list)

    @field_validator("city_event_page", "official_ad_page", "walk_tour_video", "facebook_event_page")
    def valide_optional_url(v) -> HttpUrl | None:
        """Make sure the value is a valid url otherwise None."""
        return HttpUrl(v) if v else None


class SearchFairQuery(BaseModel):
    """Search fair query params to search filter through fairs."""

    date_min: date = Field(default=(datetime.now() - relativedelta(months=1)).date())
    date_max: date = Field(default=(datetime.now() + relativedelta(months=6)).date())
    cities: list[str] = Field(default_factory=list)

    def reset(self) -> None:
        """Reset search query filters to default."""
        self.date_min = (datetime.now() - relativedelta(months=1)).date()
        self.date_max = (datetime.now() + relativedelta(months=6)).date()
        self.cities.clear()

class SearchFairMap(BaseModel):
    """Structurer fair search map."""

    color: str
    lng: float
    lat: float
    size: int


class SearchFairResult(BaseModel):
    """Structured fair search results."""

    fairs: dict[str, list[Fair]] = Field(default_factory=lambda: {s.value: [] for s in FairStatus})
    map: list[SearchFairMap] = Field(default_factory=list)
    gantt: Any = Field(...)

class FairCreateInput(BaseModel):
    """Describe the inputs to create a fair."""

    name: str
    start_date: date
    end_date: date
    locations: list[str] = Field(default_factory=list)
    rides: list[str] = Field(default_factory=list)
    walk_tour_video: URL_VALIDATION
    official_ad_page: URL_VALIDATION
    facebook_event_page: URL_VALIDATION
    city_event_page: URL_VALIDATION
