
import streamlit as st

from backend.models.fairModel import Fair
from backend.services.attractionService import (
    get_attraction_by_id,
    list_attractions_names_and_id,
)
from backend.services.fair_service import get_fair, update_fair


def fair_edit() -> None:

    fair: Fair = get_fair(fair_id=st.session_state.fair_id)
    attractions_array: dict[str, list[str]] = list_attractions_names_and_id()

    st.title(_("FAIR_EDIT_FAIR"))

    col1, col2 = st.columns([.5, .5])
    with col1:
        st.header(_("FAIR_INFORMATION"))
        colA, colB = st.columns([.5, .5])
        with colA:
            name = st.text_input(_("FAIR_NAME"), value=fair.name)
        with colB:
            start_date = st.date_input(_("FAIR_START_DATE"), value=fair.start_date)
            end_date = st.date_input(_("FAIR_END_DATE"), value=fair.end_date)


        st.divider()
        st.header(_("LOCATION"))
        for location in fair.locations:
            st.write(location)

        st.divider()


        selected_attractions_array: list[str] = []
        for attraction_id in fair.attractions:
            attraction = get_attraction_by_id(attraction_id=attraction_id)
            for array in attractions_array:
                if str(array["key"]) == str(attraction.id):
                    selected_attractions_array.append(array)
                    continue

        st.header(_("FAIR_RIDES_IN_THE_FAIR"))
        attractions = st.multiselect(
            _("FAIR_SELECT_RIDE_MESSAGE"),
            format_func=lambda a: a["value"],
            options=attractions_array,
            default=selected_attractions_array,
        )
        walk_tour_video = st.text_input(_("FAIR_WALKTOUR_VIDEO"), value=fair.walk_tour_video)

        st.divider()
        st.header(_("FAIR_SOURCES"))
        official_ad_page = st.text_input(_("FAIR_AD_URL"), value=fair.official_ad_page)
        facebook_event_page = st.text_input(_("FAIR_FACEBOOK_EVENT_PAGE_URL"), value=fair.facebook_event_page)
        city_event_page = st.text_input(_("FAIR_CITY_PAGE"), value=fair.city_event_page)


        submitted = st.button(_("SUBMIT"))
        if submitted:
            fair_form: dict = {
                "name": name, "start_date": start_date, "end_date": end_date, "attractions": [a["key"] for a in attractions],
                "locations": fair.locations,
                "walk_tour_video": walk_tour_video or None, "official_ad_page": official_ad_page or None,
                "facebook_event_page": facebook_event_page or None, "city_event_page": city_event_page or None,
            }
            try:
                update_fair(updated_fair_dict=fair_form, id=fair.id)
            except Exception as e:
                st.error(e, icon=":material/close:")
            else:
                st.success("fair edited", icon=":material/check_circle:")
                st.rerun()

    with col2:
        pass


if "fair_id" in st.session_state and st.session_state.fair_id:
    fair_edit()
else:
    st.error("no fair_id")
    st.page_link("pages/fair_list.py")
