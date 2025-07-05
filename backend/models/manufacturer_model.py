"""Class describing a manufacturer."""
from pydantic import BaseModel, Field, HttpUrl


class Manufacturer(BaseModel):
    """
    Represente a manuacturer class.

    Args:
        BaseModel (_type_): pydantic basemodel

    """

    id: str = Field(..., description="id")
    name: str = Field(..., description="Name of the manufacturer", min_length=3)
    website_url: HttpUrl | None = Field(default=None, description="manufacturer site")
