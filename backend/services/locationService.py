


from typing import TYPE_CHECKING, Any

from bson import ObjectId
from tinydb import Query, TinyDB

from backend.models.location_model import Location

if TYPE_CHECKING:
    from tinydb.table import Document

db_instance  = TinyDB("fair_db.json")
db = db_instance.table("locations")
FairQuery = Query()


def create_location(location_dict: dict[str, Any]) -> Location:
    """
    Create a new location after validating its data.

    Args:
        location_dict (Dict[str, Any]): The raw location data to validate and save.

    Returns:
        bool: True if the location was successfully saved.

    """
    validated_location = validate_location(location_dict)
    return save_location(validated_location)


def validate_location(location_dict: dict[str, str | None]) -> Location:
    """
    Parse a location dict into a location object.

    Args:
        location_dict (dict[str, str  |  None]): location data

    Returns:
        Location: parsed Location

    """
    return Location.model_validate(
        {
            "id": str(ObjectId()),
            "street": location_dict["street"], "area": location_dict["area"],
            "city": location_dict["city"], "postal_code": location_dict["postal_code"],
            "state": location_dict["state"], "country": location_dict["country"],
            "lat": location_dict["lat"] or None,
            "lng": location_dict["lng"] or None,
        },
    )


def save_location(location: Location, update_id: str | None = None) -> Location:
    """
    Save a location, may be an update if the update_id is provided.

    Args:
        location (Location): location
        update_id (str | None, optional): id if update. Defaults to None.

    Raises:
        ValueError: issues when saving

    Returns:
        Location: when succed

    """
    if update_id:
        q = Query()
        location.id = update_id
        if db.update(location.model_dump(mode="json"), q.id == update_id):
            return location
    elif db.insert(location.model_dump(mode="json")):
        return location

    msg = "Cannot save location"
    raise ValueError(msg)


def get_location_by_id(location_id: str) -> Location:
    """
    Get a location by its id.

    Args:
        location_id (str): location id

    Raises:
        KeyError: when the location does not exists

    Returns:
        Location: case of success

    """
    query = Query()
    result: Document | None = db.get(query.id == location_id)

    if result is not None:
        data: dict[str, Any] = dict(result)
        return Location(**data)

    msg: str = "Location with id does not exist"
    raise KeyError(msg)


def delete_location(location_id: str) -> bool:
    """
    Delete a location by its location_id.

    Args:
        location_id (str): The unique identifier of the location to delete.

    Returns:
        bool: True if the location was successfully deleted.

    Raises:
        KeyError: If the location with the given ID does not exist.

    """
    if db.remove(Query().id == location_id):
        return True
    msg = "Location with id does not exist"
    raise KeyError(msg)


def list_locations() -> list[Location]:
    """
    Return a list of all locations in the database.

    Returns:
        List[Location]: A list of Location objects.

    """
    documents: list[Document] = db.all()
    return [Location(**dict(doc)) for doc in documents]


def list_locations_cities() -> list[dict[str, str]]:
    return [{"key": location["id"], "value": location["city"]} for location in db.all()]
