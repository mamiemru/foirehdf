from datetime import datetime

import plotly.express as px
from dateutil.relativedelta import relativedelta
from nicegui import ui

from backend.models.fairModel import Fair, FairStatus
from backend.services.fair_service import (
    list_fair_sort_by_status,
)
from backend.services.location_service import list_locations_cities
from components.fair_timeline import fair_timeline
from pages.const import _
from pages.form_input import DotDict

search_fair_query = DotDict()

def reset_search_fair_query() -> None:
    """Reset search fair query."""
    search_fair_query.date_min = (datetime.now() - relativedelta(months=1)).date()
    search_fair_query.date_max = (datetime.now() + relativedelta(months=6)).date()
    search_fair_query.cities = []

reset_search_fair_query()

def view_fair(fair_id: int) -> None:
    """Simulate navigation to fair details page."""
    ui.navigate.to(f"/fair_view/{fair_id}")


def display_fair_item(fair: Fair) -> None:
    """
    Display a fair in a box.

    Args:
        ui (niceguid): niceguidhandler
        fair (Fair): the fair to display

    """
    with ui.card().classes("w-full p-4"):
        with ui.row().classes("items-center justify-between"):
            ui.label(fair.name).classes("text-xl font-semibold")

            ui.button(_("FAIR_VIEW_FAIR"), icon="visibility", on_click=lambda: view_fair(fair.id)).props("unelevated color=primary")

        # Locations
        ui.label(f"📍 {_('LOCATIONS')}").classes("mt-2 font-medium")
        for location in fair.locations:
            address_parts = [
                location.street or "",
                location.area or "",
                location.city,
                location.postal_code,
                location.state,
                location.country,
            ]
            address = ", ".join([part for part in address_parts if part])
            ui.label(address).classes("text-sm text-gray-600")

        # Dates
        fair_timeline(fair, draw_bars=False)


def fair_list() -> None:  # type: ignore  # noqa: PGH003
    """
    List all fairs, apply filters if provided.

    Args:
        ui (niceguid): niceguidhandler

    """
    gantt_chart_pd = None
    fairs_struct: dict[str, list[Fair]] = {}
    fairs_by_status = list_fair_sort_by_status(search_fair_query=search_fair_query)
    fairs_struct = fairs_by_status["fairs"]
    data_map = fairs_by_status["map"]
    gantt_chart_pd = fairs_by_status["gantt"]
    cities: list[dict[str, str]] = list_locations_cities()

    with ui.row().classes("w-full items-center justify-between"):
        ui.label(_("FAIRS_LIST")).style("color: #6E93D6; font-size: 200%; font-weight: 300").classes("w-3/5")
        ui.button("Add fair", icon="add", on_click=lambda: ui.notify("You clicked me!")).classes("w-1/5")

    with ui.expansion(_("FAIR_SEARCH_TITLE"), icon="search").classes("w-full"):
        ui.select(cities, multiple=True, value=search_fair_query.cities, label=_("FAIR_SEARCH_BY_CITY")).classes("w-64").props("use-chips").bind_value(search_fair_query, "cities")

        with ui.row().classes("w-full"):
            with ui.input(_("FAIR_SEARCH_BY_MIN_DATE")).bind_value(search_fair_query, "date_min") as date_input_min:
                with ui.menu() as menu:
                    ui.date().bind_value(date_input_min)
                with date_input_min.add_slot("append"):
                    ui.icon("edit_calendar").on("click", menu.open).classes("cursor-pointer")

            with ui.input(_("FAIR_SEARCH_BY_MAX_DATE")).bind_value(search_fair_query, "date_max") as date_input_max:
                with ui.menu() as menu:
                    ui.date().bind_value(date_input_max)
                with date_input_max.add_slot("append"):
                    ui.icon("edit_calendar").on("click", menu.open).classes("cursor-pointer")

        with ui.row().classes("w-full"):
            ui.button(_("FAIR_SEARCH_BUTTON"), icon="search", on_click=lambda: fairs_by_status.update(list_fair_sort_by_status(search_fair_query=search_fair_query)))
            ui.button(_("FAIR_SEARCH_BUTTON_RESET"), icon="close", on_click=reset_search_fair_query)

    ui.label().bind_text_from(search_fair_query)

    color_map = {
        FairStatus.CURRENTLY_AVAILABLE: "#33cc33",
        FairStatus.INCOMING: "#ff9900",
        FairStatus.DONE: "#0066cc",
    }
    fig = px.timeline(
        gantt_chart_pd,x_start="start",x_end="finish",y="task",color="status",
        hover_data={"name": True,"start_date": True,"end_date": True,"date": True},
        color_discrete_map=color_map,
    )
    fig.update_yaxes(title_text=_("CITY"), autorange="reversed")
    fig.update_xaxes(title_text=_("FAIR_DATES"))
    fig.update_layout(coloraxis_showscale=False)
    ui.plotly(fig).classes("w-full")

    ui.label(_("FAIR_LIST_FUNFAIRS_CURRENTLY_AVAILABLE_TODAY")).classes("mb-4 text-h3")
    with ui.row().classes("w-full flex-wrap align-center space-between"):
        with ui.column().classes("w-full  md:w-6/12"), ui.scroll_area().classes("w-full").style("height: 500px"):
            if fairs_struct[FairStatus.CURRENTLY_AVAILABLE]:
                fairs_struct[FairStatus.CURRENTLY_AVAILABLE].reverse()
                for fair in fairs_struct[FairStatus.CURRENTLY_AVAILABLE]:
                    display_fair_item(fair)
            else:
                ui.label(_("FAIR_NO_FAIRS_CURRENTLY_AVAILABLE"))

        with ui.column().classes("w-full md:w-5/12"):
            options = {"zoomControl": False,"scrollWheelZoom": False, "doubleClickZoom": False, "boxZoom": False, "keyboard": False, "dragging": False}
            lfmap = ui.leaflet(center=(50.5, 2), zoom=8, options=options).classes("w-90 h-[500px]")
            for row in data_map:
                lfmap.marker(latlng=(row["lat"], row["lng"]), options={"color": "red"})

    ui.label(_("FAIR_LIST_FUNFAIRS_COMING_SOON")).classes("mb-4 text-h3")
    if fairs_struct[FairStatus.INCOMING]:
        fairs_struct[FairStatus.INCOMING].reverse()
        for fair in fairs_struct[FairStatus.INCOMING]:
            display_fair_item(fair)
    else:
        ui.label(_("FAIR_NO_FAIRS_COMMING_SOON"))

    ui.label(_("FAIR_LIST_FUNFAIRS_DONE")).classes("mb-4 text-h3")
    if fairs_struct[FairStatus.DONE]:
        fairs_struct[FairStatus.DONE].reverse()
        for fair in fairs_struct[FairStatus.DONE]:
            display_fair_item(fair)
    else:
        ui.label(_("FAIR_NO_FAIRS_DONE"))
