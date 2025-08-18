"""Describe a location instance."""
from typing import Annotated

from pydantic import BaseModel, Field

from backend.models.annotated import OPTIONAL_STR


class LocationBase(BaseModel):
    """Describe a location."""

    street: OPTIONAL_STR = Field(None, description="Street where its situated")
    area: OPTIONAL_STR = Field(None, description="Area where the location is situated")

    city: Annotated[str, Field(..., description="City or town where the location is situated.")]
    postal_code: Annotated[str, Field(..., description="Postal code code for the location.")]
    state: Annotated[str, Field(..., description="State or province")]
    country: Annotated[str, Field(..., description="Country where the location exists.")]

    lat: Annotated[float | None, Field(None,description="Latitude value between -90 and 90.")]
    lng: Annotated[float | None, Field(None, description="Longitude value between -180 and 180.")]

    def location_to_str(self) -> str:
        """Return a location in string."""
        return f"""{self.street or ""} {self.area or ""} {self.city} {self.postal_code}, {self.state} {self.country}"""

class Location(LocationBase):
    """Describe a location with its id."""

    id: Annotated[str, Field(..., description="id")]

