
from tinydb import Query, TinyDB

from backend.models.manufacturer_model import Manufacturer

tinydb = TinyDB("fair_db.json")
db = tinydb.table("manufacturer")
query = Query()


def create_manufacturer(manufacturer: Manufacturer) -> Manufacturer:
    """
    Insert a new manufacturer into the database.

    Args:
        manufacturer (Manufacturer): The Manufacturer instance to insert.

    Returns:
        Optional[Manufacturer]: the created manufacturer if successful, else None.

    """
    if db.insert(manufacturer.model_dump(mode="json")):
        return manufacturer
    msg = "Manufacturer cannot be created"
    raise ValueError(msg)


def list_manufacturers_names() -> list[str]:
    """
    Return a list of all manufacturer names in the database.

    Returns:
        List[str]: A list of manufacturer names.

    """
    return [doc["name"] for doc in db.all() if "name" in doc]


def list_manufacturers() -> list[Manufacturer]:
    """
    Return a list of all manufacturers as DTOs.

    Returns:
        List[Manufacturer]: A list of manufacturers.

    """
    return [
        Manufacturer.model_validate(manufacturer)
        for manufacturer in db.all()
    ]


def exists_manufacturer_by_name(manufacturer_name: str) -> Manufacturer:
    """
    Check if a manufacturer with the given name exists.

    Args:
        manufacturer_name (str): The manufacturer's name.

    Returns:
        Manufacturer: The matching manufacturer instance.

    Raises:
        KeyError: If no manufacturer with the given name exists.

    """
    manufacturer_dict = db.get(query.name == manufacturer_name)
    if manufacturer_dict:
        return Manufacturer.model_validate(manufacturer_dict)
    msg = "Manufacturer with name does not exist"
    raise KeyError(msg)


def get_manufacturer(manufacturer_id: str) -> Manufacturer:
    """
    Retrieve a manufacturer by its ID.

    Args:
        manufacturer_id (str): The manufacturer's unique ID.

    Returns:
        Manufacturer: The corresponding manufacturer instance.

    Raises:
        KeyError: If no manufacturer with the given ID exists.

    """
    manufacturer_dict = db.get(query.id == manufacturer_id)
    if manufacturer_dict:
        return Manufacturer.model_validate(manufacturer_dict)
    msg = "Manufacturer with id does not exist"
    raise KeyError(msg)


def delete_manufacturer(manufacturer_id: str) -> bool:
    """
    Delete a manufacturer by its ID.

    Args:
        manufacturer_id (str): The manufacturer's unique ID.

    Returns:
        bool: True if the deletion was successful.

    Raises:
        KeyError: If no manufacturer with the given ID exists.

    """
    manufacturer_to_delete = db.get(query.id == manufacturer_id)
    if not manufacturer_to_delete:
        msg = "Manufacturer with id does not exist"
        raise KeyError(msg)

    return bool(db.remove(query.id == manufacturer_id))

