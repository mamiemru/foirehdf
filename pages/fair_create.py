from typing import Dict, List
import streamlit as st

from backend.dto.attraction_dto import AttractionImageDTO
from backend.dto.error_dto import ErrorResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.endpoints.attractionsEndpoint import list_attractions_names_and_id_endpoint
from backend.endpoints.attractionsEndpoint import get_attraction_image_by_id_endpoint

from backend.endpoints.fairEndpoint import create_fair_endpoint

def fair_create():
    
    attractions_array: Dict[str, List[str]] = {}
    response: ResponseDto = list_attractions_names_and_id_endpoint()
    if isinstance(response, SuccessResponse):
        attractions_array = response.data


    st.title(_("FAIR_CREATE_FAIR"))

    col1, col2 = st.columns([.5, .5])
    with col1:
        st.header(_("FAIR_INFORMATION"))
        colA, colB = st.columns([.5, .5])
        with colA:
            name = st.text_input(_("FAIR_NAME"))
        with colB:
            start_date = st.date_input(_("FAIR_START_DATE"), value=None)
            end_date = st.date_input(_("FAIR_END_DATE"), value=None)

        st.divider()
        st.header(_("FAIR_LOCATION"))
        colA, colB = st.columns([.5, .5])
        with colA:
            street = st.text_input(_("STREET"))
            area = st.text_input(_("AREA"))
            lat = st.text_input(_("LATITUDE"))
            lng = st.text_input(_("LONGITUDE"))
        with colB:
            city = st.text_input(_("CITY"))
            postal_code = st.text_input(_("POSTAL_CODE"))
            state = st.text_input(_("STATE"))
            country = st.text_input(_("COUNTRY"))

        st.divider()
        st.header(_("FAIR_RIDES_IN_THE_FAIR"))
        attractions = st.multiselect(
            _("FAIR_SELECT_RIDE_MESSAGE"),
            attractions_array['values'],
            [],
        )
        walk_tour_video = st.text_input(_("FAIR_WALKTOUR_VIDEO"))

        st.divider()
        st.header(_("FAIR_SOURCES"))
        official_ad_page = st.text_input(_("FAIR_CREATE_AD_URL"))
        facebook_event_page = st.text_input(_("FAIR_FACEBOOK_EVENT_PAGE_URL"))
        city_event_page = st.text_input(_("FAIR_CITY_PAGE"))


        submitted = st.button(_("SUBMIT"))
        if submitted:
            attractions = [ attractions_array['keys'][attractions_array['values'].index(x)] for x in attractions]
            fair_form: dict = {
                'name': name, 'start_date': start_date, 'end_date': end_date, 'attractions': attractions,
                'location': {
                    'street': street, 'area': area, 'city': city, 'postal_code': postal_code,
                    'state': state, 'country': country, 'lat': lat, 'lng': lng
                },
                'walk_tour_video': walk_tour_video, 'official_ad_page': official_ad_page,
                'facebook_event_page': facebook_event_page, 'city_event_page': city_event_page
            }
            response: ResponseDto = create_fair_endpoint(fair_form)
            if isinstance(response, SuccessResponse):
                st.success(response.message, icon=":material/check_circle:")
                st.rerun()
            elif isinstance(response, ErrorResponse):
                    st.error(f"{response.message}\n \n - {'\n - '.join([f'**{k}**: {v}' for k,v in response.errors.items()])})", icon=":material/close:")

    with col2:
        for attraction_id in [attractions_array['keys'][attractions_array['values'].index(x)] for x in attractions]:
            response: ResponseDto = get_attraction_image_by_id_endpoint(attraction_id)
            if isinstance(response, SuccessResponse):
                image: AttractionImageDTO = response.data
                if image:
                    st.image(image.path, width=100)

fair_create()
