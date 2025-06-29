

from bson import ObjectId
from tinydb import Query, TinyDB

from backend.dto.attraction_dto import AttractionDTO, AttractionImageDTO
from backend.models.attractionModel import Attraction, AttractionType
from backend.models.manufacturerModel import Manufacturer
from backend.services.manufacturerService import (
    exists_manufacturer_by_name,
    get_manufacturer,
)

tinydb = TinyDB("fair_db.json")
db = tinydb.table("attraction")
AttractionQuery = Query()


def _create_id() -> str:
    return str(ObjectId())

def list_attraction_images_to_dto(attraction_id: str) -> list[AttractionImageDTO]:
    ride = db.get(AttractionQuery.id == attraction_id)
    if ride and ride.get("images_url", False):
        return [AttractionImageDTO(id=f"{attraction_id}-{i}", path=url) for i, url in enumerate(ride["images_url"])]

    idb = tinydb.table("attraction_image")
    results = idb.search(AttractionQuery.attraction_id == attraction_id)
    return [AttractionImageDTO(id=result["id"], path=result["path"]) for result in results]


def attraction_to_dto(attraction: Attraction) -> AttractionDTO:
    manufacturer: Manufacturer = get_manufacturer(attraction.manufacturer_id)
    images: list[AttractionImageDTO] = list_attraction_images_to_dto(attraction.id)

    attraction_dict: dict = attraction.model_dump(mode="json")

    return AttractionDTO(
        id=attraction_dict["id"],
        name=attraction_dict["name"],
        description=attraction_dict["description"],
        ticket_price=attraction_dict["ticket_price"],
        manufacturer=manufacturer.name if manufacturer else None,
        technical_name=attraction_dict["technical_name"],
        attraction_type=attraction_dict["attraction_type"],
        images=images,
        videos_url=attraction_dict["videos_url"],
        images_url=attraction_dict["images_url"],
        owner=attraction_dict["owner"],
        manufacturer_page_url=attraction_dict["manufacturer_page_url"],
        news_page_url=attraction_dict["news_page_url"],
    )


def create_attraction(attraction_dict: dict[str, str | dict[str, str]]) -> AttractionDTO:
    """Create an attraction."""
    manufacturer_name: str = attraction_dict.get("manufacturer")
    manufacturer: Manufacturer | None = exists_manufacturer_by_name(manufacturer_name)

    if not manufacturer:
        msg = f"No manufacturer found with name '{manufacturer_name}'"
        raise KeyError(msg)

    attraction_payload: dict = {
        "id": _create_id(),
        "name": attraction_dict["name"],
        "description": attraction_dict["description"],
        "ticket_price": attraction_dict["ticket_price"],
        "manufacturer_id": manufacturer.id,
        "technical_name": attraction_dict["technical_name"],
        "attraction_type": AttractionType.from_value(attraction_dict["attraction_type"]),
        "manufacturer_page_url": attraction_dict.get("manufacturer_page_url"),
        "owner": attraction_dict["owner"],
        "news_page_url": attraction_dict.get("news_page_url"),
        "videos_url": attraction_dict.get("videos_url"),
        "images_url": attraction_dict.get("images_url"),
    }

    validated_attraction = Attraction.model_validate(attraction_payload)
    if db.insert(validated_attraction.model_dump(mode="json")):
        return attraction_to_dto(validated_attraction)
    msg = "Failed to save new attraction"
    raise KeyError(msg)


def update_attraction(id: str, attraction_dict: dict) -> AttractionDTO:
    """
    Update a ride from its id.

    Args:
        id (str): id of the ride to update
        attraction_dict (dict): new datas

    Raises:
        KeyError: something goes wrong

    Returns:
        AttractionDTO: the result

    """
    result = db.search(AttractionQuery.id == id)
    if not result:
        msg = "Attraction not found"
        raise KeyError(msg)

    manufacturer_name: str = attraction_dict.get("manufacturer")
    manufacturer: Manufacturer | None = exists_manufacturer_by_name(manufacturer_name)

    if not manufacturer:
        msg = f"No manufacturer found with name '{manufacturer_name}'"
        raise KeyError(msg)

    attraction_payload = {
        "id": _create_id(),
        "name": attraction_dict["name"],
        "description": attraction_dict["description"],
        "ticket_price": attraction_dict["ticket_price"],
        "manufacturer_id": manufacturer.id,
        "technical_name": attraction_dict["technical_name"],
        "attraction_type": AttractionType.from_value(attraction_dict["attraction_type"]),
        "manufacturer_page_url": attraction_dict.get("manufacturer_page_url"),
        "owner": attraction_dict["owner"],
        "news_page_url": attraction_dict.get("news_page_url"),
        "videos_url": attraction_dict.get("videos_url"),
        "images_url": attraction_dict.get("images_url"),
    }

    validated_attraction = Attraction.model_validate(attraction_payload)

    q = Query()
    success = db.update(validated_attraction.model_dump(mode="json"), q.id == id)
    if success:
        return attraction_to_dto(validated_attraction)
    msg = "Failed to update new attraction"
    raise KeyError(msg)


def list_attractions_names_and_id() -> list[dict[str, str]]:
    result: list = list()
    for row in db.all():
        manufacturer = get_manufacturer(row["manufacturer_id"])
        result.append({"key": row["id"], "value": f"{row['name']} ({manufacturer.name})"})
    return result


def list_attractions_names() -> list[str]:
    return [result["name"] for result in db.all()]


def list_attractions(search_ride_query: dict=None) -> list[AttractionDTO]:

    attraction_type = search_ride_query.attraction_type[:]
    manufacturers = [m.id for m in search_ride_query.manufacturers]

    def search_ride_query_funct(record):
        if attraction_type and record["attraction_type"] not in attraction_type:
            return False
        if manufacturers and record["manufacturer_id"] not in manufacturers:
            return False
        return True

    return [attraction_to_dto(Attraction(**ride)) for ride in db.all() if search_ride_query_funct(ride)]


def get_attraction_by_id(attraction_id: str) -> AttractionDTO:
    result = db.search(AttractionQuery.id == attraction_id)
    if result:
        fair: Attraction = Attraction(**result[0])
        return attraction_to_dto(fair)
    raise KeyError("Attraction with id does not exists")


def delete_attraction(id: str):
    if db.remove(AttractionQuery.id == id):
        return f"Attraction '{id}' has been deleted."
    raise KeyError("Attraction with id does not exists")
