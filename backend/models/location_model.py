"""Describe a location instance."""

from pydantic import BaseModel, Field


class LocationBase(BaseModel):
    """Describe a location."""

    street: str | None = Field(None, description="Street where its situated")
    area: str | None = Field(None, description="Area where the location is situated")

    city: str = Field(..., description="City or town where the location is situated.")
    postal_code: str = Field(..., description="Postal code code for the location.")
    state: str = Field(..., description="State or province")
    country: str = Field(..., description="Country where the location exists.")

    lat: float | None = Field(None,description="Latitude value between -90 and 90.")
    lng: float | None = Field(None, description="Longitude value between -180 and 180.")


class Location(LocationBase):
    """Describe a location with its id."""

    id: str = Field(..., description="id")
