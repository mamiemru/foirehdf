

import streamlit as st

from backend.models.manufacturer_model import Manufacturer
from backend.models.ride_model import RideType
from backend.services.manufacturer_service import list_manufacturers
from backend.services.ride_service import list_rides
from components.display_ride_in_list import display_ride_as_item_in_list
from pages.const import _
from pages.form_input import DotDict


@st.fragment
def ride_list() -> None:
    """List and display selected rides."""
    manufacturer_names: list[Manufacturer] = list_manufacturers()
    st.session_state.search_ride_query = DotDict()

    col_title, col_add = st.columns([.8, .2])
    with col_title:
        st.title(_("RIDES_LIST"))
    with col_add:
        if getattr(st.session_state, "admin", False) and st.button("", icon=":material/add:"):
                st.switch_page("pages/ride_create.py")

    with st.expander(_("RIDES_SEARCH_TITLE"), expanded=False, icon=":material/search:"):

        st.session_state.search_ride_query.ride_type = st.multiselect(
            _("RIDES_SEARCH_BY_ATTRACTION_TYPE"), options=[a.value for a in RideType], default=st.session_state.search_ride_query.ride_type or [],
        )

        st.session_state.search_ride_query.manufacturers = st.multiselect(
            _("RIDES_SEARCH_BY_MANUFACTURER"), options=manufacturer_names, default=st.session_state.search_ride_query.manufacturers or [],
            format_func=lambda m: m.name,
        )

        col_apply, col_cancel = st.columns([.5, .5])
        with col_apply:
            if st.button(_("RIDES_SEARCH_BUTTON"), type="primary", use_container_width=True):
                st.rerun(scope="fragment")
        with col_cancel:
            if st.button(_("RIDES_SEARCH_BUTTON_RESET"), use_container_width=True):
                st.session_state.search_ride_query.clear()
                st.rerun(scope="fragment")


    rides = list_rides(search_ride_query=st.session_state.search_ride_query)
    if rides:
        rides.reverse()
        for ride in rides:
            display_ride_as_item_in_list(_, st, ride)

    elif st.session_state.search_ride_query:
        st.header(_("RIDES_NO_RIDES_TO_DISPLAY_BY_SEARCH"))
    else:
        st.header(_("RIDES_NO_RIDES_TO_DISPLAY"))

st.session_state.search_ride_query = DotDict()

ride_list()
