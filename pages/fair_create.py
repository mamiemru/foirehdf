from typing import Dict, List
import streamlit as st

from backend.dto.attraction_dto import AttractionImageDTO
from backend.dto.error_dto import ErrorResponse
from backend.dto.list_dto import ListResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.endpoints.attractionsEndpoint import list_attractions_names_and_id_endpoint
from backend.endpoints.attractionsEndpoint import get_attraction_image_by_id_endpoint

from backend.endpoints.fairEndpoint import create_fair_endpoint
from backend.endpoints.locationEndpoint import list_locations_endpoint
from backend.models.locationModel import LocationDTO

def fair_create():
    
    attractions_array: Dict[str, List[str]] = {}
    response: ResponseDto = list_attractions_names_and_id_endpoint()
    if isinstance(response, SuccessResponse):
        attractions_array = response.data

    locations: List[LocationDTO] = list()
    response: ResponseDto = list_locations_endpoint()
    if isinstance(response, ListResponse):
        locations = response.data
    
    st.session_state.fair = dict()

    st.title(_("FAIR_CREATE_FAIR"))

    col1, col2 = st.columns([.5, .5])
    with col1:
        st.header(_("FAIR_INFORMATION"))
        colA, colB = st.columns([.5, .5])
        with colA:
            st.session_state.fair['name'] = st.text_input(f'{_("FAIR_NAME")}*')
        with colB:
            st.session_state.fair['start_date'] = st.date_input(f'{_("FAIR_START_DATE")}*', value=None)
            st.session_state.fair['end_date'] = st.date_input(f'{_("FAIR_END_DATE")}*', value=None)

        st.divider()
        st.header(_("FAIR_LOCATION"))
        st.session_state.fair['location'] = dict()
        st.session_state.fair['location_id'] = None
        
        colLocS, colLocA = st.columns([ .7, .3])
        with colLocS:
            ids: List[str] = list()
            options: List[str] = list()
            for location_dto in locations:
                ids.append(location_dto.id)
                options.append(", ".join([text for text in[
                    location_dto.street or "", location_dto.area or "", location_dto.city,location_dto.postal_code, location_dto.state, location_dto.country
                ] if text]))
            
            selected_location = st.selectbox(f"{_("FAIR_LOCATION_ID")}", options=options)
            if selected_location:
                st.session_state.fair['location_id'] = ids[options.index(selected_location)]
                st.session_state.fair['location'].clear()
                
        with colLocA:
            if st.button(f"{_("FAIR_CREATE_LOCATION")}"):
                st.session_state.fair['location_id'] = None
        
        if st.session_state.fair.get('location_id', True) is None:
            colA, colB = st.columns([.5, .5])
            with colA:
                st.session_state.fair['location']['street'] = st.text_input(_("STREET"))
                st.session_state.fair['location']['area'] = st.text_input(_("AREA"))
                st.session_state.fair['location']['lat'] = st.text_input(f'{_("LATITUDE")}*')
                st.session_state.fair['location']['lng'] = st.text_input(f'{_("LONGITUDE")}*')
            with colB:
                st.session_state.fair['location']['city'] = st.text_input(f'{_("CITY")}*')
                st.session_state.fair['location']['postal_code  '] = st.text_input(f'{_("POSTAL_CODE")}*')
                st.session_state.fair['location']['state'] = st.text_input(f'{_("STATE")}*')
                st.session_state.fair['location']['country'] = st.text_input(f'{_("COUNTRY")}*', value="France")

        st.divider()
        st.header(f'{_("FAIR_RIDES_IN_THE_FAIR")}*')
        st.session_state.fair['attractions'] = st.multiselect(
            _("FAIR_SELECT_RIDE_MESSAGE"),
            attractions_array['values'],
            [],
        )
        st.session_state.fair['walk_tour_video'] = st.text_input(_("FAIR_WALKTOUR_VIDEO"))

        st.divider()
        st.header(_("FAIR_SOURCES"))
        st.session_state.fair['official_ad_page'] = st.text_input(_("FAIR_AD_URL"))
        st.session_state.fair['facebook_event_page'] = st.text_input(_("FAIR_FACEBOOK_EVENT_PAGE_URL"))
        st.session_state.fair['city_event_page'] = st.text_input(_("FAIR_CITY_PAGE"))
        
        hidden_fair = st.toggle(_("FAIR_HIDE"), help=_("FAIR_HIDE_TOOLTIP"), value=False)

        submitted = st.button(_("SUBMIT"))
        if submitted:
            st.session_state.fair['attractions'] = [ attractions_array['keys'][attractions_array['values'].index(x)] for x in st.session_state.fair['attractions']]
            response: ResponseDto = create_fair_endpoint(st.session_state.fair , hidden_fair)
            if isinstance(response, SuccessResponse):
                st.success(response.message, icon=":material/check_circle:")
                st.rerun()
            elif isinstance(response, ErrorResponse):
                    st.error(f"{response.message}\n \n - {'\n - '.join([f'**{k}**: {v}' for k,v in response.errors.items()])})", icon=":material/close:")

    with col2:
        for attraction_id in [attractions_array['keys'][attractions_array['values'].index(x)] for x in st.session_state.fair['attractions']]:
            response: ResponseDto = get_attraction_image_by_id_endpoint(attraction_id)
            if isinstance(response, SuccessResponse):
                image: AttractionImageDTO = response.data
                if image:
                    st.image(image.path, width=100)

fair_create()
