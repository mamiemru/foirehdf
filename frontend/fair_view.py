

from nicegui import ui
from pydantic import HttpUrl

from backend.models.fairModel import Fair
from backend.models.location_model import LocationBase
from backend.services.fair_service import get_fair
from backend.services.ride_service import get_ride_by_id
from components.fair_timeline import fair_timeline
from components.image_loader import fetch_cached_image
from frontend.ride_box import display_ride_as_item_in_list
from pages.const import _


def icon_text(icon_name: str, text: str):
    with ui.row().classes("items-center gap-2"):
        ui.icon(icon_name)
        ui.label(text)

def get_markdown_link_table_row(td: str, url: HttpUrl) -> str:
    return f"| {_(td)} | [{url}]({url}) |\n"


def get_markdown_link_table(fair: Fair) -> str:
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


def location_to_str(location: LocationBase) -> str:
    return ", ".join([text for text in [
        location.street or "", location.area or "", location.city,
        location.postal_code, location.state, location.country,
    ] if text])



def fair_view(fair_id: str) -> None:
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
        icon_text("location_on", _("LOCATIONS"))
        ui.label(location_to_str(location)).classes("mb-2")

    with ui.row().classes("flex-wrap"):
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
            icon_text("map", _("FAIR_VIEW_SOURCES_AND_USEFUL_LINKS"))
            ui.markdown(get_markdown_link_table(fair)).classes("mb-4")

            ui.separator()

            with ui.grid(columns=3).classes("w-full flex-wrap justify-center"):
                for ride_id in fair.rides:
                    ride = get_ride_by_id(ride_id=ride_id)
                    if ride:
                        display_ride_as_item_in_list(_, ride)


        with ui.column().classes("w-full md:w-3/12"), ui.timeline(side="right"):
            ui.timeline_entry("Rodja and Falko start working on NiceGUI.",
                            title="Initial commit",
                            subtitle="May 07, 2021")
            ui.timeline_entry("The first PyPI package is released.",
                            title="Release of 0.1",
                            subtitle="May 14, 2021")
            ui.timeline_entry("Large parts are rewritten to remove JustPy "
                            "and to upgrade to Vue 3 and Quasar 2.",
                            title="Release of 1.0",
                            subtitle="December 15, 2022",
                            icon="rocket")
            ui.timeline_entry("Rodja and Falko start working on NiceGUI.",
                            title="Initial commit",
                            subtitle="May 07, 2021")
            ui.timeline_entry("The first PyPI package is released.",
                            title="Release of 0.1",
                            subtitle="May 14, 2021")
            ui.timeline_entry("Large parts are rewritten to remove JustPy "
                            "and to upgrade to Vue 3 and Quasar 2.",
                            title="Release of 1.0",
                            subtitle="December 15, 2022",
                            icon="rocket")
            ui.timeline_entry("Rodja and Falko start working on NiceGUI.",
                            title="Initial commit",
                            subtitle="May 07, 2021")
            ui.timeline_entry("The first PyPI package is released.",
                            title="Release of 0.1",
                            subtitle="May 14, 2021")
            ui.timeline_entry("Large parts are rewritten to remove JustPy "
                            "and to upgrade to Vue 3 and Quasar 2.",
                            title="Release of 1.0",
                            subtitle="December 15, 2022",
                            icon="rocket")
