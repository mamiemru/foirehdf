from io import BytesIO
from pathlib import Path

import requests
from nicegui import ui
from PIL import Image
from pydantic import HttpUrl

from backend.models.ride_model import Ride


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
    ui.navigate.to(f"/ride_view/{ride_id}")


def display_ride_as_item_in_list(_, ride: Ride) -> None:
    """Display a ride in a card-style layout using NiceGUI."""
    with ui.card().classes("w-full p-4 mb-4"), ui.row().classes("w-full items-start"):
        if ride.images_url:
            ui.image(str(ride.images_url[0])).classes("w-full h-auto rounded mb-2")

        with ui.card_section().classes("w-full"):
            ui.label(ride.name).classes("text-2xl font-bold text-orange-500 mb-2")

            with ui.grid(columns=2).classes("gap-2 flex-wrap"):
                ui.label(ride.ride_type).classes("bg-blue-500 text-white text-sm px-2 py-1 rounded font-semibold")
                ui.label(ride.manufacturer or "_").classes("bg-red-500 text-white text-sm px-2 py-1 rounded font-semibold")
                ui.label(ride.technical_name or "_").classes("bg-green-500 text-white text-sm px-2 py-1 rounded font-semibold")
                ui.label(f"{ride.ticket_price:.2f} €").classes("bg-yellow-300 text-black text-sm px-2 py-1 rounded font-semibold")

            ui.button( _("VIEW_RIDE_DETAILS"),on_click=lambda: view_ride_details(ride.id)).props("unelevated color=primary").classes("w-full mt-5")
