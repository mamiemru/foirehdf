
import plotly.express as px
from nicegui import app, ui
from pandas import DataFrame

from backend.models.fair_model import Fair, FairStatus, SearchFairQuery, SearchFairResult
from backend.services.fair_service import list_fair_sort_by_status
from backend.services.location_service import list_locations_cities
from components.fair_timeline import fair_timeline
from frontend.const import field_value


def display_fairs_list(fairs: list[Fair]) -> None:
    """
    Display a list of fairs in a box.

    Args:
        fairs (list[Fair]): the fair to display

    """

    def closure_fair(fair: Fair): # type: ignore
        """Ensure the right fair is called by the on_clock below."""
        return lambda: ui.navigate.to(f"/fair-view/{fair.id}")

    with ui.list().props("separator").classes("w-full"):
        for fair in fairs:
            with ui.item(on_click=closure_fair(fair)).classes("w-full"), ui.item_section():
                    ui.label(fair.name).classes("text-xl font-semibold")
                    for location in fair.locations_str():
                        ui.label(location).classes("text-sm text-gray-600")
                    fair_timeline(fair, draw_bars=False)

def display_gantt(gantt_chart_pd: DataFrame) -> None:
    """Display the gantt graph."""
    color_map = {
        FairStatus.CURRENTLY_AVAILABLE: "#33cc33",
        FairStatus.INCOMING: "#ff9900",
        FairStatus.DONE: "#0066cc",
    }
    if not gantt_chart_pd.empty:
        fig = px.timeline(
            gantt_chart_pd,x_start="start",x_end="finish",y="task",color="status",
            hover_data={"name": True,"start_date": True,"end_date": True,"date": True},
            color_discrete_map=color_map, height=max(len(gantt_chart_pd)*50, 200),
        )
        fig.update_yaxes(title_text=field_value("CITY"), autorange="reversed")
        fig.update_xaxes(title_text=field_value("FAIR_DATES"))
        fig.update_layout(coloraxis_showscale=False)
        with ui.card().classes("w-full"):
            ui.plotly(fig).classes("w-full")

@ui.refreshable
def display_fairs() -> None:
    """Display filtered fairs, need decorators to be dynamic."""
    search_fair_result: SearchFairResult = list_fair_sort_by_status(search_fair_query=app.storage.client["search_fair_query"])
    display_gantt(gantt_chart_pd=search_fair_result.gantt)

    with ui.row().classes("w-full flex-wrap align-center space-between"):
        with ui.column().classes("w-full  md:w-6/12"), ui.card().classes("w-full"):
            ui.label(field_value("FAIR_LIST_FUNFAIRS_CURRENTLY_AVAILABLE_TODAY")).classes("mb-4 text-h5 text-grey-8")
            with ui.scroll_area().classes("w-full h-[500px]"):
                if search_fair_result.fairs[FairStatus.CURRENTLY_AVAILABLE]:
                    search_fair_result.fairs[FairStatus.CURRENTLY_AVAILABLE].reverse()
                    display_fairs_list(fairs=search_fair_result.fairs[FairStatus.CURRENTLY_AVAILABLE])
                else:
                    ui.label(field_value("FAIR_NO_FAIRS_CURRENTLY_AVAILABLE"))

        with ui.column().classes("w-full md:w-5/12"):
            options = {"zoomControl": False,"scrollWheelZoom": False, "doubleClickZoom": False, "boxZoom": False, "keyboard": False, "dragging": False}
            lfmap = ui.leaflet(center=(50.5, 2), zoom=8, options=options).classes("w-90 h-[500px]")
            for fair_marker in search_fair_result.map:
                lfmap.marker(latlng=(fair_marker.lat, fair_marker.lng), options={"color": fair_marker.color})

    with ui.card().classes("w-full"):
        ui.label(field_value("FAIR_LIST_FUNFAIRS_COMING_SOON")).classes("mb-4 text-h5 text-grey-8")
        if search_fair_result.fairs[FairStatus.INCOMING]:
            search_fair_result.fairs[FairStatus.INCOMING].reverse()
            display_fairs_list(fairs=search_fair_result.fairs[FairStatus.INCOMING])
        else:
            ui.label(field_value("FAIR_NO_FAIRS_COMMING_SOON"))

    if search_fair_result.fairs[FairStatus.DONE]:
        with ui.card().classes("w-full"):
            ui.label(field_value("FAIR_LIST_FUNFAIRS_DONE")).classes("mb-4 text-h5 text-grey-8")
            search_fair_result.fairs[FairStatus.DONE].reverse()
            display_fairs_list(fairs=search_fair_result.fairs[FairStatus.DONE])


def refresh_fairs_list(search_fair_query: SearchFairQuery) -> None:
    """Refresh the page in one function call."""
    app.storage.client["search_fair_query"] = search_fair_query
    display_fairs.refresh()

def reset_fairs_list(search_fair_query: SearchFairQuery) -> None:
    """Reset filter and refresh the page in one function call."""
    search_fair_query.reset()
    app.storage.client["search_fair_query"] = search_fair_query
    display_fairs.refresh()

def display_search_expansion(search_fair_query: SearchFairQuery) -> None:
    """Display search expansion information."""
    cities: list[str] = list_locations_cities()
    cities.sort(key=lambda c: c)
    with ui.expansion(field_value("FAIR_SEARCH_TITLE"), icon="search").classes("w-full"):
        ui.select(cities, multiple=True, label=field_value("FAIR_SEARCH_BY_CITY")).bind_value(search_fair_query, "cities").classes("w-1/3").props("use-chips")

        with ui.row().classes("w-full"):
            with ui.input(field_value("FAIR_SEARCH_BY_MIN_DATE")).bind_value(search_fair_query, "date_min") as date_input_min:
                with ui.menu() as menu:
                    ui.date().bind_value(date_input_min)
                with date_input_min.add_slot("append"):
                    ui.icon("edit_calendar").on("click", menu.open).classes("cursor-pointer")

            with ui.input(field_value("FAIR_SEARCH_BY_MAX_DATE")).bind_value(search_fair_query, "date_max") as date_input_max:
                with ui.menu() as menu:
                    ui.date().bind_value(date_input_max)
                with date_input_max.add_slot("append"):
                    ui.icon("edit_calendar").on("click", menu.open).classes("cursor-pointer")

        with ui.row().classes("w-full"):
            ui.button(field_value("FAIR_SEARCH_BUTTON"), icon="search", on_click=lambda: refresh_fairs_list(search_fair_query))
            ui.button(field_value("FAIR_SEARCH_BUTTON_RESET"), icon="close", on_click=lambda: reset_fairs_list(search_fair_query))

def fair_list(search_fair_query: SearchFairQuery) -> None:
    """List all fairs, apply filters if provided."""
    app.storage.client["search_fair_query"] = search_fair_query
    with ui.row().classes("w-full items-center justify-between"):
        ui.label(field_value("FAIRS_LIST")).style("color: #6E93D6; font-size: 200%; font-weight: 300").classes("w-3/5")
        ui.button("Add fair", icon="add", on_click=lambda: ui.navigate.to("/fair_create")).classes("w-1/5")

    display_search_expansion(search_fair_query=search_fair_query)
    refresh_fairs_list(search_fair_query=search_fair_query)
    display_fairs()
