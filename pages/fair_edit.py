from typing import Dict, List
import streamlit as st
import gettext

from backend.dto.attraction_dto import AttractionImageDTO
from backend.dto.error_dto import ErrorResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.endpoints.attractionsEndpoint import list_attractions_names_and_id_endpoint, \
    get_attraction_image_by_id_endpoint
from backend.endpoints.fairEndpoint import get_fair_detailed_endpoint
from backend.endpoints.fairEndpoint import update_fair_endpoint
from backend.models.fairModel import FairDTO

_ = gettext.gettext

def fair_edit():
    
    response: ResponseDto = get_fair_detailed_endpoint(id=st.session_state.fair_id)
    if isinstance(response, ErrorResponse):
        st.switch_page("pages/fair_list.py")
        
    fair: FairDTO = response.data
        
    attractions_array: Dict[str, List[str]] = {}
    response: ResponseDto = list_attractions_names_and_id_endpoint()
    if isinstance(response, SuccessResponse):
        attractions_array = response.data

    st.title(_("Edit Fair"))

    col1, col2 = st.columns([.5, .5])
    with col1:
        st.header("Information about the fair")
        colA, colB = st.columns([.5, .5])
        with colA:
            name = st.text_input(_("Fair name"), value=fair.name)
        with colB:
            start_date = st.date_input(_("First day of the fair"), value=fair.start_date)
            end_date = st.date_input(_("Last day of the fair"), value=fair.end_date)


        st.divider()
        st.header(_("Location of the fair"))
        colA, colB = st.columns([.5, .5])
        with colA:
            street = st.text_input(_("Street of the fair"), value=fair.location.street)
            area = st.text_input(_("Area of the fair"), value=fair.location.area)
            lat = st.text_input(_("Latitude"), value=fair.location.lat)
            lng = st.text_input(_("Longitude"), value=fair.location.lng)
        with colB:
            city = st.text_input(_("City of the fair"), value=fair.location.city)
            postal_code = st.text_input(_("Postal code of the fair"), value=fair.location.postal_code)
            state = st.text_input(_("State/dpt of the fair"), value=fair.location.state)
            country = st.text_input(_("Country of the fair"), value=fair.location.country)

        st.divider()
        
        selected_attractions_array: List[str] = [
            attractions_array['values'][attractions_array['keys'].index(attraction.id)] for attraction in fair.attractions
        ]
        
        st.header(_("What rides are present in the fair"))
        attractions = st.multiselect(
            _("Select attractions present in the fair"),
            attractions_array['values'],
            selected_attractions_array,
        )
        walk_tour_video = st.text_input(_("Walk tour video url"), value=fair.walk_tour_video)

        st.divider()
        st.header(_("Sources"))
        official_ad_page = st.text_input(_("Official advertissement page url"), value=fair.official_ad_page)
        facebook_event_page = st.text_input(_("facebook event page url"), value=fair.facebook_event_page)
        city_event_page = st.text_input(_("City event page url"), value=fair.city_event_page)


        submitted = st.button(_("Submit"))
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
            response: ResponseDto = update_fair_endpoint(updated_fair_dict=fair_form, id=fair.id)
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


if "fair_id" in st.session_state and st.session_state.fair_id:
    fair_edit()
else:
    st.error("no fair_id")
    st.page_link("pages/fair_list.py")
