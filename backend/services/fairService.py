from dataclasses import asdict
import datetime
import locale
from bson import ObjectId

from tinydb import TinyDB, Query
from typing import List, Optional

from backend.models.fairModel import Fair, FairBase, FairBaseDTO
from backend.models.fairModel import FairDTO
from backend.models.locationModel import LocationDTO, Location
from backend.services.attractionService import get_attraction_by_id
from backend.services.locationService import get_location_by_id, save_location, validate_location

tinydb = TinyDB("fair_db.json")
db = tinydb.table("fair")
FairQuery = Query()

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

def _create_id():
    return str(ObjectId())


def _date_to_timestamp(date: datetime.date) -> float:
    datetime_obj = datetime.datetime.combine(date, datetime.datetime.min.time())
    timestamp = datetime_obj.timestamp()
    return timestamp


def _timestamp_to_date(timestamp: float) -> datetime.date:
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    date_object = dt_object.date()
    return date_object


def fair_base_to_dto(fair: FairBase) -> FairBaseDTO:
    locationdto: LocationDTO = get_location_by_id(fair.location_id)
    start_date=_timestamp_to_date(fair.start_date)
    end_date=_timestamp_to_date(fair.end_date)

    fair_dict: dict = fair.model_dump(mode="json")

    return FairBaseDTO(
        id=fair_dict['id'],
        name=fair_dict['name'],
        location=locationdto,
        start_date=start_date,
        end_date=end_date,
        attractions=list(),
        fair_done=fair.fair_done,
        fair_incoming=fair.fair_incoming,
        fair_available_today=fair.fair_available_today,
        fair_status=fair.fair_status,
        days_before_start_date=fair.days_before_start_date,
        days_before_end_date=fair.days_before_end_date
    )


def fair_to_dto(fair: Fair) -> FairDTO:
    locationdto: LocationDTO = get_location_by_id(fair.location_id)
    start_date=_timestamp_to_date(fair.start_date)
    end_date=_timestamp_to_date(fair.end_date)

    fair_dict: dict = fair.model_dump(mode="json")

    return FairDTO(
        id=fair_dict['id'],
        name=fair_dict['name'],
        location=locationdto,
        start_date=start_date,
        end_date=end_date,
        sources=fair_dict['sources'],
        attractions=list(),
        fair_done=fair.fair_done,
        fair_incoming=fair.fair_incoming,
        fair_available_today=fair.fair_available_today,
        fair_status=fair.fair_status,
        facebook_event_page=fair_dict['facebook_event_page'],
        official_ad_page=fair_dict['official_ad_page'],
        city_event_page=fair_dict['city_event_page'],
        walk_tour_video=fair_dict['walk_tour_video'],
        days_before_start_date=fair.days_before_start_date,
        days_before_end_date=fair.days_before_end_date
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
            'attractions': fair_dict['attractions'],
            'official_ad_page': fair_dict['official_ad_page'] or None,
            'city_event_page': fair_dict['city_event_page'] or None,
            'facebook_event_page': fair_dict['facebook_event_page'] or None,
            'walk_tour_video': fair_dict['walk_tour_video'] or None
        }
    )
   
    
def validate_fair_base(fair_dict: dict) -> FairBase:
    return FairBase.model_validate(
        {
            'id': _create_id(),
            'name': fair_dict['name'],
            'location_id': fair_dict['location_id'],
            'start_date': _date_to_timestamp(fair_dict['start_date']),
            'end_date': _date_to_timestamp(fair_dict['end_date']),
            'attractions': fair_dict['attractions'],
        }
    )


def create_hidden_fair(fair_dict: dict) -> FairBaseDTO:
    location: Location = validate_location(fair_dict['location'])
    fair_dict['location_id'] = location.id
    fair: Fair = validate_fair_base(fair_dict)
    save_location(location)
    save_hidden_fair(fair)
    return fair_base_to_dto(fair)


def create_fair(fair_dict: dict) -> FairDTO:
    if fair_dict['location_id'] is None and fair_dict['location']:
        location: Location = validate_location(fair_dict['location'])
        save_location(location)
        fair_dict['location_id'] = location.id
    else:
        fair_dict['location_id'] = fair_dict['location_id']
    
    fair: Fair = validate_fair(fair_dict)
    save_fair(fair)
    return fair_to_dto(fair)


def update_fair(updated_fair_dict: dict, id: str) -> FairDTO:
    fair: FairDTO = get_fair(id)
    location: LocationDTO = get_location_by_id(fair.location.id)

    fair_dict: dict = asdict(fair)
    location_dict: dict = asdict(location)
    
    fair_dict.update(updated_fair_dict)
    fair_dict['location_id'] = location.id
    location_dict.update(updated_fair_dict['location'])
    location_dict['id'] = location.id
    
    updated_location: Location = validate_location(location_dict)
    updated_fair: Fair = validate_fair(fair_dict)
    
    updated_fair.location_id = fair.location.id
    updated_location.id = fair.location.id

    save_location(updated_location, update_id=fair.location.id)
    save_fair(updated_fair, update_id=fair.id)

    return fair_to_dto(updated_fair)


def save_fair(fair: Fair, update_id: str=None) -> bool:
    if update_id:
        q = Query()
        fair.id = update_id
        success = db.update(fair.model_dump(mode="json"), q.id == update_id)
    else:
        success = db.insert(fair.model_dump(mode="json"))
    return bool(success)


def save_hidden_fair(fair: FairBase, update_id: str=None) -> bool:
    if update_id:
        q = Query()
        fair.id = update_id
        success = tinydb.table("hidden_fair").update(fair.model_dump(mode="json"), q.id == update_id)
    else:
        success = tinydb.table("hidden_fair").insert(fair.model_dump(mode="json"))
    return bool(success)


def list_fairs(name: Optional[str] = None, location: Optional[str] = None) -> List[FairDTO]:
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


def delete_fair(id: str):
    db.remove(FairQuery.id == id)
    return f"Fair '{id}' has been deleted."


def list_fairs_containing_ride_id(ride_id: str) -> List[FairDTO]:
    fairs: List[FairDTO] = [fair_to_dto(Fair(**fair)) for fair in db.search(FairQuery.attractions.any(ride_id))]
    hidden_fairs: List[FairBaseDTO] = [fair_base_to_dto(FairBase(**fair)) for fair in tinydb.table("hidden_fair").search(FairQuery.attractions.any(ride_id))]
    ## fairs.extend(hidden_fairs)
    fairs.sort(key=lambda fair: fair.start_date, reverse=True)
    return fairs
