import json

from nicegui import ui

from backend.models.fair_model import FairCreateInput
from backend.models.location_model import Location
from backend.services.fair_service import create_fair
from backend.services.location_service import list_locations
from backend.services.ride_service import list_rides_names_and_id
from frontend.const import field_value, mandatory_field_value


def submit_new_fair(fair: FairCreateInput) -> None:
    """
    Add the new fair.

    Args:
        fair (FairCreateInput): fair to create

    """
    try:
        validated_fair = FairCreateInput.model_validate(fair)
        create_fair(fair_create_input=validated_fair)
    except ValueError as e:
        json_error = json.loads(e.json())
        error_message: list[str] = [f"""{error["loc"]}: {error['type']}""" for error in json_error]
        ui.notify("\n".join(error_message), color="red")


def fair_create() -> None:
    """Wizard to create a fair."""
    fair: FairCreateInput = FairCreateInput.model_construct()
    rides_array: dict[str, str] = list_rides_names_and_id()
    locations: list[Location] = list_locations()

    with ui.row().classes("w-full flex-wrap items-start gap-6"):
        with ui.column().classes("w-full  md:w-5/12"):
            ui.label(field_value("FAIR_CREATE_FAIR")).classes("text-xl font-semibold")
            ui.label(mandatory_field_value("FAIR_INFORMATION"))
            ui.input(mandatory_field_value("FAIR_NAME")).bind_value(fair, "name").classes("w-full")

            with ui.grid(columns=2, rows=1).classes("w-full"):
                with ui.input(mandatory_field_value("FAIR_START_DATE")).bind_value(fair, "start_date").classes("w-full") as start_date:
                    with ui.menu() as menu:
                        ui.date().bind_value(start_date)
                    with start_date.add_slot("append"):
                        ui.icon("edit_calendar").on("click", menu.open).classes("cursor-pointer")

                with ui.input(mandatory_field_value("FAIR_END_DATE")).bind_value(fair, "end_date").classes("w-full") as end_date:
                    with ui.menu() as menu:
                        ui.date().bind_value(end_date)
                    with end_date.add_slot("append"):
                        ui.icon("edit_calendar").on("click", menu.open).classes("cursor-pointer")

            ui.label(mandatory_field_value("FAIR_LOCATION"))
            ui.select(
                {loc.id:loc.location_to_str() for loc in locations}, with_input=True, multiple=True,
                clearable=True, label=mandatory_field_value("FAIR_SEARCH_BY_CITY"),
            ).bind_value(fair, "locations").classes("w-full").props("use-chips")

            ui.label(mandatory_field_value("FAIR_RIDES_IN_THE_FAIR"))
            ui.select(
                rides_array,
                label=mandatory_field_value("FAIR_SELECT_RIDE_MESSAGE"),
                multiple=True, clearable=True,
            ).bind_value(fair, "rides").props("use-chips").classes("w-full")

            ui.input(label=field_value("FAIR_WALKTOUR_VIDEO"), placeholder="http://...").bind_value(fair, "walk_tour_video").classes("w-full")

            ui.label(text=field_value("FAIR_SOURCES"))
            ui.input(label=field_value("FAIR_AD_URL"), placeholder="http://..." ).bind_value(fair, "official_ad_page").classes("w-full")
            ui.input(label=field_value("FAIR_FACEBOOK_EVENT_PAGE_URL"), placeholder="http://...").bind_value(fair, "facebook_event_page").classes("w-full")
            ui.input(label=field_value("FAIR_CITY_PAGE"), placeholder="http://...").bind_value(fair, "city_event_page").classes("w-full")

            ui.button(field_value("SUBMIT"), on_click=lambda: submit_new_fair(fair))

        with ui.column().classes("w-full  md:w-5/12"):
            pass
