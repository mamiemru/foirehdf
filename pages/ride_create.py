
import streamlit as st
from typing import List

from backend.endpoints.attractionsEndpoint import create_attraction_endpoint
from backend.endpoints.attractionsEndpoint import list_attractions_names_endpoint
from backend.endpoints.manufacturerEndpoint import list_manufacturer_names_endpoint
from backend.endpoints.manufacturerEndpoint import create_manufacturer_endpoint

from backend.models.attractionModel import AttractionType

from backend.dto.error_dto import ErrorResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse
from backend.dto.list_dto import ListResponse
from pages.form_input import DotDict


class Datas:
    ride: DotDict
    
    def __init__(self):
        self.ride = DotDict()
        self.ride.videos_url = []
        self.ride.images_url = []
        self.location = DotDict()

@st.dialog(_("add manufacturer"))
def add_manufacturer_dialog():    

    name = st.text_input(_("Name of the manufacturer*"))
    if st.button(_("submit")):
        response: ResponseDto = create_manufacturer_endpoint({"name": name})
        if isinstance(response, SuccessResponse):
            st.success(response.message, icon=":material/check_circle:")
            st.rerun()
        elif isinstance(response, ErrorResponse):
            st.error(f"{response.message}\n \n {'\n - '.join([f'**{k}**: {v}' for k,v in response.errors.items()])})", icon=":material/close:")


@st.fragment
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

            st.session_state.datas.ride.name = st.text_input(_("Name*"), placeholder=_("Name of the ride"))
            if st.session_state.datas.ride.name in rides_names:
                st.write(_("This attraction name already exists"))

            st.session_state.datas.ride.description = st.text_area(_("Description"), placeholder=_("A short description of the ride"))
            st.session_state.datas.ride.ticket_price = st.number_input(_("Ticket Price"), placeholder=_("Ticket price"))

            st.divider()
            st.header(_("Manufacturer Information"))

            manufacturer_col, add_col = st.columns([.9, .1])
            with manufacturer_col:
                st.session_state.datas.ride.manufacturer = st.selectbox(
                    _("Manufacturer"), options=manufacturer_names, index=0, placeholder=_("Manufacturer")
                )
            with add_col:
                st.write("")
                if st.button("", key="add_manufacturer", icon=":material/add:"):
                    add_manufacturer_dialog()

            st.session_state.datas.ride.technical_name = st.text_input(
                _("Technical Name"), placeholder=_("The name given by the manufacturer")
            )
            st.session_state.datas.ride.attraction_type = st.selectbox(
                _("Attraction Type*"), options=list(AttractionType), placeholder=_("the type of the ride")
            )
            st.session_state.datas.ride.manufacturer_page_url = st.text_input(
                _("Manufacturer page"), help=_("A link to the product"),
                placeholder=_("Enter the url page of the manufacturer ride")
            )

            st.divider()
            st.header(_("Owners"))

            st.session_state.datas.ride.owner = st.text_input(
                _("Family owner"), placeholder=_("Name of the family that own the ride")
            )

            st.divider()
            st.header(_("Media"))

            st.session_state.datas.ride.news_page_url = st.text_input(
                _("Official news page of the ride"), placeholder=_("Official news page or fan page"), help=_("Tell us where to find this ride")
            )

            with st.container(border=False):
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
                            st.session_state.datas.ride.videos_url.append(video_url)
                        else:
                            log.warning("Please enter a valid video URL.")

                cols_video, cols_video_del = st.columns([.8, .2])
                if st.session_state.datas.ride.videos_url:
                    for i, video_url in enumerate(st.session_state.datas.ride.videos_url):
                        with cols_video:
                            st.video(video_url)
                        with cols_video_del:
                            if st.button("", key=f"delete_video_{i}", icon=":material/delete:"):
                                st.session_state.datas.ride.videos_url.pop(i)
                else:
                    st.info(_("No videos added yet. Add some above!"))

            with st.container(border=False):
                st.write(_("Images"))
                colC, colD = st.columns([.8, .2])
                with colC:
                    image_url = st.text_input(
                        _("Immages url"), placeholder=_("Enter a image URL"), label_visibility="collapsed"
                    )
                    log = st.empty()
                with colD:
                    if st.button(_("Add Image")):
                        if image_url:
                            st.session_state.datas.ride.images_url.append(image_url)
                        else:
                            log.warning(_("Please enter a valid video URL."))

                cols_image, cols_image_del = st.columns([.8, .2])
                if st.session_state.datas.ride.images_url:
                    for i, image_url in enumerate(st.session_state.datas.ride.images_url):
                        with cols_image:
                            st.image(image_url)
                        with cols_image_del:
                            if st.button("", key=f"delete_image_{i}", icon=":material/delete:"):
                                st.session_state.datas.ride.images_url.pop(i)


            st.divider()
            submitted = st.button(_("Submit"))
            if submitted:
                attraction_form: dict = {
                    'name': st.session_state.datas.ride.name, 'description': st.session_state.datas.ride.description,
                    'ticket_price': st.session_state.datas.ride.ticket_price, 'manufacturer': st.session_state.datas.ride.manufacturer,
                    'technical_name': st.session_state.datas.ride.technical_name, 'attraction_type': st.session_state.datas.ride.attraction_type,
                    'manufacturer_page_url': st.session_state.datas.ride.manufacturer_page_url or None, 'owner': st.session_state.datas.ride.owner,
                    'news_page_url': st.session_state.datas.ride.news_page_url or None, 'videos_url': st.session_state.datas.ride.videos_url,
                    'images_url': st.session_state.datas.ride.images_url
                }
                response: ResponseDto = create_attraction_endpoint(attraction_form, None)
                if isinstance(response, SuccessResponse):
                    st.success(response.message, icon=":material/check_circle:")
                    st.page_link("pages/ride_list.py", label=_("Check your attractions"), icon=":material/celebration:")
                elif isinstance(response, ErrorResponse):
                    st.error(f"{response.message}\n \n {'\n - '.join([f'**{k}**: {v}' for k,v in response.errors.items()])})", icon=":material/close:")

    with colB:
        pass


st.session_state.datas = Datas()
ride_create()
