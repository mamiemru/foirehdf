

from typing import Any

from tinydb import Query, TinyDB

from backend.models.ride_model import Ride, SearchRideQuery

tinydb = TinyDB("fair_db.json")
db = tinydb.table("ride")
RideQuery = Query()

def create_ride(ride_dict: dict[str, Any]) -> Ride:
    """Create an ride."""
    validated_ride = Ride.model_validate(ride_dict)
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

    validated_ride = Ride.model_validate(ride_dict)

    q = Query()
    success = db.update(validated_ride.model_dump(mode="json"), q.id == id)
    if success:
        return validated_ride
    msg = "Failed to update new ride"
    raise KeyError(msg)


def list_rides_names_and_id() -> dict[str, str]:
    """Return a dict of ride ids and explicite name."""
    return {row["id"]: f"""{row['name']} ({row["manufacturer"]})""" for row in db.all()}


def list_rides_names() -> list[str]:
    return [result["name"] for result in db.all()]


def list_rides(search_ride_query: SearchRideQuery) -> list[Ride]:
    """List rides according the search_query."""
    if not search_ride_query:
        return [Ride(**ride) for ride in db.all()]

    def search_ride_query_funct(record: dict[str, str]) -> bool:
        if search_ride_query.ride_type and record["ride_type"] not in search_ride_query.ride_type:
            return False
        return not (search_ride_query.manufacturers and record["manufacturer"] not in search_ride_query.manufacturers)

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
