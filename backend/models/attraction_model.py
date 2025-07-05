"""Describe a ride."""

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field, HttpUrl


class AttractionType(StrEnum):
    """Store the type of the ride."""

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
    TOP_SCAN = "Top Scan"
    LOOP_FIGHTER = "Loop Fighter"
    INVERTED_RIDES = "Inverted Rides"
    FLAT_RIDE = "Flat ride"
    SHAKE = "Shake"
    BOOSTER = "Booster"
    ROUND_UP = "Round up"

    @staticmethod
    def from_value(value: str) ->  None:
        """"Get the enum from its value."""
        for e in AttractionType:
            if e.value == value:
                return e
        return None

class AttractionImage(BaseModel):
    """Register an image, it can be from url or locally stored."""

    id: str
    attraction_id: str = Field(description="many to one key cheat")
    url: HttpUrl | None = Field(default=None, description="url to the image")
    path: Path | None = Field(default=None, description="path of the image")

    def is_url(self) -> bool:
        """Tell if the image is an url."""
        return self.url is not None

    def is_path(self) -> bool:
        """Tell if the image is a stored locally."""
        return self.path is not None

class Attraction(BaseModel):
    """Describe a ride, the minimal is the name."""

    id: str
    name: str = Field(..., description="Name of the attraction")
    owner: str | None = Field(default=None, description="Family owner name")
    description: str | None = Field(
        default=None, description="Short description of the attraction",
    )
    ticket_price: float | None = Field(
        default=None, description="Additional ticket price for the attraction, if any",
        ge=.0,
    )
    manufacturer_id: str | None = Field(
        default=None, description="Manufacturer of the attraction",
    )
    technical_name: str | None = Field(
        default=None, description="Technical name of the attraction",
    )
    attraction_type: AttractionType | None = Field(
        default=None, description="Type of the attraction (e.g., roller coaster, carousel)",
    )

    images_url: list[HttpUrl] = Field(default_factory=list, description="some images")
    videos_url: list[HttpUrl] = Field(default_factory=list, description="some videos")
    manufacturer_page_url: HttpUrl | None = Field(
        default=None, description="page of the manufacturer",
    )
    news_page_url: HttpUrl | None = Field(
        default=None, description="official or fan page of the attraction",
    )
