from datetime import datetime
from typing import List, Dict
from dateutil.relativedelta import relativedelta

import altair as alt
import streamlit as st

from backend.services.fairService import list_fair_locations
from backend.services.fairService import delete_fair
from backend.services.fairService import list_fair_sort_by_status
from backend.models.fairModel import FairStatus
from backend.dto.fair_dto import FairDTO
from pages.form_input import DotDict


@st.dialog("delete fair")
def delete_fair_dialog(fair_dto: FairDTO):
    st.subheader(_("FAIR_DELETE_A_FAIR"))
    st.write(f"{_('FAIR_ARE_YOU_SURE_TO_DELETE')} {fair_dto.name}")
    if st.button(_("DELETE")):
        delete_fair(fair_dto.id)
        st.rerun()

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
            if fair.days_before_end_date:
                date_str.append(f"**{_("FAIR_DAYS_LEFT_UNTIL_END")}**: {fair.days_before_end_date} {_("DAYS")}")
            else:
                date_str.append(f"**{_("FAIR_LAST_DAY")}**")
            
        st.caption(", ".join(date_str))


@st.fragment
def fair_list():

    gantt_chart_pd = None
    data_map: List[Dict[str, str]] = []
    fairs_struct: Dict[str, List[FairDTO]] = {}
    fairs_by_status = list_fair_sort_by_status(search_fair_query=st.session_state.search_fair_query)
    fairs_struct = fairs_by_status['fairs']
    data_map = fairs_by_status['map']
    gantt_chart_pd = fairs_by_status['gantt']

        
    cities: List[Dict[str, str]] = list_fair_locations()
    colTitle, colAdd = st.columns([.8, .2])
    with colTitle:
        st.title(_("FAIRS_LIST"))
    with colAdd:
        if getattr(st.session_state, 'admin', False):
            if st.button("", icon=":material/add:"):
                st.switch_page("pages/fair_create.py")

    with st.expander(_("FAIR_SEARCH_TITLE"), expanded=False, icon=":material/search:"):
        
        st.session_state.search_fair_query.cities = st.multiselect(
            _("FAIR_SEARCH_BY_CITY"), options=cities, default=st.session_state.search_fair_query.cities or None,
            format_func=lambda c: c['value']
        )
        colDmin, colDmax = st.columns([.5, .5])
        with colDmin:
            st.session_state.search_fair_query.date_min = st.date_input(_("FAIR_SEARCH_BY_MIN_DATE"), value=st.session_state.search_fair_query.date_min or None)
        with colDmax:
            st.session_state.search_fair_query.date_max = st.date_input( _("FAIR_SEARCH_BY_MAX_DATE"), value=st.session_state.search_fair_query.date_max or None)
        
        colApply, colCancel = st.columns([.5, .5])
        with colApply:
            if st.button(_("FAIR_SEARCH_BUTTON"), type="primary", use_container_width=True):
                st.rerun(scope="fragment")
        with colCancel:
            if st.button(_("FAIR_SEARCH_BUTTON_RESET"), use_container_width=True):
                st.session_state.search_fair_query.clear()
                st.rerun(scope="fragment")
    
    if data_map:
        with st.container(border=True):
            chart = alt.Chart(gantt_chart_pd).mark_bar().encode(
                x=alt.X('start', title=_("FAIR_DATES")),      
                x2=alt.X2('finish'),
                y=alt.Y('task', title=_("CITY")),
                color=alt.Color('color', scale=None),
                tooltip=[
                    {"field": "name", "title": _("FAIR_TITLE")},
                    {"field": "start_date", "title": _("FAIR_FROM_DATE")},
                    {"field": "end_date", "title": _("FAIR_UNTIL_DATE")},
                    {"field": "date", "title": _("FAIR_DAYS_BEFORE_THE_FAIR")}
                ]
            )

            st.altair_chart(chart, use_container_width=True)

        st.header(f":green[{_('FAIR_LIST_FUNFAIRS_CURRENTLY_AVAILABLE_TODAY')}]")
        colCurrent, colMap = st.columns([.5, .5])
        with colCurrent:
            with st.container(height=500, border=False):
                if fairs_struct[FairStatus.CURRENTLY_AVAILABLE]:
                    for fair in fairs_struct[FairStatus.CURRENTLY_AVAILABLE]:
                        display_fair(fair)
                else:
                    st.write(_("FAIR_NO_FAIRS_CURRENTLY_AVAILABLE"))
        
        with colMap:
            st.map(data=data_map, latitude="lat", longitude="lng", size="size", color="color", zoom=7)

        colComming, colPast = st.columns([.5, .5])
        with colComming:
            st.header(f":orange[{_('FAIR_LIST_FUNFAIRS_COMING_SOON')}]")
            if fairs_struct[FairStatus.INCOMING]:
                for fair in sorted(fairs_struct[FairStatus.INCOMING], key=lambda f: f.start_date):
                    display_fair(fair)
            else:
                st.write(_("FAIR_NO_FAIRS_COMMING_SOON"))

        with colPast:
            st.header(f":blue[{_('FAIR_LIST_FUNFAIRS_DONE')}]")
            if fairs_struct[FairStatus.DONE]:
                for fair in fairs_struct[FairStatus.DONE]:
                    display_fair(fair)
            else:
                st.write(_("FAIR_NO_FAIRS_DONE"))
    else:
        if st.session_state.search_fair_query:
            st.header(_("FAIR_NO_FAIRS_TO_DISPLAY_BY_SEARCH"))
        else:
            st.header(_("FAIR_NO_FAIRS_TO_DISPLAY"))

st.session_state.search_fair_query = DotDict()
st.session_state.search_fair_query.date_min = (datetime.now() - relativedelta(months=2)).date()
fair_list()
