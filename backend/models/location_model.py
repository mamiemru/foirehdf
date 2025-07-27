"""Describe a location instance."""
from typing import Annotated

from pydantic import BaseModel, Field


class LocationBase(BaseModel):
    """Describe a location."""

    street: Annotated[str | None, Field(None, description="Street where its situated")]
    area: Annotated[str | None, Field(None, description="Area where the location is situated")]

    city: Annotated[str, Field(..., description="City or town where the location is situated.")]
    postal_code: Annotated[str, Field(..., description="Postal code code for the location.")]
    state: Annotated[str, Field(..., description="State or province")]
    country: Annotated[str, Field(..., description="Country where the location exists.")]

    lat: Annotated[float | None, Field(None,description="Latitude value between -90 and 90.")]
    lng: Annotated[float | None, Field(None, description="Longitude value between -180 and 180.")]


class Location(LocationBase):
    """Describe a location with its id."""

    id: Annotated[str, Field(..., description="id")]
