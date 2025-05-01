
import uuid
from typing import Dict

from tinydb import TinyDB, Query

from backend.models.locationModel import LocationDTO, Location

tinydb = TinyDB("fair_db.json")
db = tinydb.table("locations")
FairQuery = Query()

def _create_id():
    return str(uuid.uuid4())


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

def get_location_by_id(location_id: str) -> Location:
    result = db.get(Query().id == location_id)
    if result:
        return location_to_dto(Location(**result))
    return None
