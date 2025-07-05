
import streamlit as st

from backend.models.location_model import Location
from backend.services.attractionService import list_attractions_names_and_id
from backend.services.fair_service import create_fair, create_hidden_fair
from backend.services.locationService import list_locations


@st.fragment()
def fair_create():

    attractions_array: list[dict[str, str]] = list_attractions_names_and_id()
    locations: list[Location] = list_locations()

    st.session_state.fair = dict()

    st.title(_("FAIR_CREATE_FAIR"))

    col1, col2 = st.columns([.5, .5])
    with col1:
        st.header(_("FAIR_INFORMATION"))
        colA, colB = st.columns([.5, .5])
        with colA:
            st.session_state.fair["name"] = st.text_input(f'{_("FAIR_NAME")}*')
        with colB:
            st.session_state.fair["start_date"] = st.date_input(f'{_("FAIR_START_DATE")}*', value=None)
            st.session_state.fair["end_date"] = st.date_input(f'{_("FAIR_END_DATE")}*', value=None)

        st.divider()
        st.header(_("FAIR_LOCATION"))
        st.session_state.fair["locations"] = list()


        selected_locations = st.multiselect(f"{_("FAIR_LOCATION_ID")}", options=locations, format_func=lambda l: str(l))
        if selected_locations:
            st.session_state.fair["locations"] = selected_locations


        st.divider()
        st.header(f'{_("FAIR_RIDES_IN_THE_FAIR")}*')
        st.session_state.fair["attractions"] = st.multiselect(
            _("FAIR_SELECT_RIDE_MESSAGE"),
            options=attractions_array,
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
            st.session_state.fair["attractions"] = [x["key"] for x in st.session_state.fair["attractions"]]
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

    with col2:
        pass

fair_create()
