import dataclasses
import datetime
import enum
import time
from datetime import date

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, PositiveFloat
from pydantic import field_validator, field_serializer

from backend.dto.attraction_dto import AttractionDTO
from backend.models.locationModel import LocationForm, LocationDTO


class FairStatus(enum.StrEnum):
    INCOMING = "incoming"
    CURRENTLY_AVAILABLE = "currently available"
    DONE = "done"

class FairCreateForm(BaseModel):
    name: str
    location: LocationForm
    start_date: date
    end_date: date

class Fair(BaseModel):
    id: str = Field(..., description="id")
    name: str = Field(..., description="Name of the fair", min_length=3)
    location_id: str = Field(..., description="id Location of the fair", min_length=3)
    start_date: PositiveFloat = Field(..., description="Start timestamp of the fair")
    end_date: PositiveFloat = Field(..., description="End timestamp of the fair")
    attractions: List[str] = Field(..., description="List of ids of attractions at the fair")
    city_event_page: Optional[HttpUrl] = Field(default=None, descriptio="city event page")
    official_ad_page: Optional[HttpUrl] = Field(default=None, descriptio="official_ad_page")
    walk_tour_video: Optional[HttpUrl] = Field(default=None, descriptio="walk_tour_video")
    facebook_event_page: Optional[HttpUrl] = Field(default=None, descriptio="facebook_event_page")
    sources: List[HttpUrl] = Field(default=[], description="Useful sources of the event")

    @field_serializer("sources")
    def serialize_urls(urls: List[str]):
        return [str(url) if url else None for url in urls]

    @field_serializer("official_ad_page","city_event_page", "walk_tour_video", "facebook_event_page")
    def serialize_url(url: str):
        return str(url) if url else None

    @field_validator("official_ad_page","city_event_page", "walk_tour_video", "facebook_event_page")
    def validate_optional_url(cls, url: str) -> HttpUrl | None:
        if url:
            if isinstance(url, HttpUrl):
                return url
            return HttpUrl(url)
        return None

    @field_validator("id","name", 'location_id', mode="before")
    def non_empty_string(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Must not be empty or blank")
        return value.strip()

    @field_validator('start_date', 'end_date', mode="before")
    def non_empty_float(cls, value: float) -> float:
        if not value or not isinstance(value, float):
            raise ValueError("Must be a valid field")
        return value

    @property
    def fair_status(self) -> FairStatus:
        if self.fair_available_today:
            return FairStatus.CURRENTLY_AVAILABLE
        if self.fair_incoming:
            return FairStatus.INCOMING
        return FairStatus.DONE

    @property
    def fair_available_today(self):
        return self.start_date < time.time() < self.end_date

    @property
    def fair_incoming(self):
        return time.time() < self.start_date

    @property
    def fair_done(self):
        return self.end_date < time.time()

    @property
    def days_before_start_date(self):
        if self.fair_incoming:
            return (datetime.datetime.fromtimestamp(self.start_date) - datetime.datetime.now()).days
        return None

    @property
    def days_before_end_date(self):
        if self.fair_available_today:
            return (datetime.datetime.fromtimestamp(self.end_date) - datetime.datetime.now()).days
        return None

@dataclasses.dataclass
class FairDTO:
    id: str
    name: str
    location: LocationDTO
    start_date: str
    end_date: str
    fair_status: str
    days_before_start_date: Optional[int]
    days_before_end_date: Optional[int]
    attractions: List[AttractionDTO] = None
    sources: Optional[List[HttpUrl]] = None
    fair_done: bool = True
    fair_incoming: bool = False
    fair_available_today: bool = False
    image: str = None
    official_ad_page: Optional[str] = None
    city_event_page: Optional[str] = None
    walk_tour_video: Optional[str] = None
    facebook_event_page: Optional[str] = None
