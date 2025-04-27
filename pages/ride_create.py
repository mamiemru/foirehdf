import gettext

import gettext
import streamlit as st
from typing import List

from backend.endpoints.attractionsEndpoint import create_attraction_endpoint
from backend.endpoints.attractionsEndpoint import list_attractions_names_endpoint
from backend.endpoints.manufacturerEndpoint import list_manufacturer_names_endpoint

from backend.models.attractionModel import AttractionType

from backend.dto.error_dto import ErrorResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse
from backend.dto.list_dto import ListResponse

_ = gettext.gettext


@st.dialog(_("add manufacturer"))
def add_manufacturer_dialog():
    name = st.text_input(_("Name of the manufacturer*"))
    if st.button(_("submit")):
        response: ResponseDto = create_attraction_endpoint({"name": name})
        if isinstance(response, SuccessResponse):
            st.success(response.message, icon=":material/check_circle:")
            st.rerun()
        elif isinstance(response, ErrorResponse):
            st.error(response.message, icon=":material/close:")
            st.error(response.errors, icon=":material/close:")


def ride_create():
    st.header(_("Add a new ride"))

    rides_names: List[str] = list()
    response: ResponseDto = list_attractions_names_endpoint()
    if isinstance(response, ListResponse):
        rides_names: List[str] = response.data

    manufacturer_names: List[str] = list()
    response: ResponseDto = list_manufacturer_names_endpoint()
    if isinstance(response, ListResponse):
        manufacturer_names: List[str] = response.data

    colA, colB = st.columns([.5, .5])
    with colA:
        with st.container(border=True):

            st.header(_("General Information"))

            name = st.text_input(_("Name*"), placeholder=_("Name of the ride"))
            if name in rides_names:
                st.write(_("This attraction name already exists"))

            description = st.text_area(_("Description"), placeholder=_("A short description of the ride"))
            ticket_price = st.number_input(_("Ticket Price"), placeholder=_("Ticket price"))

            image = st.file_uploader(_("An image of the ride"), accept_multiple_files=False,
                                     type=['png', 'jpg', 'jpeg'])


            st.divider()
            st.header(_("Manufacturer Information"))

            manufacturer_col, add_col = st.columns([.9, .1])
            with manufacturer_col:
                manufacturer = st.selectbox(
                    _("Manufacturer"), options=manufacturer_names, index=0, placeholder=_("Manufacturer")
                )
            with add_col:
                st.write("")
                if st.button("", key="add_manufacturer", icon=":material/add:"):
                    add_manufacturer_dialog()

            technical_name = st.text_input(
                _("Technical Name"), placeholder=_("The name given by the manufacturer")
            )
            attraction_type = st.selectbox(
                _("Attraction Type*"), options=list(AttractionType), placeholder=_("the type of the ride")
            )
            manufacturer_page_url = st.text_input(
                _("Manufacturer page"), help=_("A link to the product"),
                placeholder=_("Enter the url page of the manufacturer ride")
            )

            st.divider()
            st.header(_("Owners"))

            owner = st.text_input(
                _("Family owner"), placeholder=_("Name of the family that own the ride")
            )

            st.divider()
            st.header(_("Media"))

            news_page_url = st.text_input(
                _("Official news page of the ride"), placeholder=_("Official news page or fan page"), help=_("Tell us where to find this ride")
            )

            st.session_state.videos_url = list()

            st.write(_("Videos"))
            colC, colD = st.columns([.8, .2])
            with colC:
                video_url = st.text_input(
                    _("Videos url"), placeholder=_("Enter a video URL (e.g., YouTube, MP4 link)"), label_visibility="collapsed"
                )
                log = st.empty()
            with colD:
                if st.button(_("Add Video")):
                    if video_url:
                        st.session_state.videos_url.append(video_url)
                    else:
                        log.warning("Please enter a valid video URL.")

            if st.session_state.videos_url:
                for cursor in range(0, len(st.session_state.videos_url), 3):
                    for i, col in enumerate(st.columns(3)):
                        with col:
                            if cursor+i < len(st.session_state.videos_url):
                                st.video(st.session_state.videos_url[cursor+i])
            else:
                st.info(_("No videos added yet. Add some above!"))

            st.session_state.images_url = list()

            st.write(_("Images"))
            colC, colD = st.columns([.8, .2])
            with colC:
                video_url = st.text_input(
                    _("Immages url"), placeholder=_("Enter a image URL"), label_visibility="collapsed"
                )
                log = st.empty()
            with colD:
                if st.button(_("Add Image")):
                    if video_url:
                        st.session_state.images_url.append(video_url)
                    else:
                        log.warning(_("Please enter a valid video URL."))

            if st.session_state.images_url:
                for cursor in range(0, len(st.session_state.images_url), 3):
                    for i, col in enumerate(st.columns(3)):
                        with col:
                            if cursor + i < len(st.session_state.images_url):
                                st.image(st.session_state.images_url[cursor + i])
            else:
                st.info(_("No Images added yet. Add some above!"))

            st.divider()
            submitted = st.button(_("Submit"))
            if submitted:
                attraction_form: dict = {
                    'name': name, 'description': description,
                    'ticket_price': ticket_price, 'manufacturer': manufacturer,
                    'technical_name': technical_name, 'attraction_type': attraction_type,
                    'manufacturer_page_url': manufacturer_page_url, 'owner': owner,
                    'news_page_url': news_page_url, 'videos_url': st.session_state.videos_url,
                    'images_url': st.session_state.images_url

                }
                response: ResponseDto = create_attraction_endpoint(attraction_form, image)
                if isinstance(response, SuccessResponse):
                    st.success(response.message, icon=":material/check_circle:")
                    st.page_link("pages/ride_list.py", label=_("Check your attractions"), icon=":material/celebration:")
                elif isinstance(response, ErrorResponse):
                    st.error(response.message, icon=":material/close:")
                    st.error(response.errors, icon=":material/close:")

    with colB:
        if image:
            st.image(image.read())


ride_create()
