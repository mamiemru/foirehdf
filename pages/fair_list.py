
from typing import List, Dict

import altair as alt
import streamlit as st

from backend.dto.error_dto import ErrorResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.endpoints.fairEndpoint import delete_fair_endpoint, list_fair_for_gantt_chart_endpoint
from backend.endpoints.fairEndpoint import list_fair_sort_by_status_endpoint

from backend.models.fairModel import FairDTO, FairStatus


@st.dialog("delete fair")
def delete_fair_dialog(fair_dto: FairDTO):
    st.subheader(_("FAIR_DELETE_A_FAIR"))
    st.write(f"{_('FAIR_ARE_YOU_SURE_TO_DELETE')} {fair_dto.name}")
    if st.button(_("DELETE")):
        response: ResponseDto = delete_fair_endpoint(fair_dto.id)
        if isinstance(response, SuccessResponse):
            st.success(response.message, icon=":material/check_circle:")
            st.rerun()
        elif isinstance(response, ErrorResponse):
            st.error(f"{response.message}\n \n - {'\n - '.join([f'**{k}**: {v}' for k,v in response.errors.items()])})", icon=":material/close:")


def display_fair(fair: FairDTO):
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader(fair.name)
        with col2:
            if st.button(_("FAIR_VIEW_FAIR"), key=f"view_fair_{fair.id}", icon=":material/visibility:", use_container_width=True):
                st.session_state.fair_id = fair.id
                st.switch_page("pages/fair_view.py")


        st.write(f":material/location_on: {_('LOCATIONS')}")
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
        st.write(f":material/calendar_month: {_("DATES")}")
        date_str: List[str] = [
            f"**{_("FAIR_FROM_DATE")}**: {fair.start_date.strftime('%d %B %Y')}", 
            f"**{_("FAIR_UNTIL_DATE")}**: {fair.end_date.strftime('%d %B %Y')}",
            f"**{_("FAIR_FOR_DATE")}**: {(fair.end_date - fair.start_date).days} {_("DAYS")}"
        ]

        if fair.fair_incoming:
            date_str.append(f"**{_("FAIR_DAYS_BEFORE_THE_FAIR")}**:  {fair.days_before_start_date} {_("DAYS")}")

        elif fair.fair_available_today:
            date_str.append(f"**{_("FAIR_DAYS_LEFT_UNTIL_END")}**:  {fair.days_before_end_date} {_("DAYS")}")
            
        st.caption(", ".join(date_str))


def fair_list():

    fairs_struct: Dict[str, List[FairDTO]] = {}
    data_map: List[Dict[str, str]] = []
    response: ResponseDto = list_fair_sort_by_status_endpoint()
    if isinstance(response, SuccessResponse):
        fairs_struct = response.data['fairs']
        data_map = response.data['map']
        
    gantt_chart_pd = None
    response: ResponseDto = list_fair_for_gantt_chart_endpoint()
    if isinstance(response, SuccessResponse):
        gantt_chart_pd = response.data

    st.title(_("FAIRS_LIST"))

    col_search, col_add = st.columns([0.9, 0.1])

    with col_search:
        search_fair = st.text_input(_("FAIR_SEARCH"), label_visibility="collapsed")
        if search_fair:
            st.rerun()

    with col_add:
        if getattr(st.session_state, 'admin', False):
            if st.button("", icon=":material/add:"):
                st.switch_page("pages/fair_create.py")
                
    chart = alt.Chart(gantt_chart_pd).mark_bar().encode(
        x="Start",
        x2="Finish",
        y="Task",
        color="Color",
        tooltip=["Description", "Completion"]
    )

    st.altair_chart(chart, use_container_width=True)

    st.header(f":green[{_('FAIR_LIST_FUNFAIRS_CURRENTLY_AVAILABLE_TODAY')}]")
    colCurrent, colMap = st.columns([.5, .5])
    with colCurrent:
        with st.container(height=500, border=False):
            for fair in fairs_struct[FairStatus.CURRENTLY_AVAILABLE]:
                display_fair(fair)

    with colMap:
        st.map(data=data_map, latitude="lat", longitude="lng", size="size", color="color", zoom=7)

    colComming, colPast = st.columns([.5, .5])
    with colComming:
        st.header(f":orange[{_('FAIR_LIST_FUNFAIRS_COMING_SOON')}]")
        for fair in fairs_struct[FairStatus.INCOMING]:
            display_fair(fair)

    with colPast:
        st.header(f":blue[{_('FAIR_LIST_FUNFAIRS_DONE')}]")
        for fair in fairs_struct[FairStatus.DONE]:
            display_fair(fair)

fair_list()