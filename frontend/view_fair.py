from datetime import datetime

from dateutil.relativedelta import relativedelta

from backend.models.fairModel import Fair
from backend.services.fair_service import (
    list_fair_sort_by_status,
)
from backend.services.location_service import list_locations_cities
from pages.const import _
from pages.form_input import DotDict

search_fair_query = DotDict()
search_fair_query.date_min = (datetime.now() - relativedelta(months=2)).date()

def view_fair(ui) -> None:
    """List all fairs, apply filters if provided."""
    ui.label("Welcome to the other side")

    gantt_chart_pd = None
    data_map: list[dict[str, str]] = []
    fairs_struct: dict[str, list[Fair]] = {}
    fairs_by_status = list_fair_sort_by_status(search_fair_query=earch_fair_query)
    fairs_struct = fairs_by_status["fairs"]
    data_map = fairs_by_status["map"]
    gantt_chart_pd = fairs_by_status["gantt"]
    cities: list[dict[str, str]] = list_locations_cities()

    with ui.row():
        ui.label(_("FAIRS_LIST"))
        ui.button("Add fair", icon="add", on_click=lambda: ui.notify("You clicked me!"))
