import dataclasses

from pathlib import Path
from typing import List, Optional


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
    images: List[AttractionImageDTO]
    owner: Optional[str]
    videos_url: Optional[List[str]]
    images_url: Optional[List[str]]
    manufacturer_page_url: Optional[str]
    news_page_url: Optional[str]
