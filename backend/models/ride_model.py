"""Describe a ride."""

from enum import StrEnum

from bson.objectid import ObjectId
from pydantic import BaseModel, Field, HttpUrl


class RideType(StrEnum):
    """Store the type of the ride."""

    NA = ""
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
        for e in RideType._value2member_map_:
            if e.value == value:
                return e
        return None

class ManufacturerRide(BaseModel):
    """A ride from the manufacturer, its the kinds of information you have when browsing manufacturer's rides."""

    manufacturer_ride_id: str = Field(default_factory=lambda:str(ObjectId()), description="unique id of the manufactured ride")
    manufacturer: str | None = Field(default=None, description="Manufacturer name of the ride")
    technical_name: str | None = Field(default=None, description="Technical name of the ride")
    ride_type: RideType | None = Field(default=None, description="Type of the ride (e.g., roller coaster, carousel)")
    manufacturer_page_url: HttpUrl | None = Field(default=None, description="page of the manufacturer")
    description: str | None = Field(default=None, description="Short description of the ride")

class Ride(ManufacturerRide):
    """Describe a ride owned by a fraiground worker, the minimal is the name."""

    id: str = Field(default_factory=lambda:str(ObjectId()))
    name: str = Field(..., description="Name of the ride")
    owner: str | None = Field(default=None, description="Family owner name")
    ticket_price: float | None = Field(default=None, description="Additional ticket price for the ride, if any", ge=.0)
    images_url: list[HttpUrl] = Field(default_factory=list, description="some images")
    videos_url: list[HttpUrl] = Field(default_factory=list, description="some videos")
    news_page_url: HttpUrl | None = Field( default=None, description="official or fan page of the ride" )
