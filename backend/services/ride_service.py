

from typing import Any

from bson import ObjectId
from tinydb import Query, TinyDB

from backend.models.ride_model import Ride, RideType

tinydb = TinyDB("fair_db.json")
db = tinydb.table("ride")
RideQuery = Query()


def _create_id() -> str:
    return str(ObjectId())


def create_ride(ride_dict: dict[str, str | dict[str, str]]) -> Ride:
    """Create an ride."""
    ride_payload: dict = {
        "id": _create_id(),
        "name": ride_dict["name"],
        "description": ride_dict["description"],
        "ticket_price": ride_dict["ticket_price"],
        "manufacturer": ride_dict["manufacturer"],
        "technical_name": ride_dict["technical_name"],
        "ride_type": RideType.from_value(ride_dict["ride_type"]),
        "manufacturer_page_url": ride_dict.get("manufacturer_page_url"),
        "owner": ride_dict["owner"],
        "news_page_url": ride_dict.get("news_page_url"),
        "videos_url": ride_dict.get("videos_url"),
        "images_url": ride_dict.get("images_url"),
    }

    validated_ride = Ride.model_validate(ride_payload)
    if db.insert(validated_ride.model_dump(mode="json")):
        return validated_ride
    msg = "Failed to save new ride"
    raise KeyError(msg)


def update_ride(id: str, ride_dict: dict[str, Any]) -> Ride:
    """
    Update a ride from its id.

    Args:
        id (str): id of the ride to update
        ride_dict (dict): new datas

    Raises:
        KeyError: something goes wrong

    Returns:
        Ride: the result

    """
    result = db.search(RideQuery.id == id)
    if not result:
        msg = "Ride not found"
        raise KeyError(msg)

    ride_payload = {
        "id": _create_id(),
        "name": ride_dict["name"],
        "description": ride_dict["description"],
        "ticket_price": ride_dict["ticket_price"],
        "manufacturer": ride_dict.get("manufacturer"),
        "technical_name": ride_dict["technical_name"],
        "ride_type": RideType.from_value(ride_dict["ride_type"]),
        "manufacturer_page_url": ride_dict.get("manufacturer_page_url"),
        "owner": ride_dict["owner"],
        "news_page_url": ride_dict.get("news_page_url"),
        "videos_url": ride_dict.get("videos_url"),
        "images_url": ride_dict.get("images_url"),
    }

    validated_ride = Ride.model_validate(ride_payload)

    q = Query()
    success = db.update(validated_ride.model_dump(mode="json"), q.id == id)
    if success:
        return validated_ride
    msg = "Failed to update new ride"
    raise KeyError(msg)


def list_rides_names_and_id() -> list[dict[str, str]]:
    result: list = list()
    for row in db.all():
        manufacturer = row["manufacturer"]
        result.append({"key": row["id"], "value": f"{row['name']} ({manufacturer})"})
    return result


def list_rides_names() -> list[str]:
    return [result["name"] for result in db.all()]


def list_rides(search_ride_query: dict | None = None) -> list[Ride]:
    """List rides according the search_query."""
    if not search_ride_query:
        return [Ride(**ride) for ride in db.all()]

    ride_type = search_ride_query.ride_type[:]
    manufacturers = [m.name for m in search_ride_query.manufacturers]

    def search_ride_query_funct(record) -> bool:
        if ride_type and record["ride_type"] not in ride_type:
            return False
        return not (manufacturers and record["manufacturer"] not in manufacturers)

    return [Ride(**ride) for ride in db.all() if search_ride_query_funct(ride)]


def get_ride_by_id(ride_id: str) -> Ride:
    """Get a ride by its id."""
    result = db.get(RideQuery.id == ride_id)
    if result:
        fair: Ride = Ride(**result)
        return fair
    msg = "Ride with id does not exists"
    raise KeyError(msg)


def delete_ride(ride_id: str) -> str:
    """
    Delete a ride from the db.

    Args:
        ride_id (str): id of the ride to delete

    Raises:
        KeyError: the ride does not exists

    Returns:
        str: success message

    """
    if db.remove(RideQuery.id == ride_id):
        return f"Ride '{ride_id}' has been deleted."
    msg = "Ride with id does not exists"
    raise KeyError(msg)
