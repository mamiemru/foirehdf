
import streamlit as st
from typing import List

from backend.dto.attraction_dto import AttractionDTO
from backend.services.attractionService import update_attraction
from backend.services.attractionService import list_attractions_names
from backend.services.attractionService import get_attraction_by_id
from backend.services.manufacturerService import create_manufacturer
from backend.services.manufacturerService import list_manufacturers_names

from backend.models.attractionModel import AttractionType

from backend.dto.error_dto import ErrorResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse
from backend.dto.list_dto import ListResponse


class Datas:
    ride: AttractionDTO
    rides_names: List[str]
    manufacturer_names: List[str]
    
    def __init__(self):
        self.ride: AttractionDTO = get_attraction_by_id(st.session_state.ride_id)
        self.rides_names: List[str] = list_attractions_names()
        self.manufacturer_names: List[str] = list_manufacturers_names()


@st.dialog(_("RIDE_ADD_MANUFACTURER"))
def add_manufacturer_dialog():    

    name = st.text_input(_("RIDE_NAME_OF_THE_MANUFACTURER"))
    if st.button(_("SUBMIT")):
        create_manufacturer({"name": name})
        st.rerun()


@st.fragment
def ride_edit():
    st.header(_("RIDE_UPDATE_A_NEW_RIDE"))

    colA, colB = st.columns([.5, .5])
    with colA:
        with st.container(border=True):

            st.header(_("RIDE_GENERAL_INFORMATION"))

            st.session_state.datas.name = st.text_input(f'{_("RIDE_NAME")}*', placeholder=_("RIDE_NAME_OF_THE_RIDE"), value=st.session_state.datas.ride.name)
            st.session_state.datas.description = st.text_area(_("RIDE_DESCRIPTION"), placeholder=_("RIDE_A_SHORT_DESCRIPTION_OF_THE_RIDE"), value=st.session_state.datas.ride.description)
            st.session_state.datas.ticket_price = st.number_input(_("RIDE_TICKET_PRICE"), placeholder=_("RIDE_TICKET_PRICE"), value=st.session_state.datas.ride.ticket_price)

            st.divider()
            st.header(_("RIDE_MANUFACTURER_INFORMATION"))

            manufacturer_col, add_col = st.columns([.9, .1])
            with manufacturer_col:
                st.session_state.datas.manufacturer = st.selectbox(
                    _("RIDE_MANUFACTURER"), options=st.session_state.datas.manufacturer_names, index=st.session_state.datas.manufacturer_names.index(st.session_state.datas.ride.manufacturer)
                )
            with add_col:
                st.write("")
                if st.button("", key="add_manufacturer", icon=":material/add:"):
                    add_manufacturer_dialog()

            st.session_state.datas.technical_name = st.text_input(
                _("RIDE_TECHNICAL_NAME"), placeholder=_("RIDE_THE_NAME_GIVEN_BY_THE_MANUFACTURER"), value=st.session_state.datas.ride.technical_name
            )
            attraction_type_options = list(AttractionType)
            st.session_state.datas.attraction_type = st.selectbox(
                _("RIDE_ATTRACTION_TYPE"), options=attraction_type_options, placeholder=_("RIDE_THE_TYPE_OF_THE_RIDE"), index=attraction_type_options.index(st.session_state.datas.ride.attraction_type)
            )
            st.session_state.datas.manufacturer_page_url = st.text_input(
                _("RIDE_MANUFACTURER_PAGE"), help=_("RIDE_A_LINK_TO_THE_PRODUCT"),
                placeholder=_("RIDE_ENTER_THE_URL_PAGE_OF_THE_MANUFACTURER_RIDE"), value=st.session_state.datas.ride.manufacturer_page_url
            )

            st.divider()
            st.header(_("RIDE_OWNER"))

            st.session_state.datas.owner = st.text_input(
                _("RIDE_FAMILY_OWNER"), placeholder=_("RIDE_NAME_OF_THE_FAMILY_THAT_OWN_THE_RIDE"), value=st.session_state.datas.ride.owner
            )

            st.divider()
            st.header(_("RIDE_MEDIAS"))

            st.session_state.datas.news_page_url = st.text_input(
                _("RIDE_OFFICIAL_NEWS_PAGE_OF_THE_RIDE"), placeholder=_("RIDE_OFFICIAL_NEWS_PAGE_OR_FAN_PAGE"), help=_("RIDE_TELL_US_WHERE_TO_FIND_THIS_RIDE"), value=st.session_state.datas.ride.news_page_url
            )

            with st.container(border=False):
                st.write(_("RIDE_VIDEOS"))
                colC, colD = st.columns([.8, .2])
                with colC:
                    video_url = st.text_input(
                        _("RIDE_VIDEOS_URL"), placeholder=_("RIDE_ENTER_A_VIDEO_URL_E_G_YOUTUBE_MP4_LINK"), label_visibility="collapsed"
                    )
                    log = st.empty()
                with colD:
                    if st.button(_("RIDE_ADD_VIDEO")):
                        if video_url:
                            st.session_state.datas.ride.videos_url.append(video_url)
                        else:
                            log.warning(_("RIDE_PLEASE_ENTER_A_VALID_VIDEO_URL"))

                cols_video, cols_video_del = st.columns([.8, .2])
                if st.session_state.datas.ride.videos_url:
                    for i, video_url in enumerate(st.session_state.datas.ride.videos_url):
                        with cols_video:
                            st.video(video_url)
                        with cols_video_del:
                            if st.button("", key=f"delete_video_{i}", icon=":material/delete:"):
                                st.session_state.datas.ride.videos_url.pop(i)
                else:
                    st.info(_("RIDE_NO_VIDEOS_ADDED_YET_ADD_SOME_ABOVE"))

            with st.container(border=False):
                st.write(_("RIDE_IMAGES"))
                colC, colD = st.columns([.8, .2])
                with colC:
                    image_url = st.text_input(
                        _("RIDE_IMAGES_URL"), placeholder=_("RIDE_ENTER_A_IMAGE_URL"), label_visibility="collapsed"
                    )
                    log = st.empty()
                with colD:
                    if st.button(_("RIDE_ADD_IMAGE")):
                        if image_url:
                            st.session_state.datas.ride.images_url.append(image_url)
                        else:
                            log.warning(_("RIDE_PLEASE_ENTER_A_VALID_IMAGE_URL"))

                cols_image, cols_image_del = st.columns([.8, .2])
                if st.session_state.datas.ride.images_url:
                    for i, image_url in enumerate(st.session_state.datas.ride.images_url):
                        with cols_image:
                            st.image(image_url)
                        with cols_image_del:
                            if st.button("", key=f"delete_image_{i}", icon=":material/delete:"):
                                st.session_state.datas.ride.images_url.pop(i)

            st.divider()
            submitted = st.button(_("SUBMIT"))
            if submitted:
                attraction_form: dict = {
                    'name': st.session_state.datas.name, 'description': st.session_state.datas.description,
                    'ticket_price': st.session_state.datas.ticket_price, 'manufacturer': st.session_state.datas.manufacturer,
                    'technical_name': st.session_state.datas.technical_name, 'attraction_type': st.session_state.datas.attraction_type,
                    'manufacturer_page_url': st.session_state.datas.manufacturer_page_url, 'owner': st.session_state.datas.owner,
                    'news_page_url': st.session_state.datas.news_page_url, 'videos_url': st.session_state.datas.ride.videos_url,
                    'images_url': st.session_state.datas.ride.images_url

                }
                try:
                    update_attraction(id=st.session_state.datas.ride.id, attraction_dict=attraction_form)
                except Exception as e:
                    st.error(e, icon=":material/close:")
                else:
                    st.page_link("pages/ride_list.py", label=_("RIDE_CHECK_YOUR_ATTRACTIONS"), icon=":material/celebration:")

    with colB:
        pass
            
            
            
if "ride_id" in st.session_state and st.session_state.ride_id:
    st.session_state.datas = Datas()
    ride_edit()
else:
    st.error("no ride_id")
    st.page_link("pages/ride_list.py")


