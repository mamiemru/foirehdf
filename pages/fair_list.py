import gettext
from typing import List, Dict

import streamlit as st

from backend.dto.error_dto import ErrorResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.endpoints.fairEndpoint import delete_fair_endpoint, list_fair_sort_by_status_endpoint

from backend.models.fairModel import FairDTO, FairStatus

_ = gettext.gettext

@st.dialog("delete fair")
def delete_fair_dialog(fair_dto: FairDTO):
    st.subheader("Delete a Fair")
    st.write(f"Are you sure to delete {fair_dto.name}")
    if st.button("Delete"):
        response: ResponseDto = delete_fair_endpoint(fair_dto.id)
        if isinstance(response, SuccessResponse):
            st.success(response.message, icon=":material/check_circle:")
            st.rerun()
        elif isinstance(response, ErrorResponse):
            st.error(response.message, icon=":material/close:")
            st.error(response.errors, icon=":material/close:")


import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"],
)


def display_fair(fair: FairDTO):
    with st.container(border=True, height=200):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader(fair.name)
        with col2:
            if st.button(_("View fair"), key=f"view_fair_{fair.id}", icon=":material/visibility:", use_container_width=True):
                st.session_state.view_fair_id = fair.id
                st.switch_page("pages/fair_view.py")

        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(":material/location_on: Locations")
            st.caption(
                ", ".join([
                    text for text in
                    [
                        fair.location.street or "", fair.location.area or "", fair.location.city,
                        fair.location.postal_code, fair.location.state, fair.location.country
                    ] if text
                ]
                )
            )
        with col2:
            st.write(":material/calendar_month: Dates")
            st.caption(f"**From** {fair.start_date} **Until** {fair.end_date}")


def fair_list():

    fairs_struct: Dict[str, List[FairDTO]] = {}
    data_map: List[Dict[str, str]] = []
    response: ResponseDto = list_fair_sort_by_status_endpoint()
    if isinstance(response, SuccessResponse):
        fairs_struct = response.data['fairs']
        data_map = response.data['map']

    st.title("Fairs")

    col_search, col_add = st.columns([0.9, 0.1])

    with col_search:
        search_fair = st.text_input("search", label_visibility="collapsed")
        if search_fair:
            st.rerun()

    with col_add:
        if st.button("", icon=":material/add:"):
            st.switch_page("pages/fair_create.py")

    st.header(_(":green[FunFairs currently available today]"))
    colCurrent, colMap = st.columns([.5, .5])
    with colCurrent:
        with st.container(height=500, border=False):
            for fair in fairs_struct[FairStatus.CURRENTLY_AVAILABLE]:
                display_fair(fair)

    with colMap:
        st.map(data=data_map, latitude="lat", longitude="lng", size="size", color="color", zoom=7)

    colComming, colPast = st.columns([.5, .5])
    with colComming:
        st.header(_(":orange[FunFairs coming soon]"))
        for fair in fairs_struct[FairStatus.INCOMING]:
            display_fair(fair)

    with colPast:
        st.header(_(":blue[FunFairs done]"))
        for fair in fairs_struct[FairStatus.DONE]:
            display_fair(fair)

fair_list()