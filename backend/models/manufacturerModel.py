
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

class ManufacturerForm(BaseModel):
    name: str
    website_url: str

class Manufacturer(BaseModel):
    id: str = Field(..., description="id")
    name: str = Field(..., description="Name of the manufacturer", min_length=3)
    website_url: Optional[HttpUrl] = Field(default=None, description="url of the manufacturer site")
