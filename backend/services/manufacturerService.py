from typing import List
from tinydb import TinyDB, Query
from bson import ObjectId
from backend.dto.manufacturer_dto import ManufacturerDto
from backend.models.manufacturerModel import Manufacturer

tinydb = TinyDB("fair_db.json")
db = tinydb.table("manufacturer")
query = Query()

def _create_id():
    return str(ObjectId())

def manufacturer_to_dto(manufacturer: Manufacturer) -> ManufacturerDto:
    return ManufacturerDto(
        id=manufacturer.id,
        name=manufacturer.name,
        website_url=manufacturer.website_url
    )

def validate_manufacturer(manufacturer_dict: dict) -> Manufacturer:
    validation_manufacturer: Manufacturer = Manufacturer(
        id=_create_id(),
        name=manufacturer_dict['name'],
        website_url=manufacturer_dict['website_url']
    )

    if validation_manufacturer.name not in list_manufacturers_names():
        return validation_manufacturer
    return None

def create_manufacturer(manufacturer: Manufacturer) -> ManufacturerDto:
    success = db.insert(manufacturer.model_dump(mode="json"))
    return manufacturer_to_dto(manufacturer) if success else None

def list_manufacturers_names() -> List[str]:
    return [manufacturer['name'] for manufacturer in db.all()]

def list_manufacturers() -> List[ManufacturerDto]:
    return [manufacturer_to_dto(Manufacturer(**manufacturer)) for manufacturer in db.all()]

def exists_manufacturer_by_name(manufacturer_name: str) -> Manufacturer:
    result = db.search(query.name == manufacturer_name)
    if result:
        manufacturer: Manufacturer = Manufacturer(**result[0])
        return manufacturer
    return None

def get_manufacturer(id: str) -> Manufacturer:
    result = db.search(query.id == id)
    if result:
        manufacturer: Manufacturer = Manufacturer(**result[0])
        return manufacturer
    return None

def update_manufacturer(id: str, updated_manufacturer: Manufacturer) -> Manufacturer:
    db.update(updated_manufacturer.model_dump(mode="json"), query.id == id)
    return get_manufacturer(id)

def delete_manufacturer(id: str) -> bool:
    db.remove(query.id == id)
    return True
