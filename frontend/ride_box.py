from io import BytesIO
from pathlib import Path

import requests
from nicegui import app, ui
from PIL import Image
from pydantic import HttpUrl

from backend.models.ride_model import Ride
from frontend.const import field_value


def _fetch_cached_image(url: str) -> Image.Image | None:
    """Fetch and cache an image from a URL."""
    response = requests.get(str(url), timeout=10)

    if response.status_code == 200:

        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            return None

        return Image.open(BytesIO(response.content))

    return None


def fetch_cached_image(url: HttpUrl | str) -> Image.Image | None:
    """Parse any url to string in order to fetch it."""
    image = _fetch_cached_image(str(url))
    if image:
        return image

    return Image.open(Path(__file__).parent.parent / "statics" / "image-not-found.jpg")


def view_ride_details(ride_id: int) -> None:
    """Navigate to the ride details page with ride_id."""
    ui.navigate.to(f"/ride-view/{ride_id}")


def display_ride_as_item_in_list(ride: Ride) -> None:
    """Display a ride in a list item-style layout using NiceGUI."""
    with ui.item_section().props("image"):
        if ride.images_url:
            ui.image(str(ride.images_url[0])).classes("w-full h-auto rounded mb-2")

    with ui.item_section().classes("flex-wrap justify-center"):
        ui.label(ride.name).classes("text-2xl font-bold text-orange-500 mb-2")
        with ui.row().classes("gap-2 flex-wrap"):
            if ride.ride_type:
                ui.label(ride.ride_type).classes("bg-blue-500 text-white text-sm px-2 py-1 rounded font-semibold")
            if ride.manufacturer:
                ui.label(ride.manufacturer).classes("bg-red-500 text-white text-sm px-2 py-1 rounded font-semibold")
            if ride.technical_name:
                ui.label(ride.technical_name).classes("bg-green-500 text-white text-sm px-2 py-1 rounded font-semibold")
            if ride.ticket_price:
                ui.label(f"{ride.ticket_price:.2f} €").classes("bg-yellow-300 text-black text-sm px-2 py-1 rounded font-semibold")

    with ui.item_section().props("side"):
        ui.button( field_value("VIEW_RIDE_DETAILS"),on_click=lambda: view_ride_details(ride.id)).props("unelevated color=primary").classes("w-full mt-5")


def display_ride_as_item_in_card(ride: Ride) -> None:
    """Display a ride in a card-style layout using NiceGUI."""
    with ui.card().classes("w-full p-4 mb-4"), ui.row().classes("w-full items-start"):
        if ride.images_url:
            ui.image(str(ride.images_url[0])).classes("w-full h-auto rounded mb-2")

        with ui.card_section().classes("w-full"):
            ui.label(ride.name).classes("text-2xl font-bold text-orange-500 mb-2")

            with ui.row().classes("gap-2 flex-wrap"):
                if ride.ride_type:
                    ui.label(ride.ride_type).classes("bg-blue-500 text-white text-sm px-2 py-1 rounded font-semibold")
                if ride.manufacturer:
                    ui.label(ride.manufacturer).classes("bg-red-500 text-white text-sm px-2 py-1 rounded font-semibold")
                if ride.technical_name:
                    ui.label(ride.technical_name).classes("bg-green-500 text-white text-sm px-2 py-1 rounded font-semibold")
                if ride.ticket_price:
                    ui.label(f"{ride.ticket_price:.2f} €").classes("bg-yellow-300 text-black text-sm px-2 py-1 rounded font-semibold")

            ui.button( field_value("VIEW_RIDE_DETAILS"),on_click=lambda: view_ride_details(ride.id)).props("unelevated color=primary").classes("w-full mt-5")

@ui.refreshable
def _display_rides(rides: list[Ride]) -> None:
    ui.label().bind_text_from(app.storage.client["layout_grid"])
    ui.notify(app.storage.client["layout_grid"])
    if app.storage.client["layout_grid"]:
        with ui.row().classes("w-full flex-wrap justify-center"):
            for ride in rides:
                with ui.column().classes("w-full sm:w-1/2 md:w-1/3 lg:w-1/4 p-2"):
                    display_ride_as_item_in_card(ride=ride)

    else:
        with ui.list().props("bordered separator").classes("w-full flex-wrap justify-center"):
            for ride in rides:
                with ui.item(on_click=lambda: ui.notify("Selected contact 1")):
                    display_ride_as_item_in_list(ride=ride)


def display_rides_wizard(rides: list[Ride]) -> None:
    """Wizard to display a list of rides."""
    ui.toggle({0:"Liste", 1:"Grid"}, value=1, on_change=lambda: _display_rides.refresh()).bind_value(app.storage.client, "layout_grid")
    _display_rides(rides=rides)
