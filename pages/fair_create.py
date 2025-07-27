
import streamlit as st

from backend.models.location_model import Location
from backend.services.fair_service import create_fair, create_hidden_fair
from backend.services.location_service import list_locations
from backend.services.ride_service import list_rides_names_and_id
from pages.const import _


@st.fragment()
def fair_create() -> None:
    """Wizard to create a fair."""
    rides_array: list[dict[str, str]] = list_rides_names_and_id()
    locations: list[Location] = list_locations()

    st.session_state.fair = {}

    st.title(_("FAIR_CREATE_FAIR"))

    col1, col2 = st.columns([.5, .5])
    with col1:
        st.header(_("FAIR_INFORMATION"))
        st.session_state.fair["name"] = st.text_input(f'{_("FAIR_NAME")}*')
        col_fair_dates_start, col_fair_dates_end = st.columns([.5, .5])
        with col_fair_dates_start:
            st.session_state.fair["start_date"] = st.date_input(f'{_("FAIR_START_DATE")}*', value=None)
        with col_fair_dates_end:
            st.session_state.fair["end_date"] = st.date_input(f'{_("FAIR_END_DATE")}*', value=None)

        st.divider()
        st.header(_("FAIR_LOCATION"))
        st.session_state.fair["locations"] = []


        selected_locations = st.multiselect(f"{_("FAIR_LOCATION_ID")}", options=locations, format_func=lambda l: str(l))
        if selected_locations:
            st.session_state.fair["locations"] = selected_locations


        st.divider()
        st.header(f'{_("FAIR_RIDES_IN_THE_FAIR")}*')
        st.session_state.fair["rides"] = st.multiselect(
            _("FAIR_SELECT_RIDE_MESSAGE"),
            options=rides_array,
            format_func=lambda a: a["value"],
        )
        st.session_state.fair["walk_tour_video"] = st.text_input(_("FAIR_WALKTOUR_VIDEO"))

        st.divider()
        st.header(_("FAIR_SOURCES"))
        st.session_state.fair["official_ad_page"] = st.text_input(_("FAIR_AD_URL"))
        st.session_state.fair["facebook_event_page"] = st.text_input(_("FAIR_FACEBOOK_EVENT_PAGE_URL"))
        st.session_state.fair["city_event_page"] = st.text_input(_("FAIR_CITY_PAGE"))

        hidden_fair = st.toggle(_("FAIR_HIDE"), help=_("FAIR_HIDE_TOOLTIP"), value=False)

        submitted = st.button(_("SUBMIT"))
        if submitted:
            st.session_state.fair["rides"] = [x["key"] for x in st.session_state.fair["rides"]]
            for url in ["walk_tour_video", "official_ad_page", "facebook_event_page", "city_event_page"]:
                if not st.session_state.fair[url]:
                    st.session_state.fair[url] = None

            try:
                if hidden_fair:
                    create_hidden_fair(st.session_state.fair)
                else:
                    create_fair(st.session_state.fair)
            except Exception as e:
                st.error(e, icon=":material/close:")
            else:
                st.success("fair added", icon=":material/check_circle:")
                st.rerun()

fair_create()
