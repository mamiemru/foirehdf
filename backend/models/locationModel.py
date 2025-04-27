import dataclasses

from pydantic import BaseModel, Field, field_validator
from typing import Optional

class LocationForm(BaseModel):
    street: Optional[str]
    area: Optional[str]
    city: str
    postal_code: str
    state: str
    country: str
    lat: Optional[float]
    lng: Optional[float]


class Location(BaseModel):
    id: str = Field(..., description="id")

    street: Optional[str] = Field(None, description="Street where the location is situated")
    area: Optional[str] = Field(None, description="Area where the location is situated")

    city: str = Field(..., description="City or town where the location is situated.")
    postal_code: str = Field(..., description="Postal code or ZIP code for the location.")
    state: str = Field(..., description="State or province (optional for countries without this division).")
    country: str = Field(..., description="Country where the location exists.")

    lat: Optional[float] = Field(None,description="Latitude value between -90 and 90.")
    lng: Optional[float] = Field(None, description="Longitude value between -180 and 180.")

    @field_validator('city', 'state', 'city')
    def non_empty_string(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Must not be empty or blank")
        return value.strip()

    @field_validator('postal_code')
    def validate_postal_code_format(cls, v):
        if v and not any(char.isdigit() for char in v):
            raise ValueError("Postal code must contain at least one number.")
        return v

@dataclasses.dataclass
class LocationDTO:
    id: str
    street: Optional[str]
    area: Optional[str]
    city: str
    postal_code: str
    state: str
    country: str
    lat: Optional[float]
    lng: Optional[float]
