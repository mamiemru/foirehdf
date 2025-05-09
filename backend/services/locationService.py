

from dataclasses import asdict
from typing import Dict, List
from bson import ObjectId
from tinydb import TinyDB, Query

from backend.models.locationModel import LocationDTO, Location

tinydb = TinyDB("fair_db.json")
db = tinydb.table("locations")
FairQuery = Query()

def _create_id():
    return str(ObjectId())


def location_to_dto(location: Location) -> LocationDTO:
    return LocationDTO(
        id=location.id,
        street=location.street,
        area=location.area,
        city=location.city,
        postal_code=location.postal_code,
        state=location.state,
        country=location.country,
        lat=location.lat,
        lng=location.lng
    )

def validate_location(location_dict: Dict):
    return Location.model_validate(
        {
            'id': _create_id(),
            'street': location_dict['street'], 'area': location_dict['area'],
            'city': location_dict['city'], 'postal_code': location_dict['postal_code'],
            'state': location_dict['state'], 'country': location_dict['country'],
            'lat': location_dict['lat'] or None,
            'lng': location_dict['lng'] or None
        }
    )

def save_location(location: Location, update_id: str=None) -> bool:
    if update_id:
        q = Query()
        location.id = update_id
        success = db.update(location.model_dump(mode="json"), q.id == update_id)
    else:
        success = db.insert(location.model_dump(mode="json"))
    return bool(success)

def get_location_by_id(location_id: str) -> LocationDTO:
    result = db.get(Query().id == location_id)
    if result:
        return location_to_dto(Location(**result))
    return None

def create_location(location_dict: Dict) -> LocationDTO:
    location: Location = validate_location(location_dict=location_dict)
    if save_location(location=location):
        return location_to_dto(Location(**location))
    return None

def update_location(location_id: str, updated_location_dict: Dict) -> LocationDTO:
    location: LocationDTO = get_location_by_id(location_id=location.id)
    location_dict: dict = asdict(location)
    location_dict.update(updated_location_dict)
    location_dict['id'] = location.id
    location: Location = validate_location(location_dict=location_dict)
    if save_location(location=location ,update_id=location_id):
        return location_to_dto(Location(**location))
    return None

def list_locations() -> List[LocationDTO]:
    return [location_to_dto(Location(**location)) for location in db.all()]

def list_locations_cities() -> List[Dict[str, str]]:
    return [{'key': location['id'], 'value': location['city']} for location in db.all()]
