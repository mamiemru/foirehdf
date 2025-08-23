

from datetime import datetime

from nicegui import ui
from pydantic import HttpUrl

from backend.models.fair_model import Fair
from backend.models.ride_model import Ride
from backend.models.timeline_model import TimelineItemType
from backend.services.fair_service import get_fair
from backend.services.ride_service import get_ride_by_id
from components.fair_timeline import fair_timeline
from components.image_loader import fetch_cached_image
from frontend.const import _, field_value
from frontend.ride_box import display_rides_wizard


def icon_text(icon_name: str, text: str) -> None:
    """Display a text with an icon prepend."""
    with ui.row().classes("items-center gap-2"):
        ui.icon(icon_name)
        ui.label(text)

def get_markdown_link_table_row(td: str, url: HttpUrl) -> str:
    """Return a markdown row with url and title."""
    return f"| {_(td)} | [{url}]({url}) |\n"


def get_markdown_link_table(fair: Fair) -> str:
    """Return a markdown list of urls."""
    markdown_table = f"| {_('FAIR_URL_TYPE')} | {_('FAIR_URL')} |\n"
    markdown_table += "|------|------|\n"

    if fair.official_ad_page:
        markdown_table += get_markdown_link_table_row("FAIR_AD_URL", fair.official_ad_page)
    if fair.city_event_page:
        markdown_table += get_markdown_link_table_row("FAIR_CITY_PAGE", fair.city_event_page)
    if fair.facebook_event_page:
        markdown_table += get_markdown_link_table_row("FAIR_FACEBOOK_EVENT_PAGE_URL", fair.facebook_event_page)
    if fair.walk_tour_video:
        markdown_table += get_markdown_link_table_row("FAIR_WALKTOUR_VIDEO", fair.walk_tour_video)

    for url in fair.sources:
        markdown_table += get_markdown_link_table_row("FAIR_VIEW_OTHER", url)
    return markdown_table

def timeline_in_the_past(d: datetime) -> str:
    """Return blue if the event is in comming, grey otherwise."""
    return "grey" if d < datetime.today() else "blue"

def timeline_item_icon(t: TimelineItemType | None) -> str:
    """Return the right icon according to the timeline item."""
    if t == TimelineItemType.RIDE_AVAILABLE:
        return "add"
    if t == TimelineItemType.RIDE_LEAVING:
        return "remove"
    return "rocket"

def fair_view(fair_id: str) -> None:
    """Display all information about a fair."""
    fair: Fair = get_fair(fair_id=fair_id)

    # Header
    with ui.row().classes("w-full items-center justify-between"):
        ui.label(fair.name).classes("text-3xl font-bold text-primary")
        ui.button(icon="edit", on_click=lambda: ui.navigate.to(f"/fair_edit/{fair.id}")).props("flat")

    with ui.row().classes("w-full mt-4 gap-6"):
        location = fair.locations[0]
        if location.lat and location.lng:
            options = {"keyboard": False, "dragging": False}
            lfmap = ui.leaflet(center=(50.5, 2), zoom=8, options=options).classes("w-full h-[500px]")
            lfmap.marker(latlng=(location.lat, location.lng), options={"color": "red","autoPanOnFocus": True})
        icon_text("location_on", field_value("LOCATIONS"))
        ui.label(fair.first_location_str()).classes("mb-2")

    with ui.row().classes("w-full flex-wrap justify-around"):
        with ui.column().classes("w-full md:w-8/12"):

            fair_timeline(fair)

            with ui.column().classes("w-1/3"):
                if fair.official_ad_page:
                    banner = fetch_cached_image(fair.official_ad_page)
                    if banner:
                        ui.image(banner).classes("w-full rounded shadow mb-2")
                for image in fair.images:
                    img = fetch_cached_image(image)
                    if img:
                        ui.image(img).classes("w-full rounded shadow mb-2")

            ui.separator()
            icon_text("map", field_value("FAIR_VIEW_SOURCES_AND_USEFUL_LINKS"))
            ui.markdown(get_markdown_link_table(fair)).classes("mb-4 w-full")

            ui.separator()

            rides: list[Ride] = [get_ride_by_id(ride_id=ride_id) for ride_id in fair.rides]
            display_rides_wizard(rides=rides)

        with ui.column().classes("w-full md:w-3/12"), ui.card().classes("w-full"), ui.timeline(side="right"):
            ui.timeline_entry(
                title="Fin de la foire.",
                subtitle=fair.end_date.strftime("%d %B"),
                icon="close",
                color=timeline_in_the_past(fair.end_date),
            )
            if fair.timeline:
                for item in fair.timeline.line:
                    ui.timeline_entry(
                        item.description,
                        title=item.title,
                        subtitle=item.date.strftime("%d %B"),
                        icon=timeline_item_icon(item.type),
                        color=timeline_in_the_past(item.date),
                    )
            ui.timeline_entry(
                title="Début de la foire",
                subtitle=fair.start_date.strftime("%d %B"),
                icon="auto_awesome",
                color=timeline_in_the_past(fair.start_date),
            )
