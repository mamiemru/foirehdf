"""A serviec for Fair."""

import locale
from datetime import datetime
from typing import Any

import pandas as pd
from tinydb import Query, TinyDB

from backend.models.fairModel import Fair, FairBase, FairStatus

tinydb: TinyDB = TinyDB("fair_db.json")
db = tinydb.table("fair")
FairQuery: Query = Query()

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")



def create_hidden_fair(fair_dict: dict[str, Any]) -> FairBase:
    fair: FairBase = FairBase.model_validate(fair_dict)
    save_hidden_fair(fair)
    return fair


def create_fair(fair_dict: dict[str, Any]) -> Fair:
    fair: Fair = Fair.model_validate(fair_dict)
    save_fair(fair)
    return fair


def update_fair(updated_fair_dict: dict[str, Any], id: str) -> Fair:
    fair: Fair = get_fair(id)
    updated_fair: Fair = Fair.model_validate(updated_fair_dict)
    save_fair(updated_fair, update_id=fair.id)
    return updated_fair


def save_fair(fair: Fair, update_id: str | None = None) -> bool:
    if update_id:
        q: Query = Query()
        fair.id = update_id
        success = db.update(fair.model_dump(mode="json"), q.id == update_id)
    else:
        success = db.insert(fair.model_dump(mode="json"))
    return bool(success)


def save_hidden_fair(fair: FairBase, update_id: str | None = None) -> bool:
    hidden_db = tinydb.table("hidden_fair")
    if update_id:
        q: Query = Query()
        fair.id = update_id
        success = hidden_db.update(fair.model_dump(mode="json"), q.id == update_id)
    else:
        success = hidden_db.insert(fair.model_dump(mode="json"))
    return bool(success)


def list_fairs(search_fair_query: Any | None = None) -> list[Fair]:
    """
    List fairs, using search_query.

    Args:
        search_fair_query (Any | None, optional): _description_. Defaults to None.

    Returns:
        list[Fair]: list of filtered fairs

    """
    cities: list[str] = [obj["key"] for obj in search_fair_query.cities] if search_fair_query and search_fair_query.cities else []
    date_min: date | None = search_fair_query.date_min if search_fair_query else None
    date_max: date | None = search_fair_query.date_max if search_fair_query else None

    def search_query_func(record: dict[str, Any]) -> bool:
        date = datetime.fromtimestamp(record["start_date"], tz=None).date()
        if cities and record.get("location_id") not in cities:
            return False
        if date_min and date < date_min:
            return False
        return not (date_max and date > date_max)

    return [Fair.model_validate(result) for result in db.all() if search_query_func(result)]


def get_fair(fair_id: str) -> Fair:
    """Get a fair by its id."""
    result = db.get(FairQuery.id == fair_id)
    if result:
        return Fair(**result)
    msg = "Fair with id does not exist"
    raise KeyError(msg)


def delete_fair(id: str) -> str:
    if db.remove(FairQuery.id == id):
        return f"Fair '{id}' has been deleted."
    raise KeyError("Fair with id does not exist")


def list_fairs_containing_ride_id(ride_id: str) -> list[Fair]:
    fairs: list[Fair] = [Fair(**fair) for fair in db.search(FairQuery.rides.any(ride_id))]
    # hidden fairs aren't Fair objects — but type declared says return Fair
    # you could optionally change return type to list[Union[Fair, FairBase]]
    fairs.sort(key=lambda fair: fair.start_date, reverse=True)
    return fairs



def list_fair_sort_by_status(search_fair_query: Any | None = None) -> dict[str, Any]:
    fairs: list[Fair] = list_fairs(search_fair_query=search_fair_query)
    pd_dict: list[dict[str, Any]] = []

    response: dict[str, Any] = {
        "fairs": {
            str(FairStatus.INCOMING.value): [],
            str(FairStatus.DONE.value): [],
            str(FairStatus.CURRENTLY_AVAILABLE.value): [],
        },
        "map": [],
        "gantt": None,
    }

    for fair in fairs:
        response["fairs"][fair.fair_status].append(fair)
        location = fair.locations[0]
        if location.lng and location.lat:
            color = (
                "#33cc33"
                if fair.fair_available_today
                else "#ff9900"
                if fair.fair_incoming
                else "#0066cc"
            )
            size = 7 if fair.fair_available_today else 5 if fair.fair_incoming else 2
            response["map"].append(
                {
                    "color": color,
                    "lng": location.lng,
                    "lat": location.lat,
                    "size": size,
                },
            )

        pd_dict.append(
            {
                "task": location.city,
                "start": fair.start_date,
                "finish": fair.end_date,
                "resource": location.city,
                "color": (
                    "#33cc33"
                    if fair.fair_available_today
                    else "#ff9900"
                    if fair.fair_incoming
                    else "#0066cc"
                ),
                "date": (
                    fair.days_before_start_date
                    if fair.fair_incoming
                    else fair.days_before_end_date
                    if fair.fair_available_today
                    else None
                ),
                "start_date": fair.start_date.strftime("%d %B %Y"),
                "end_date": fair.end_date.strftime("%d %B %Y"),
                "name": fair.name,
            },
        )

    for key, fair_list in response["fairs"].items():
        response["fairs"][key] = sorted(fair_list, key=lambda fair: fair.start_date, reverse=True)

    response["gantt"] = pd.DataFrame(pd_dict)
    return response
