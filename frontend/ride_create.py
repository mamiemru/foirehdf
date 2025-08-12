

import json

from nicegui import ui
from pydantic import BaseModel, Field, HttpUrl

from backend.models.ride_model import RideType
from backend.services.manufacturer_service import (
    create_manufacturer,
    list_manufacturers_names,
)
from backend.services.ride_service import create_ride, list_ride_types, list_rides_names
from pages.const import _


class RideCreateInput(BaseModel):
    """Describe the inputs to create a ride."""

    name: str
    owner: str | None
    ticket_price: float | None
    manufacturer: str | None
    technical_name: str | None
    ride_type: RideType | None
    manufacturer_page_url: HttpUrl | None
    description: str | None
    images_url: list[HttpUrl] = Field(default_factory=list)
    videos_url: list[HttpUrl] = Field(default_factory=list)
    news_page_url: HttpUrl | None


def add_manufacturer_dialog() -> None:
    """Open a dialog to create a new manufacturer."""
    name = ui.input(_("RIDE_NAME_OF_THE_MANUFACTURER"))
    if st.button(_("RIDE_SUBMIT")):
        create_manufacturer({"name": name})
        st.rerun()

def display_video_wizard(ride_create_input: RideCreateInput) -> None:
    """Display video wizard."""
    ui.label(_("RIDE_VIDEOS"))
    with ui.grid(rows=1, columns=2).classes("w-full"):
        video_url = ui.input(
            label=_("RIDE_VIDEOS_URL"), placeholder=_("RIDE_ENTER_A_VIDEO_URL_E_G_YOUTUBE_MP4_LINK"),
        )

        if ui.button(_("RIDE_ADD_VIDEO")):
            if video_url.value:
                ride_create_input.videos_url.append(HttpUrl(video_url.value))
            else:
                ui.label(_("RIDE_ERROR_VIDEO_URL"))

    if ride_create_input.videos_url:
        with ui.row().classes("w-full"):
            for i, vvideo_url in enumerate(ride_create_input.videos_url):
                with ui.column():
                    ui.label(str(vvideo_url))
                    ui.video(str(vvideo_url))
                with ui.column():
                    if ui.button(icon=":material/delete:"):
                        ride_create_input.videos_url.pop(i)

def append_ride_image(ride_create_input: RideCreateInput, url: str) -> None:
    """
    Add a new image to ride list.

    Args:
        ride_create_input (RideCreateInput): ride to create
        url (str): url to add

    """
    if url:
        ride_create_input.images_url.append(HttpUrl(url))
    else:
        ui.label(_("RIDE_PLEASE_ENTER_A_VALID_IMAGE_URL"))

def display_image_wizard(ride_create_input: RideCreateInput) -> None:
    """Display image wizard."""
    ui.label(_("RIDE_IMAGES"))
    with ui.grid(rows=1, columns=2).classes("w-full"):
        image_url = ui.input(
            label=_("RIDE_IMAGES_URL"), placeholder=_("RIDE_ENTER_A_IMAGE_URL"),
        )

        ui.button(_("RIDE_ADD_IMAGE"), on_click=lambda: append_ride_image(ride_create_input, image_url.value))

    if ride_create_input.images_url:
        with ui.row().classes("w-full"):
            for i, iimage_url in enumerate(ride_create_input.images_url):
                with ui.column():
                    ui.label(str(iimage_url))
                    ui.image(str(iimage_url))
                with ui.column():
                    if ui.button(icon=":material/delete:"):
                        ride_create_input.images_url.pop(i)

def submit_new_ride(ride: RideCreateInput) -> None:
    """
    Add the new ride.

    Args:
        ride (RideCreateInput): ride to create

    """
    print(ride)
    ui.notify(ride.model_dump())
    try:
        validated_ride = RideCreateInput.model_validate(ride)
        create_ride(validated_ride.model_dump())
    except ValueError as e:
        json_error = json.loads(e.json())
        error_message: list[str] = [f"""{error["loc"]}: {error['type']}""" for error in json_error]
        ui.notify("\n".join(error_message), color="red")


def ride_create() -> None:
    """Wizard to create a ride."""
    ui.label(_("RIDE_ADD_A_NEW_RIDE"))

    ride_create_input: RideCreateInput = RideCreateInput.model_construct()
    rides_names: list[str] = list_rides_names()
    manufacturer_names: list[str] = list_manufacturers_names()

    with ui.row().classes("w-full flex-wrap items-start gap-6"):
        with ui.column().classes("w-full  md:w-5/12"):
            ui.label(_("RIDE_GENERAL_INFORMATION"))

            ui.input(label=f"{_('RIDE_NAME')}*", placeholder=_("RIDE_NAME_OF_THE_RIDE")).bind_value(ride_create_input, "name").classes("w-full")
            if ride_create_input.name in rides_names:
                ui.label(_("RIDE_THIS_ATTRACTION_NAME_ALREADY_EXISTS"))

            ui.textarea(label=_("RIDE_DESCRIPTION"), placeholder=_("RIDE_A_SHORT_DESCRIPTION_OF_THE_RIDE")).bind_value(ride_create_input, "description").classes("w-full")
            ui.number(label=_("RIDE_TICKET_PRICE"), placeholder=_("RIDE_TICKET_PRICE")).bind_value(ride_create_input, "ticket_price").classes("w-full")

            ui.label(_("RIDE_MANUFACTURER_INFORMATION"))

            ui.select(label=_("RIDE_MANUFACTURER"), options=manufacturer_names).bind_value(ride_create_input, "manufacturer").classes("w-full")

            ui.input(
                label=_("RIDE_TECHNICAL_NAME"), placeholder=_("RIDE_THE_NAME_GIVEN_BY_THE_MANUFACTURER"),
            ).bind_value(ride_create_input, "technical_name").classes("w-full")

            ui.select(label=_("RIDE_ATTRACTION_TYPE"), options=list_ride_types()).bind_value(ride_create_input, "ride_type").classes("w-full")

            ui.input(
                label=_("RIDE_MANUFACTURER_PAGE"), placeholder=_("RIDE_ENTER_THE_URL_PAGE_OF_THE_MANUFACTURER_RIDE"),
            ).bind_value(ride_create_input, "manufacturer_page_url").classes("w-full")

            ui.label(_("RIDE_OWNER"))

            ui.input(label=_("RIDE_FAMILY_OWNER"), placeholder=_("RIDE_NAME_OF_THE_FAMILY_THAT_OWN_THE_RIDE")).bind_value(ride_create_input, "owner").classes("w-full")

            ui.label(_("RIDE_MEDIAS"))

            ui.input(
                _("RIDE_OFFICIAL_NEWS_PAGE_OF_THE_RIDE"), placeholder=_("RIDE_OFFICIAL_NEWS_PAGE_OR_FAN_PAGE"),
            ).bind_value(ride_create_input, "news_page_url").classes("w-full")


            display_video_wizard(ride_create_input)
            display_image_wizard(ride_create_input)

            ui.button(_("SUBMIT"), on_click=lambda: submit_new_ride(ride_create_input))

        with ui.column().classes("w-full  md:w-5/12"):
            pass
