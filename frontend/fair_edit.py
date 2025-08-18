import json

from nicegui import ui

from backend.models.fair_model import Fair, FairUpdateInput
from backend.models.location_model import Location
from backend.services.fair_service import get_fair, update_fair
from backend.services.location_service import list_locations
from backend.services.ride_service import list_rides_names_and_id


def mandatory_field_value(value: str) -> str:
    """Return a translated field with an asterix meaning the field is required."""
    return f"{_(value)}*"

def submit_edit_fair(fair_id: str, fair_edit: FairUpdateInput) -> None:
    """
    Add the new fair.

    Args:
        fair_id (str): fair id
        fair_edit (FairUpdateInput): fair to edit

    """
    try:
        validated_fair = FairUpdateInput.model_validate(fair_edit)
        update_fair(fair_id=fair_id, fair_update_input=validated_fair)
    except ValueError as e:
        json_error = json.loads(e.json())
        error_message: list[str] = [f"""{error["loc"]}: {error['type']}""" for error in json_error]
        ui.notify("\n".join(error_message), color="red")


def fair_edit(fair_id: str) -> None:
    """Wizard to edit a fair."""
    fair: Fair = get_fair(fair_id=fair_id)

    rides_array: dict[str, str] = list_rides_names_and_id()
    locations: list[Location] = list_locations()
    locations_dict = {loc.id:loc.location_to_str() for loc in locations}

    fair_wrapper = fair.model_dump()
    fair_wrapper["locations"] = []
    locs_dict = fair.locations_str()
    for loc_id, loc in locations_dict.items():
        if loc in locs_dict:
            fair_wrapper["locations"].append(loc_id)

    fair_edit: FairUpdateInput = FairUpdateInput.model_validate(fair_wrapper)

    with ui.row().classes("w-full flex-wrap items-start gap-6"):
        with ui.column().classes("w-full  md:w-5/12"):
            ui.label(_("FAIR_EDIT_FAIR")).classes("text-xl font-semibold")
            ui.label(mandatory_field_value("FAIR_INFORMATION"))
            ui.input(mandatory_field_value("FAIR_NAME")).bind_value(fair_edit, "name").classes("w-full")

            with ui.grid(columns=2, rows=1).classes("w-full"):
                with ui.input(mandatory_field_value("FAIR_START_DATE")).bind_value(fair_edit, "start_date").classes("w-full") as start_date:
                    with ui.menu() as menu:
                        ui.date().bind_value(start_date)
                    with start_date.add_slot("append"):
                        ui.icon("edit_calendar").on("click", menu.open).classes("cursor-pointer")

                with ui.input(mandatory_field_value("FAIR_END_DATE")).bind_value(fair_edit, "end_date").classes("w-full") as end_date:
                    with ui.menu() as menu:
                        ui.date().bind_value(end_date)
                    with end_date.add_slot("append"):
                        ui.icon("edit_calendar").on("click", menu.open).classes("cursor-pointer")

            ui.label(mandatory_field_value("FAIR_LOCATION"))
            ui.select(
                locations_dict, with_input=True, multiple=True,
                clearable=True, label=mandatory_field_value("FAIR_SEARCH_BY_CITY"),
            ).bind_value(fair_edit, "locations").classes("w-full").props("use-chips")

            ui.label(mandatory_field_value("FAIR_RIDES_IN_THE_FAIR"))
            ui.select(
                rides_array,
                label=mandatory_field_value("FAIR_SELECT_RIDE_MESSAGE"),
                multiple=True, clearable=True,
            ).bind_value(fair_edit, "rides").props("use-chips").classes("w-full")

            ui.input(label=_("FAIR_WALKTOUR_VIDEO"), placeholder="http://...").bind_value(fair_edit, "walk_tour_video").classes("w-full")

            ui.label(_("FAIR_SOURCES"))
            ui.input(label=_("FAIR_AD_URL"), placeholder="http://..." ).bind_value(fair_edit, "official_ad_page").classes("w-full")
            ui.input(label=_("FAIR_FACEBOOK_EVENT_PAGE_URL"), placeholder="http://...").bind_value(fair_edit, "facebook_event_page").classes("w-full")
            ui.input(label=_("FAIR_CITY_PAGE"), placeholder="http://...").bind_value(fair_edit, "city_event_page").classes("w-full")

            ui.button(_("SUBMIT"), on_click=lambda: submit_edit_fair(fair_id=fair.id, fair_edit=fair_edit))

        with ui.column().classes("w-full  md:w-5/12"):
            pass
