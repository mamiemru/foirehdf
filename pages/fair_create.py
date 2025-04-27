from typing import Dict, List
import streamlit as st
import gettext

from backend.dto.attraction_dto import AttractionImageDTO
from backend.dto.error_dto import ErrorResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.endpoints.attractionsEndpoint import list_attractions_names_and_id_endpoint, \
    get_attraction_image_by_id_endpoint

from backend.endpoints.fairEndpoint import create_fair_endpoint

_ = gettext.gettext

def fait_create():
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
            start_date = st.date_input(_("First day of the fair"))
            end_date = st.date_input(_("Last day of the fair"))


        st.divider()
        st.header("Location of the fair")
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
        st.header("What rides is present in the fair")
        attractions = st.multiselect(
            "Select attractions present in the fair",
            attractions_array['values'],
            [],
        )

        submitted = st.button("Submit")
        if submitted:
            attractions = [ attractions_array['keys'][attractions_array['values'].index(x)] for x in attractions]
            fair_form: dict = {
                'name': name, 'start_date': start_date, 'end_date': end_date, 'attractions': attractions,
                'location': {
                    'street': street, 'area': area, 'city': city, 'postal_code': postal_code,
                    'state': state, 'country': country, 'lat': lat, 'lng': lng
                }
            }
            response: ResponseDto = create_fair_endpoint(fair_form)
            if isinstance(response, SuccessResponse):
                st.success(response.message, icon=":material/check_circle:")
                st.rerun()
            elif isinstance(response, ErrorResponse):
                st.error(response.message, icon=":material/close:")
                st.error(response.errors, icon=":material/close:")

    with col2:
        for attraction_id in [attractions_array['keys'][attractions_array['values'].index(x)] for x in attractions]:
            response: ResponseDto = get_attraction_image_by_id_endpoint(attraction_id)
            if isinstance(response, SuccessResponse):
                image: AttractionImageDTO = response.data
                st.image(image.path, width=100)

fait_create()
