
from nicegui import app, ui

from backend.models.ride_model import RideOrderBy, SearchRideQuery, SortDirection
from backend.services.manufacturer_service import list_manufacturers
from backend.services.ride_service import list_ride_types, list_rides
from frontend.const import _, field_value
from frontend.ride_box import display_ride_as_item_in_list


def view_ride(fair_id: int) -> None:
    """Simulate navigation to fair details page."""
    ui.navigate.to(f"/fair-view/{fair_id}")

@ui.refreshable
def display_rides() -> None:
    """Display filtered rides, need decorators to be dynamic."""
    with ui.row().classes("w-full flex-wrap justify-center"):
        for ride in list_rides(search_ride_query=app.storage.client["search_ride_query"]):
            with ui.column().classes("w-full sm:w-1/2 md:w-1/3 lg:w-1/4 p-2"):
                display_ride_as_item_in_list(_, ride)

def refresh_rides_list(search_ride_query: SearchRideQuery) -> None:
    """Refresh the page in one function call."""
    app.storage.client["search_ride_query"] = search_ride_query
    display_rides.refresh()

def reset_rides_list(search_ride_query: SearchRideQuery) -> None:
    """Reset filter and refresh the page in one function call."""
    search_ride_query.reset()
    app.storage.client["search_ride_query"] = search_ride_query
    display_rides.refresh()

def ride_list(search_ride_query: SearchRideQuery) -> None:
    """List and display selected rides."""
    app.storage.client["search_ride_query"] = search_ride_query
    manufacturer_names: list[str] = [m.name for m in list_manufacturers()]

    with ui.row().classes("w-full justify-between"):
        ui.label(field_value("RIDES_LIST")).style("color: #6E93D6; font-size: 200%; font-weight: 300")
        ui.space()
        ui.button("Add ride", icon="add", on_click=lambda: ui.navigate.to("/ride_create"))

    with ui.expansion(field_value("RIDES_SEARCH_TITLE"), icon="search").classes("w-full justify-center"):
        with ui.row().classes("w-full justify-center space-between"):

            with ui.column().classes("w-6/12"):
                ui.select(list_ride_types(), with_input=True, multiple=True, label=field_value("RIDES_SEARCH_BY_ATTRACTION_TYPE")).classes("w-full").props("use-chips").bind_value(search_ride_query, "ride_type")
                ui.select(manufacturer_names, with_input=True, multiple=True, label=field_value("RIDES_SEARCH_BY_MANUFACTURER")).classes("w-full").props("use-chips").bind_value(search_ride_query, "manufacturers")

            with ui.column().classes("w-5/12"):
                ui.select({r:field_value(r) for r in list(RideOrderBy)}, with_input=True, label=field_value("RIDES_SEARCH_ORDER_BY")).classes("w-full").bind_value(search_ride_query, "order_by")
                ui.select({s:field_value(s) for s in list(SortDirection)}, with_input=True, label=field_value("RIDES_SEARCH_SORT")).classes("w-full").bind_value(search_ride_query, "sort")

        with ui.row().classes("w-full"):
            ui.button(field_value("FAIR_SEARCH_BUTTON"), icon="search",on_click=lambda: refresh_rides_list(search_ride_query))
            ui.button(field_value("FAIR_SEARCH_BUTTON_RESET"), icon="close", on_click=lambda: reset_rides_list(search_ride_query))


    refresh_rides_list(search_ride_query=search_ride_query)
    display_rides()
