import dataclasses
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
    sources: List[HttpUrl] = Field(default=[], description="Useful sources of the event")

    @field_serializer("sources")
    def serialize_urls(urls: List[str]):
        return [str(url) if url else None for url in urls]

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

@dataclasses.dataclass
class FairDTO:
    id: str
    name: str
    location: LocationDTO
    start_date: date
    end_date: date
    fair_status: str
    attractions: List[AttractionDTO] = None
    sources: Optional[List[HttpUrl]] = None
    fair_done: bool = True
    fair_incoming: bool = False
    fair_available_today: bool = False
    image: str = None

