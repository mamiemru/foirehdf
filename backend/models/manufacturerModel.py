
from pydantic import BaseModel, Field

class ManufacturerForm(BaseModel):
    name: str

class Manufacturer(BaseModel):
    id: str = Field(..., description="id")
    name: str = Field(..., description="Name of the manufacturer", min_length=3)
