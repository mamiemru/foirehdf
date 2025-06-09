from typing import Dict, List
import streamlit as st

from backend.dto.attraction_dto import AttractionImageDTO

from backend.services.attractionService import list_attractions_names_and_id
from backend.services.attractionService import list_attraction_images_to_dto
from backend.services.fairService import get_fair_detailed
from backend.services.fairService import update_fair
from backend.dto.fair_dto import FairDTO


def fair_edit():
    
    fair: FairDTO = get_fair_detailed(id=st.session_state.fair_id)
    attractions_array: Dict[str, List[str]] = list_attractions_names_and_id()

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
        colA, colB = st.columns([.5, .5])
        with colA:
            street = st.text_input(_("STREET"), value=fair.location.street)
            area = st.text_input(_("AREA"), value=fair.location.area)
            lat = st.text_input(_("LATITUDE"), value=fair.location.lat)
            lng = st.text_input(_("LONGITUDE"), value=fair.location.lng)
        with colB:
            city = st.text_input(_("CITY"), value=fair.location.city)
            postal_code = st.text_input(_("POSTAL_CODE"), value=fair.location.postal_code)
            state = st.text_input(_("STATE"), value=fair.location.state)
            country = st.text_input(_("COUNTRY"), value=fair.location.country)

        st.divider()
        
        selected_attractions_array: List[str] = [
            attractions_array['values'][attractions_array['keys'].index(attraction.id)] for attraction in fair.attractions
        ]
        
        st.header(_("FAIR_RIDES_IN_THE_FAIR"))
        attractions = st.multiselect(
            _("FAIR_SELECT_RIDE_MESSAGE"),
            attractions_array['values'],
            selected_attractions_array,
        )
        walk_tour_video = st.text_input(_("FAIR_WALKTOUR_VIDEO"), value=fair.walk_tour_video)

        st.divider()
        st.header(_("FAIR_SOURCES"))
        official_ad_page = st.text_input(_("FAIR_AD_URL"), value=fair.official_ad_page)
        facebook_event_page = st.text_input(_("FAIR_FACEBOOK_EVENT_PAGE_URL"), value=fair.facebook_event_page)
        city_event_page = st.text_input(_("FAIR_CITY_PAGE"), value=fair.city_event_page)


        submitted = st.button(_("SUBMIT"))
        if submitted:
            attractions = [ attractions_array['keys'][attractions_array['values'].index(x)] for x in attractions]
            fair_form: dict = {
                'name': name, 'start_date': start_date, 'end_date': end_date, 'attractions': attractions,
                'location': {
                    'street': street, 'area': area, 'city': city, 'postal_code': postal_code,
                    'state': state, 'country': country, 'lat': lat, 'lng': lng, 'id': fair.location.id
                },
                'walk_tour_video': walk_tour_video, 'official_ad_page': official_ad_page,
                'facebook_event_page': facebook_event_page, 'city_event_page': city_event_page
            }
            try:
                update_fair(updated_fair_dict=fair_form, id=fair.id)
            except Exception as e:
                st.error(e, icon=":material/close:")
            else:
                st.success("fair edited", icon=":material/check_circle:")
                st.rerun()

    with col2:
        for attraction_id in [attractions_array['keys'][attractions_array['values'].index(x)] for x in attractions]:
            image: AttractionImageDTO = list_attraction_images_to_dto(attraction_id=attraction_id)
            if image:
                st.image(image.path, width=100)


if "fair_id" in st.session_state and st.session_state.fair_id:
    fair_edit()
else:
    st.error("no fair_id")
    st.page_link("pages/fair_list.py")
