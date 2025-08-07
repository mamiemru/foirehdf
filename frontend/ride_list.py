
from nicegui import ui

from backend.models.manufacturer_model import Manufacturer
from backend.models.ride_model import RideType
from backend.services.manufacturer_service import list_manufacturers
from backend.services.ride_service import list_rides
from frontend.ride_box import display_ride_as_item_in_list
from pages.const import _
from pages.form_input import DotDict

search_ride_query = DotDict()

def reset_search_ride_query() -> None:
    """Reset search ride query."""
    search_ride_query.ride_type = []
    search_ride_query.manufacturers = []

reset_search_ride_query()


def view_ride(fair_id: int) -> None:
    """Simulate navigation to fair details page."""
    ui.navigate.to(f"/fair_view/{fair_id}")

def ride_list() -> None:
    """List and display selected rides."""
    manufacturer_names: list[Manufacturer] = [str(m) for m in list_manufacturers()]

    with ui.row().classes("w-full justify-between"):
        ui.label(_("RIDES_LIST")).style("color: #6E93D6; font-size: 200%; font-weight: 300")
        ui.space()
        ui.button("Add ride", icon="add", on_click=lambda: ui.notify("You clicked me!"))


    with ui.expansion(_("RIDES_SEARCH_TITLE"), icon="search").classes("w-full justify-center"):
        ui.select([a.value for a in RideType], multiple=True, value=search_ride_query.ride_type, label=_("RIDES_SEARCH_BY_ATTRACTION_TYPE")).classes("w-64").props("use-chips").bind_value(search_ride_query, "ride_type")
        ui.select(manufacturer_names, multiple=True, value=search_ride_query.ride_type, label=_("RIDES_SEARCH_BY_MANUFACTURER")).classes("w-64").props("use-chips").bind_value(search_ride_query, "manufacturers")

        with ui.row().classes("w-full"):
            ui.button(_("FAIR_SEARCH_BUTTON"), icon="search", on_click=lambda: fairs_by_status.update(list_fair_sort_by_status(search_ride_query=search_ride_query)))
            ui.button(_("FAIR_SEARCH_BUTTON_RESET"), icon="close", on_click=reset_search_ride_query)

    ui.label().bind_text_from(search_ride_query)

    rides = list_rides(search_ride_query=search_ride_query)

    with ui.row().classes("w-full flex-wrap justify-center"):
        for ride in rides:
            with ui.column().classes("w-full sm:w-1/2 md:w-1/3 lg:w-1/4 p-2"):
                display_ride_as_item_in_list(_, ride)
