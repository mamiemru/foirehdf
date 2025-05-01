
import hashlib
from typing import List, Dict
from pathlib import Path
from tinydb import TinyDB, Query

from backend.services.manufacturerService import get_manufacturer
from backend.services.manufacturerService import exists_manufacturer_by_name

from backend.models.manufacturerModel import Manufacturer
from backend.models.attractionModel import Attraction, AttractionType

from backend.dto.attraction_dto import AttractionDTO
from backend.dto.attraction_dto import AttractionImageDTO

tinydb = TinyDB("fair_db.json")
db = tinydb.table("attraction")
AttractionQuery = Query()

def _create_id(attraction: dict):
    return f"{hash(attraction['name'])}-{hash(attraction['manufacturer'])}-{hash(attraction['technical_name'])}"

def upload_attraction_image(attraction_image, attraction_id: str) -> str:
    image_dir = Path("images/attractions/rides")
    image_dir.mkdir(parents=True, exist_ok=True)
    image_bytes = attraction_image.read()
    hash_id = hashlib.sha256(image_bytes[:128]).hexdigest()

    image_path = image_dir / f"{hash_id}.jpg"
    with open(image_path, "wb") as f:
        f.write(image_bytes)
    idb = tinydb.table("attraction_image")
    if idb.insert({"id": hash_id, "path": str(image_path), "attraction_id": attraction_id}):
        return hash_id
    return None

def list_attraction_images_to_dto(attraction_id: str) -> List[AttractionImageDTO]:
    ride = db.get(AttractionQuery.id == attraction_id)
    if ride and ride.get('images_url', False):
        return [AttractionImageDTO(id=f"{attraction_id}-{i}", path=url) for i, url in enumerate(ride['images_url'])]

    idb = tinydb.table("attraction_image")
    results = idb.search(AttractionQuery.attraction_id == attraction_id)
    return [AttractionImageDTO(id=result['id'], path=result['path']) for result in results]

def attraction_to_dto(attraction: Attraction) -> AttractionDTO:
    manufacturer: Manufacturer = get_manufacturer(attraction.manufacturer_id)
    images: List[AttractionImageDTO] = list_attraction_images_to_dto(attraction.id)

    attraction_dict: dict = attraction.model_dump(mode="json")

    return AttractionDTO(
        id=attraction_dict['id'],
        name=attraction_dict['name'],
        description=attraction_dict['description'],
        ticket_price=attraction_dict['ticket_price'],
        manufacturer=manufacturer.name if manufacturer else None,
        technical_name=attraction_dict['technical_name'],
        attraction_type=attraction_dict['attraction_type'],
        images=images,
        videos_url=attraction_dict['videos_url'],
        images_url=attraction_dict['images_url'],
        owner=attraction_dict['owner'],
        manufacturer_page_url=attraction_dict['manufacturer_page_url'],
        news_page_url=attraction_dict['news_page_url']
    )

def create_attraction(attraction_dict: dict, attraction_image=None) -> AttractionDTO:
    
    manufacturer: Manufacturer = exists_manufacturer_by_name(attraction_dict['manufacturer'])
    if not manufacturer:
        raise KeyError("no manufacturer found")

    validation_attraction: Attraction = Attraction.model_validate(
        {
            "id": _create_id(attraction_dict), "name": attraction_dict['name'],
            "description": attraction_dict['description'], "ticket_price": attraction_dict['ticket_price'],
            "manufacturer_id": manufacturer.id, "technical_name": attraction_dict['technical_name'],
            "attraction_type": AttractionType.from_value(attraction_dict['attraction_type']),
            'manufacturer_page_url': attraction_dict['manufacturer_page_url'] or None, 'owner': attraction_dict['owner'],
            'news_page_url': attraction_dict['news_page_url'] or None, 'videos_url': attraction_dict['videos_url'],
            'images_url': attraction_dict['images_url']
        }
    )
    
    success = db.insert(validation_attraction.model_dump(mode="json"))
    if success:
        return attraction_to_dto(validation_attraction)
    return None


def update_attraction(id: str, attraction_dict: dict) -> AttractionDTO:
        
    manufacturer: Manufacturer = exists_manufacturer_by_name(attraction_dict['manufacturer'])
    if not manufacturer:
        raise KeyError("no manufacturer found")

    validation_attraction: Attraction = Attraction.model_validate(
        {
            "id": id, "name": attraction_dict['name'],
            "description": attraction_dict['description'], "ticket_price": attraction_dict['ticket_price'],
            "manufacturer_id": manufacturer.id, "technical_name": attraction_dict['technical_name'],
            "attraction_type": AttractionType.from_value(attraction_dict['attraction_type']),
            'manufacturer_page_url': attraction_dict['manufacturer_page_url'], 'owner': attraction_dict['owner'],
            'news_page_url': attraction_dict['news_page_url'], 'videos_url': attraction_dict['videos_url'],
            'images_url': attraction_dict['images_url']
        }
    )
    
    q = Query()
    success = db.update(validation_attraction.model_dump(mode="json"), q.id == id)
    if success:
        return attraction_to_dto(validation_attraction)
    return None

def list_attractions_names_and_id() -> Dict[str, List[str]]:
    result: dict = {"keys": list(), "values": list()}
    for row in db.all():
        manufacturer = get_manufacturer(row['manufacturer_id'])
        result['keys'].append(row['id'])
        result['values'].append(f"{row['name']} ({manufacturer.name})")
    return result

def list_attractions_names() -> List[str]:
    results = db.all()
    return [result['name'] for result in results ]

def list_attractions() -> List[AttractionDTO]:
    rides: List[Attraction] = [Attraction(**result) for result in db.all()]
    return [attraction_to_dto(ride) for ride in rides]

def get_attraction_by_id(attraction_id: str) -> AttractionDTO:
    result = db.search(AttractionQuery.id == attraction_id)
    if result:
        fair: Attraction = Attraction(**result[0])
        return attraction_to_dto(fair)
    return None

def delete_attraction(id: str):
    db.remove(AttractionQuery.id == id)
    return f"Attraction '{id}' has been deleted."
