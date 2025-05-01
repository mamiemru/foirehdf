
from enum import StrEnum
from pathlib import Path
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl, field_validator, field_serializer

class AttractionType(StrEnum):
    ROLLER_COASTER = "roller coaster"
    CAROUSEL = "carousel"
    FERRIS_WHEEL = "ferris wheel"
    SLIDE = "slide"
    FRISBEE = "Frisbee"
    PENDULUM = "Pendulum"
    ROTOR = "Rotor"
    ORBITER = "Orbiter"
    DROP_TOWER = "Drop Tower"
    TOP_SPIN = "Top Spin"
    LOOP_FIGHTER = "Loop Fighter"
    INVERTED_RIDES = "Inverted Rides"
    SHAKE = "Shake"
    BOOSTER = "Booster"
    ROUND_UP = "Round up"

    @staticmethod
    def from_value(value: str):
        for e in AttractionType:
            if e.value == value:
                return e
        return None

class AttractionImage(BaseModel):
    id: str
    attraction_id: str = Field(description="many to one key cheat")
    url: Optional[HttpUrl] = Field(default=None, description="url to the image")
    path: Optional[Path] = Field(default=None, description="path of the image")

    def is_url(self):
        return self.url is not None

    def is_path(self):
        return self.path is not None

class Attraction(BaseModel):
    id: str
    name: str = Field(..., description="Name of the attraction")
    owner: Optional[str] = Field(default=None, description="Family owner name")
    description: Optional[str] = Field(default=None, description="Short description of the attraction")
    ticket_price: Optional[float] = Field(default=None, description="Additional ticket price for the attraction, if any")
    manufacturer_id: Optional[str] = Field(..., description="Manufacturer of the attraction")
    technical_name: Optional[str] = Field(default=None, description="Technical name of the attraction")
    attraction_type: AttractionType = Field(..., description="Type of the attraction (e.g., roller coaster, carousel)"),

    images_url: Optional[List[HttpUrl]] = Field(default=[], description="some images")
    videos_url: Optional[List[HttpUrl]] = Field(default=[], description="some videos")
    manufacturer_page_url: Optional[HttpUrl] = Field(default=None, description="page of the manufacturer")
    news_page_url: Optional[HttpUrl] = Field(default=None, description="official or fan page of the attraction")

    @field_serializer("manufacturer_page_url", "news_page_url")
    def serialize_url(url: str):
        return str(url) if url else None

    @field_serializer("videos_url", "images_url")
    def serialize_urls(urls: List[str]):
        return [str(url) if url else None for url in urls]

    @field_validator("name", "manufacturer_id", mode="before")
    def non_empty_string(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Must not be empty or blank")
        return value.strip()
    
    @field_validator("ticket_price")
    def ticket_price_non_negative(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Ticket price must be non-negative")
        return value
