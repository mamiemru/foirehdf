

import streamlit as st

from backend.models.ride_model import RideType
from backend.services.manufacturer_service import (
    create_manufacturer,
    list_manufacturers_names,
)
from backend.services.ride_service import create_ride, list_rides_names
from pages.const import _
from pages.form_input import DotDict


class Datas:
    ride: DotDict

    def __init__(self) -> None:
        self.ride = DotDict()
        self.ride.videos_url = []
        self.ride.images_url = []
        self.location = DotDict()


@st.dialog(_("RIDE_ADD_MANUFACTURER"))
def add_manufacturer_dialog() -> None:
    """Open a dialog to create a new manufacturer."""
    name = st.text_input(_("RIDE_NAME_OF_THE_MANUFACTURER"))
    if st.button(_("RIDE_SUBMIT")):
        create_manufacturer({"name": name})
        st.rerun()


@st.fragment
def ride_create() -> None:
    st.header(_("RIDE_ADD_A_NEW_RIDE"))

    rides_names: list[str] = list_rides_names()
    manufacturer_names: list[str] = list_manufacturers_names()

    colA, colB = st.columns([.5, .5])
    with colA:
        with st.container(border=True):

            st.header(_("RIDE_GENERAL_INFORMATION"))

            st.session_state.datas.ride.name = st.text_input(f"{_('RIDE_NAME')}*", placeholder=_("RIDE_NAME_OF_THE_RIDE"))
            if st.session_state.datas.ride.name in rides_names:
                st.write(_("RIDE_THIS_ATTRACTION_NAME_ALREADY_EXISTS"))

            st.session_state.datas.ride.description = st.text_area(_("RIDE_DESCRIPTION"), placeholder=_("RIDE_A_SHORT_DESCRIPTION_OF_THE_RIDE"))
            st.session_state.datas.ride.ticket_price = st.number_input(_("RIDE_TICKET_PRICE"), placeholder=_("RIDE_TICKET_PRICE"))

            st.divider()
            st.header(_("RIDE_MANUFACTURER_INFORMATION"))


            manufacturer_col, add_col = st.columns([.9, .1])
            with manufacturer_col:
                st.session_state.datas.ride.manufacturer = st.selectbox(
                    _("RIDE_MANUFACTURER"), options=manufacturer_names, index=0, placeholder=_("RIDE_MANUFACTURER"),
                )
            with add_col:
                st.write("")
                if st.button("", key="add_manufacturer", icon=":material/add:"):
                    add_manufacturer_dialog()

            st.session_state.datas.ride.technical_name = st.text_input(
                _("RIDE_TECHNICAL_NAME"), placeholder=_("RIDE_THE_NAME_GIVEN_BY_THE_MANUFACTURER"), value=st.session_state.datas.ride.technical_name,
            )
            st.session_state.datas.ride.ride_type = st.selectbox(
                _("RIDE_ATTRACTION_TYPE"), options=list(RideType), placeholder=_("RIDE_THE_TYPE_OF_THE_RIDE"),
                format_func=lambda a: a.value, index=st.session_state.ride_type_index,
            )
            st.session_state.datas.ride.manufacturer_page_url = st.text_input(
                _("RIDE_MANUFACTURER_PAGE"), help=_("RIDE_A_LINK_TO_THE_PRODUCT"),
                placeholder=_("RIDE_ENTER_THE_URL_PAGE_OF_THE_MANUFACTURER_RIDE"),
                value=st.session_state.datas.ride.manufacturer_page_url,
            )

            st.divider()
            st.header(_("RIDE_OWNER"))

            st.session_state.datas.ride.owner = st.text_input(
                _("RIDE_FAMILY_OWNER"), placeholder=_("RIDE_NAME_OF_THE_FAMILY_THAT_OWN_THE_RIDE"),
            )

            st.divider()
            st.header(_("RIDE_MEDIAS"))

            st.session_state.datas.ride.news_page_url = st.text_input(
                _("RIDE_OFFICIAL_NEWS_PAGE_OF_THE_RIDE"), placeholder=_("RIDE_OFFICIAL_NEWS_PAGE_OR_FAN_PAGE"), help=_("RIDE_TELL_US_WHERE_TO_FIND_THIS_RIDE"),
            )

            with st.container(border=False):
                st.write(_("RIDE_VIDEOS"))
                colC, colD = st.columns([.8, .2])
                with colC:
                    video_url = st.text_input(
                        _("RIDE_VIDEOS_URL"), placeholder=_("RIDE_ENTER_A_VIDEO_URL_E_G_YOUTUBE_MP4_LINK"), label_visibility="collapsed",
                    )
                    log = st.empty()
                with colD:
                    if st.button(_("RIDE_ADD_VIDEO")):
                        if video_url:
                            st.session_state.datas.ride.videos_url.append(video_url)
                        else:
                            log.warning(_("RIDE_ERROR_VIDEO_URL"))

                cols_video, cols_video_del = st.columns([.8, .2])
                if st.session_state.datas.ride.videos_url:
                    for i, video_url in enumerate(st.session_state.datas.ride.videos_url):
                        with cols_video:
                            st.video(video_url)
                        with cols_video_del:
                            if st.button("", key=f"delete_video_{i}", icon=":material/delete:"):
                                st.session_state.datas.ride.videos_url.pop(i)
                else:
                    st.info(_("RIDE_PLEASE_ENTER_A_VALID_VIDEO_URL"))

            with st.container(border=False):
                st.write(_("RIDE_IMAGES"))
                colC, colD = st.columns([.8, .2])
                with colC:
                    image_url = st.text_input(
                        _("RIDE_IMAGES_URL"), placeholder=_("RIDE_ENTER_A_IMAGE_URL"), label_visibility="collapsed",
                    )
                    log = st.empty()
                with colD:
                    if st.button(_("RIDE_ADD_IMAGE")):
                        if image_url:
                            st.session_state.datas.ride.images_url.append(image_url)
                        else:
                            log.warning(_("RIDE_PLEASE_ENTER_A_VALID_VIDEO_URL"))

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
                ride_form: dict = {
                    "name": st.session_state.datas.ride.name, "description": st.session_state.datas.ride.description,
                    "ticket_price": st.session_state.datas.ride.ticket_price, "manufacturer": st.session_state.datas.ride.manufacturer,
                    "technical_name": st.session_state.datas.ride.technical_name, "ride_type": st.session_state.datas.ride.ride_type,
                    "manufacturer_page_url": st.session_state.datas.ride.manufacturer_page_url or None, "owner": st.session_state.datas.ride.owner,
                    "news_page_url": st.session_state.datas.ride.news_page_url or None, "videos_url": st.session_state.datas.ride.videos_url,
                    "images_url": st.session_state.datas.ride.images_url,
                }
                try:
                    create_ride(ride_form)
                except Exception as e:
                    st.error(e, icon=":material/close:")
                else:
                    st.page_link("pages/ride_list.py", label=_("RIDE_CHECK_YOUR_ATTRACTIONS"), icon=":material/celebration:")

    with colB:
        pass


st.session_state.datas = Datas()
st.session_state.ride_type_index = None
ride_create()
