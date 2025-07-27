



from tinydb import TinyDB

from backend.models.ride_model import ManufacturerRide

tinydb = TinyDB("fair_db.json")
db = tinydb.table("manufacturer_ride")

def list_manufacturer_rides() -> list[ManufacturerRide]:
    """List all manufactured rides."""
    return [ManufacturerRide(**ride) for ride in db.all()]

