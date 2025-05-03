
import streamlit as st

from backend.endpoints.attractionsEndpoint import list_attractions_endpoint

from backend.dto.error_dto import ErrorResponse
from backend.dto.paginated_list_dto import PaginatedResponse
from backend.dto.response_dto import ResponseDto
from components.display_attraction_in_list import display_ride_as_item_in_list


def ride_list():
    col_search, col_add = st.columns([0.9, 0.1])

    with col_search:
        search_fair = st.text_input(_("search"), key="search", label_visibility="collapsed")
        if search_fair:
            st.rerun()

    with col_add:
        if getattr(st.session_state, 'admin', False):
            if st.button("", icon=":material/add:"):
                st.switch_page("pages/ride_create.py")

    response: ResponseDto = list_attractions_endpoint()
    if isinstance(response, PaginatedResponse):
        rides = response.data
        rides.reverse()

        for attraction in rides:
            display_ride_as_item_in_list(_, st, attraction)

    elif isinstance(response, ErrorResponse):
        st.error(f"{response.message}\n \n {'\n - '.join([f'**{k}**: {v}' for k,v in response.errors.items()])})", icon=":material/close:")

ride_list()