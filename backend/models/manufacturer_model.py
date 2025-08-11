"""Class describing a manufacturer."""

from pydantic import BaseModel, Field

from backend.models.annotated import URL_VALIDATION


class Manufacturer(BaseModel):
    """Represente a manuacturer class."""

    id: str = Field(..., description="id")
    name: str = Field(..., description="Name of the manufacturer", min_length=3)
    website_url: URL_VALIDATION = Field(default=None, description="manufacturer site")
