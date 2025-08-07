
from nicegui import ui

from backend.models.fairModel import Fair
from backend.models.ride_model import Ride
from backend.services.fair_service import list_fairs_containing_ride_id
from components.image_loader import fetch_cached_image
from pages.const import _


def display_fair(fair: Fair):
    location = ", ".join([
        text for text in [
            fair.locations[0].street or "", fair.locations[0].area or "", fair.locations[0].city,
            fair.locations[0].postal_code, fair.locations[0].state,
        ] if text
    ])
    ui.label(f"🎡 {fair.name}").classes("text-xl font-bold")
    ui.label(location).classes("text-gray-700")
    ui.label(f'Du {fair.start_date.strftime("%d %B %Y")} au {fair.end_date.strftime("%d %B %Y")}').classes("text-gray-700")


def ride_view(ride: Ride) -> None:
    """Display full ride view layout in NiceGUI."""
    with ui.row().classes("w-full flex-wrap items-start gap-6"):
        # --- Left Column (ride info) ---
        with ui.column().classes("w-full  md:w-6/12"):

            ui.label(ride.name).classes("text-4xl font-bold text-orange-500 mb-4")
            if ride.description:
                    ui.markdown(ride.description).classes("mb-4")

            with ui.grid(columns=2).classes("w-full"):
                ui.markdown(f"**{_('RIDE_TICKET_PRICE')}:** €{ride.ticket_price}").classes("bg-yellow-300 text-black text-sm px-2 py-1 rounded font-semibold")
                ui.markdown(f"**{_('RIDE_MANUFACTURER')}:** {ride.manufacturer}").classes("bg-red-500 text-white text-sm px-2 py-1 rounded font-semibold")
                ui.markdown(f"**{_('RIDE_TECHNICAL_NAME')}:** {ride.technical_name}").classes("bg-green-500 text-white text-sm px-2 py-1 rounded font-semibold")
                ui.markdown(f"**{_('RIDE_ATTRACTION_TYPE')}:** {ride.ride_type}").classes("bg-blue-500 text-white text-sm px-2 py-1 rounded font-semibold")

                if ride.owner:
                    ui.markdown(f"**{_('RIDE_OWNER')}:** {ride.owner}").classes("bg-gray-300 text-black text-sm px-2 py-1 rounded font-semibold")
                if ride.manufacturer_page_url:
                    ui.markdown(f"**{_('RIDE_MANUFACTURER_PAGE')}:** [Link]({ride.manufacturer_page_url})").classes("bg-pink-300 text-black text-sm px-2 py-1 rounded font-semibold")
                if ride.news_page_url:
                    ui.markdown(f"**{_('RIDE_NEWS_PAGE')}:** [Link]({ride.news_page_url})").classes("bg-orange-300 text-black text-sm px-2 py-1 rounded font-semibold")

        # --- Right Column (admin + image) ---
        with ui.column().classes("w-full  md:w-5/12 item-end"):

            #ui.button(icon="edit", on_click=lambda: go_to_edit_ride(ride.id)).props("round flat color=primary")

            if ride.images_url:
                image = fetch_cached_image(ride.images_url[0])
                if image:
                    ui.image(image).classes("w-full rounded shadow")

    ui.separator()

    # --- Section: Fairs where ride was installed ---
    ui.label(_("RIDE_WAS_INSTALLED_IN_FAIRS")).classes("text-2xl font-semibold mb-2")

    with ui.grid(columns=3):
        for fair in list_fairs_containing_ride_id(ride.id):
            display_fair(fair=fair)

    ui.separator()

    with ui.row().classes("w-full flex-wrap"):
        for url in ride.videos_url:
            with ui.column().classes("w-1/3 p-2"):
                ui.video(str(url)).classes("w-full rounded shadow-md")

    ui.separator()

    with ui.row().classes("w-full flex-wrap"):
        for url in ride.images_url:
            with ui.column().classes("w-1/3 p-2"):
                ui.image(str(url)).classes("w-full rounded shadow-md")
