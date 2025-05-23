
from typing import List
import streamlit as st

from backend.dto.list_dto import ListResponse
from backend.dto.manufacturer_dto import ManufacturerDto
from backend.endpoints.attractionsEndpoint import list_attractions_endpoint

from backend.dto.error_dto import ErrorResponse
from backend.dto.paginated_list_dto import PaginatedResponse
from backend.dto.response_dto import ResponseDto
from backend.endpoints.manufacturerEndpoint import list_manufacturer_endpoint
from backend.models.attractionModel import AttractionType
from components.display_attraction_in_list import display_ride_as_item_in_list
from pages.form_input import DotDict

@st.fragment
def ride_list():
    
    manufacturer_names: List[ManufacturerDto] = list()
    response: ResponseDto = list_manufacturer_endpoint()
    if isinstance(response, ListResponse):
        manufacturer_names = response.data

    colTitle, colAdd = st.columns([.8, .2])
    with colTitle:
        st.title(_("RIDES_LIST"))
    with colAdd:
        if getattr(st.session_state, 'admin', False):
            if st.button("", icon=":material/add:"):
                st.switch_page("pages/ride_create.py")

    with st.expander(_("RIDES_SEARCH_TITLE"), expanded=False, icon=":material/search:"):
        
        st.session_state.search_ride_query.attraction_type = st.multiselect(
            _("RIDES_SEARCH_BY_ATTRACTION_TYPE"), options=[a.value for a in AttractionType], default=st.session_state.search_ride_query.attraction_type or []
        )
        
        st.session_state.search_ride_query.manufacturers = st.multiselect(
            _("RIDES_SEARCH_BY_MANUFACTURER"), options=manufacturer_names, default=st.session_state.search_ride_query.manufacturers or [],
            format_func=lambda m: m.name
        )
        
        colApply, colCancel = st.columns([.5, .5])
        with colApply:
            if st.button(_("RIDES_SEARCH_BUTTON"), type="primary", use_container_width=True):
                st.rerun(scope="fragment")
        with colCancel:
            if st.button(_("RIDES_SEARCH_BUTTON_RESET"), use_container_width=True):
                st.session_state.search_ride_query.clear()
                st.rerun(scope="fragment")
    

    response: ResponseDto = list_attractions_endpoint(search_ride_query=st.session_state.search_ride_query)
    if isinstance(response, PaginatedResponse):
        rides = response.data

        if rides:
            rides.reverse()
            for attraction in rides:
                display_ride_as_item_in_list(_, st, attraction)
        else:
            if st.session_state.search_rides_query:
                st.header(_("RIDES_NO_RIDES_TO_DISPLAY_BY_SEARCH"))
            else:
                st.header(_("RIDES_NO_RIDES_TO_DISPLAY"))
                
    elif isinstance(response, ErrorResponse):
        st.error(response, icon=":material/close:")

st.session_state.search_ride_query = DotDict()

ride_list()