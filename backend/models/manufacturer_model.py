"""Class describing a manufacturer."""
from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl


class Manufacturer(BaseModel):
    """Represente a manuacturer class."""

    id: Annotated[str, Field(..., description="id")]
    name: Annotated[str, Field(..., description="Name of the manufacturer", min_length=3)]
    website_url: Annotated[HttpUrl | None, Field(default=None, description="manufacturer site")]
