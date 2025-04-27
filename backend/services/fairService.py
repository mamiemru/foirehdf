import datetime
import uuid

from tinydb import TinyDB, Query
from typing import Optional

from backend.models.fairModel import Fair
from backend.models.fairModel import FairDTO
from backend.models.locationModel import LocationDTO, Location
from backend.services.attractionService import attraction_to_dto, get_attraction_by_id
from backend.services.locationService import location_to_dto, get_location_by_id

tinydb = TinyDB("fair_db.json")
db = tinydb.table("fair")
FairQuery = Query()

def _create_id():
    return str(uuid.uuid4())

def _date_to_timestamp(date: datetime.date) -> float:
    datetime_obj = datetime.datetime.combine(date, datetime.datetime.min.time())
    timestamp = datetime_obj.timestamp()
    return timestamp

def _timestamp_to_date(timestamp: float) -> datetime.date:
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    date_object = dt_object.date()
    return date_object

def fair_to_dto(fair: Fair) -> FairDTO:
    location: Location = get_location_by_id(fair.location_id)

    fair_dict: dict = fair.model_dump(mode="json")

    return FairDTO(
        id=fair_dict['id'],
        name=fair_dict['name'],
        location=location_to_dto(location) if location else None,
        start_date=_timestamp_to_date(fair.start_date),
        end_date=_timestamp_to_date(fair.end_date),
        sources=fair_dict['sources'],
        attractions=list(),
        fair_done=fair.fair_done,
        fair_incoming=fair.fair_incoming,
        fair_available_today=fair.fair_available_today,
        fair_status=fair.fair_status
    )

def fair_to_dto_detailed(fair: Fair) -> FairDTO:
    fair_dto: FairDTO = fair_to_dto(fair)
    fair_dto.attractions = [
        get_attraction_by_id(attraction) for attraction in fair.attractions
    ]
    return fair_dto

def validate_fair(fair_dict: dict) -> Fair:
    return Fair.model_validate(
        {
            'id': _create_id(),
            'name': fair_dict['name'],
            'location_id': fair_dict['location_id'],
            'start_date': _date_to_timestamp(fair_dict['start_date']),
            'end_date': _date_to_timestamp(fair_dict['end_date']),
            'sources': fair_dict.get('sources', []),
            'attractions': fair_dict['attractions']
        }
    )


def save_fair(fair: Fair) -> bool:
    success = db.insert(fair.model_dump(mode="json"))
    return bool(success)

def list_fairs(name: Optional[str] = None, location: Optional[str] = None):
    query = (FairQuery.name == name) if name else (FairQuery.location == location) if location else None
    results = db.search(query) if query else db.all()
    return [fair_to_dto(Fair(**result)) for result in results]

def get_fair(id: str) -> FairDTO:
    result = db.get(FairQuery.id == id)
    if result:
        fair: Fair = Fair(**result)
        return fair_to_dto(fair)
    return None

def get_fair_detailed(id: str) -> FairDTO:
    result = db.get(FairQuery.id == id)
    if result:
        fair: Fair = Fair(**result)
        return fair_to_dto_detailed(fair)
    return None

def update_fair(id: str, updated_fair: Fair):
    pass

def delete_fair(id: str):
    db.remove(FairQuery.id == id)
    return f"Fair '{id}' has been deleted."
