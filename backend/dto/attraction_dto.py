import dataclasses
from pathlib import Path


@dataclasses.dataclass
class AttractionImageDTO:
    id: str
    path: Path

@dataclasses.dataclass
class AttractionDTO:
    id: str
    name: str
    description: str
    ticket_price: float
    manufacturer: str
    technical_name: str
    attraction_type: str
    images: list[AttractionImageDTO]
    owner: str | None
    videos_url: list[str] | None
    images_url: list[str] | None
    manufacturer_page_url: str | None
    news_page_url: str | None
