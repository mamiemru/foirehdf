"""A serviec for Fair."""

import locale
from datetime import datetime
from typing import Any

import pandas as pd
from tinydb import Query, TinyDB

from backend.models.fair_model import Fair, FairBase, FairCreateInput, FairStatus, FairUpdateInput, SearchFairMap, SearchFairQuery, SearchFairResult
from backend.models.location_model import LocationBase
from backend.models.ride_model import Ride
from backend.models.timeline_model import Timeline, TimelineItem, TimelineItemType
from backend.services.location_service import get_location_by_id
from backend.services.ride_service import get_ride_by_id

tinydb: TinyDB = TinyDB("fair_db.json")
db = tinydb.table("fair")
FairQuery: Query = Query()

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")



def create_hidden_fair(fair_dict: dict[str, Any]) -> FairBase:
    fair: FairBase = FairBase.model_validate(fair_dict)
    save_hidden_fair(fair)
    return fair


def create_fair(fair_create_input: FairCreateInput) -> Fair:
    """
    Create a fair.

    Args:
        fair_create_input (FairCreateInput): fair datas

    Returns:
        Fair: created fair

    """
    rides: dict[str, Ride] = {ride_id: get_ride_by_id(ride_id) for ride_id in fair_create_input.rides}
    locations: list[LocationBase] = [get_location_by_id(loc) for loc in fair_create_input.locations]

    fair_dict: dict[str, Any] = fair_create_input.model_dump()
    fair_dict["locations"] = locations
    fair: Fair = Fair.model_validate(fair_dict)
    fair.timeline = Timeline(
        line=[
            TimelineItem(type=TimelineItemType.RIDE_AVAILABLE, ride=ride.id, date=fair.start_date, title=ride.name) for ride in rides if ride
        ],
    )
    save_fair(fair)
    return fair


def update_fair(fair_id: str, fair_update_input: FairUpdateInput) -> Fair:
    fair: Fair = get_fair(fair_id=fair_id)
    fair_dict: dict[str, Any] = fair_update_input.model_dump()
    fair_dict["locations"] = [get_location_by_id(loc) for loc in fair_dict["locations"]]
    updated_fair: Fair = Fair.model_validate(fair_dict)
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


def list_fairs(search_fair_query: SearchFairQuery) -> list[Fair]:
    """
    List fairs, using search_query.

    Args:
        search_fair_query (SearchFairQuery): filter search. Defaults to None.

    Returns:
        list[Fair]: list of filtered fairs

    """

    def search_query_func(record: dict[str, Any]) -> bool:
        date = datetime.fromtimestamp(record["start_date"], tz=None).date()
        city = record["locations"][0]["city"]
        if search_fair_query.cities and city not in search_fair_query.cities:
            return False
        if search_fair_query.date_min and date < search_fair_query.date_min:
            return False
        return not (search_fair_query.date_max and date > search_fair_query.date_max)

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
    """
    List all fairs that contrains the ride.

    Args:
        ride_id (str): the ride we are looking for

    Returns:
        list[Fair]: a list of fairs with the ride in it

    """
    fairs: list[Fair] = [Fair(**fair) for fair in db.search(FairQuery.rides.any(ride_id))]
    # hidden fairs aren't Fair objects — but type declared says return Fair
    # you could optionally change return type to list[Union[Fair, FairBase]]
    fairs.sort(key=lambda fair: fair.start_date, reverse=True)
    return fairs



def list_fair_sort_by_status(search_fair_query: SearchFairQuery) -> SearchFairResult:
    """
    List all fairs that match with search_fair_query. it also returns map and gentt informations about the selected list of fairs.

    Args:
        search_fair_query (SearchFairQuery): Some filters to filter out fairs

    Returns:
        SearchFairResult: search result

    """
    fairs: list[Fair] = list_fairs(search_fair_query=search_fair_query)
    fairs.sort(key=lambda f: f.start_date)

    pd_dict: list[dict[str, Any]] = []
    fairs_map: list[SearchFairMap] = []
    fairs_sorted: dict[str, list[Fair]] = {f.value: [] for f in FairStatus}

    def fair_color(fair: Fair) -> str:
        """Return the best color from a fair state."""
        return "#33cc33" if fair.fair_available_today else "#ff9900" if fair.fair_incoming else "#0066cc"

    def fair_date_info(fair: Fair) -> int | None:
        """Return piece of information about the date."""
        return fair.days_before_start_date if fair.fair_incoming  else fair.days_before_end_date  if fair.fair_available_today else None

    for fair in fairs:
        fairs_sorted[fair.fair_status.value].append(fair)
        location = fair.locations[0]
        if location.lng and location.lat:
            color = fair_color(fair=fair)
            size = 7 if fair.fair_available_today else 5 if fair.fair_incoming else 2
            fairs_map.append(SearchFairMap(color=color, lng=location.lng, lat=location.lat, size=size))

        pd_dict.append(
            {
                "task": location.city,
                "start": fair.start_date,
                "finish": fair.end_date,
                "resource": location.city,
                "status":  fair.fair_status,
                "date": fair_date_info(fair=fair),
                "start_date": fair.start_date.strftime("%d %B %Y"),
                "end_date": fair.end_date.strftime("%d %B %Y"),
                "name": fair.name,
            },
        )

    structured_search_fair_result: SearchFairResult = SearchFairResult(gantt=pd.DataFrame(pd_dict), map=fairs_map, fairs=fairs_sorted)
    return structured_search_fair_result
