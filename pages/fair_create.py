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


    st.title(_("Create Fair"))

    col1, col2 = st.columns([.5, .5])
    with col1:
        st.header("Information about the fair")
        colA, colB = st.columns([.5, .5])
        with colA:
            name = st.text_input(_("Fair name"))
        with colB:
            start_date = st.date_input(_("First day of the fair"), value=None)
            end_date = st.date_input(_("Last day of the fair"), value=None)

        st.divider()
        st.header(_("Location of the fair"))
        colA, colB = st.columns([.5, .5])
        with colA:
            street = st.text_input(_("Street of the fair"))
            area = st.text_input(_("Area of the fair"))
            lat = st.text_input(_("Latitude"))
            lng = st.text_input(_("Longitude"))
        with colB:
            city = st.text_input(_("City of the fair"))
            postal_code = st.text_input(_("Postal code of the fair"))
            state = st.text_input(_("State/dpt of the fair"))
            country = st.text_input(_("Country of the fair"))

        st.divider()
        st.header(_("What rides are present in the fair"))
        attractions = st.multiselect(
            _("Select attractions present in the fair"),
            attractions_array['values'],
            [],
        )
        walk_tour_video = st.text_input(_("Walk tour video url"))

        st.divider()
        st.header(_("Sources"))
        official_ad_page = st.text_input(_("Official advertissement page url"))
        facebook_event_page = st.text_input(_("facebook event page url"))
        city_event_page = st.text_input(_("City event page url"))


        submitted = st.button(_("Submit"))
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
                    st.error(f"{response.message}\n \n {'\n - '.join([f'**{k}**: {v}' for k,v in response.errors.items()])})", icon=":material/close:")

    with col2:
        for attraction_id in [attractions_array['keys'][attractions_array['values'].index(x)] for x in attractions]:
            response: ResponseDto = get_attraction_image_by_id_endpoint(attraction_id)
            if isinstance(response, SuccessResponse):
                image: AttractionImageDTO = response.data
                if image:
                    st.image(image.path, width=100)

fair_create()
