
from nicegui import ui

from backend.models.fair_model import Fair
from backend.models.ride_model import Ride
from backend.services.fair_service import list_fairs_containing_ride_id
from components.image_loader import fetch_cached_image
from frontend.const import _, field_value, youtube_video_player


def display_fair(fair: Fair) -> None:
    """Display an entry to a fair which had the concerned ride."""
    ui.label(f"{fair.name}").classes("text-xl font-bold")
    ui.label(fair.first_location_str()).classes("text-gray-700")
    ui.label(f'Du {fair.start_date.strftime("%d %B %Y")} au {fair.end_date.strftime("%d %B %Y")}').classes("text-gray-700")


def ride_view(ride: Ride) -> None:
    """Display full ride view layout in NiceGUI."""
    with ui.row().classes("w-full flex-wrap items-start gap-6"):
        with ui.column().classes("w-full  md:w-6/12"):

            ui.label(ride.name).classes("text-4xl font-bold text-orange-500 mb-4")
            if ride.description:
                    ui.markdown(ride.description).classes("mb-4")

            with ui.row().classes("w-full"):
                if ride.ticket_price:
                    ui.markdown(f"**{_('RIDE_TICKET_PRICE')}:** €{ride.ticket_price}").classes("bg-yellow-300 text-black text-sm px-2 py-1 rounded font-semibold")
                if ride.manufacturer:
                    ui.markdown(f"**{_('RIDE_MANUFACTURER')}:** {ride.manufacturer}").classes("bg-red-500 text-white text-sm px-2 py-1 rounded font-semibold")
                if ride.technical_name:
                    ui.markdown(f"**{_('RIDE_TECHNICAL_NAME')}:** {ride.technical_name}").classes("bg-green-500 text-white text-sm px-2 py-1 rounded font-semibold")
                if ride.ride_type:
                    ui.markdown(f"**{_('RIDE_ATTRACTION_TYPE')}:** {ride.ride_type}").classes("bg-blue-500 text-white text-sm px-2 py-1 rounded font-semibold")
                if ride.owner:
                    ui.markdown(f"**{_('RIDE_OWNER')}:** {ride.owner}").classes("bg-gray-300 text-black text-sm px-2 py-1 rounded font-semibold")
                if ride.manufacturer_page_url:
                    ui.markdown(f"**{_('RIDE_MANUFACTURER_PAGE')}:** [Link]({ride.manufacturer_page_url})").classes("bg-pink-300 text-black text-sm px-2 py-1 rounded font-semibold")
                if ride.news_page_url:
                    ui.markdown(f"**{_('RIDE_NEWS_PAGE')}:** [Link]({ride.news_page_url})").classes("bg-orange-300 text-black text-sm px-2 py-1 rounded font-semibold")

        with ui.column().classes("w-full  md:w-5/12 item-end"):
            if ride.images_url:
                image = fetch_cached_image(ride.images_url[0])
                if image:
                    ui.image(image).classes("w-full rounded shadow")

    ui.separator()

    with ui.tabs().classes("w-full space-arround") as ride_tabs:
        ui.tab("ride_history", label=field_value("RIDE_WAS_INSTALLED_IN_FAIRS"), icon="attractions")
        ui.tab("videos", label=field_value("RIDE_LIST_OF_VIDEOS"), icon="videocam")
        ui.tab("images", label=field_value("RIDE_LIST_OF_IMAGES"), icon="image")

    with ui.tab_panels(ride_tabs, value="ride_history").classes("w-full"):
        with ui.tab_panel("ride_history"):
            ui.label(field_value("RIDE_WAS_INSTALLED_IN_FAIRS")).classes("text-2xl font-semibold mb-2")
            with ui.grid(columns=3):
                for fair in list_fairs_containing_ride_id(ride.id):
                    display_fair(fair=fair)

        with ui.tab_panel("videos"):
            ui.label(field_value("RIDE_LIST_OF_VIDEOS")).classes("text-2xl font-semibold mb-2")
            with ui.row().classes("w-full flex-wrap"):
                for url in ride.videos_url:
                    with ui.column().classes("w-1/3 p-2"):
                        youtube_video_player(url)

        with ui.tab_panel("images"):
            ui.label(field_value("RIDE_LIST_OF_IMAGES")).classes("text-2xl font-semibold mb-2")
            with ui.row().classes("w-full flex-wrap"):
                for url in ride.images_url:
                    with ui.column().classes("w-1/3 p-2"):
                        ui.image(str(url)).classes("w-full rounded shadow-md")
