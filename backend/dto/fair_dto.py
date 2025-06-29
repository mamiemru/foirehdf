import dataclasses
from datetime import datetime

from typing import List, Optional
from pydantic import HttpUrl

from backend.dto.attraction_dto import AttractionDTO
from backend.models.locationModel import LocationDTO

@dataclasses.dataclass
class FairBaseDTO:
    id: str
    name: str
    location: LocationDTO
    locations: List[LocationDTO]
    start_date: datetime
    end_date: datetime
    fair_status: str
    days_before_start_date: Optional[int]
    days_before_end_date: Optional[int]
    attractions: List[AttractionDTO] = None
    fair_done: bool = True
    fair_incoming: bool = False
    fair_available_today: bool = False


@dataclasses.dataclass
class FairDTO(FairBaseDTO):
    sources: Optional[List[HttpUrl]] = None
    image: str = None
    official_ad_page: Optional[str] = None
    city_event_page: Optional[str] = None
    walk_tour_video: Optional[str] = None
    facebook_event_page: Optional[str] = None
