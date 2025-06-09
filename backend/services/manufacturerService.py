from typing import List
from tinydb import TinyDB, Query
from backend.dto.manufacturer_dto import ManufacturerDto
from backend.models.manufacturerModel import Manufacturer

tinydb = TinyDB("fair_db.json")
db = tinydb.table("manufacturer")
query = Query()


def manufacturer_to_dto(manufacturer: Manufacturer) -> ManufacturerDto:
    return ManufacturerDto(
        id=manufacturer.id,
        name=manufacturer.name,
        website_url=manufacturer.website_url
    )

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
    raise KeyError("Manufacturer with id does not exists")


def get_manufacturer(id: str) -> Manufacturer:
    result = db.search(query.id == id)
    if result:
        manufacturer: Manufacturer = Manufacturer(**result[0])
        return manufacturer
    raise KeyError("Manufacturer with id does not exists")


def delete_manufacturer(id: str) -> bool:
    if db.remove(query.id == id):
        return "manufacturer has been deleted"
    raise KeyError("Manufacturer with id does not exists")
