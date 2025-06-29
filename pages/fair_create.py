from typing import Dict, List
import streamlit as st

from backend.services.attractionService import list_attractions_names_and_id
from backend.services.fairService import create_fair, create_hidden_fair
from backend.services.locationService import list_locations

from backend.models.locationModel import LocationDTO

st.session_state.add_location = False

@st.fragment()
def fair_create():
    
    attractions_array: Dict[str, List[str]] = list_attractions_names_and_id()
    locations: List[LocationDTO] = list_locations()
    
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
                st.session_state.add_location = False
                
        with colLocA:
            if st.button(f"{_("FAIR_CREATE_LOCATION")}"):
                st.session_state.add_location = True
        
        if st.session_state.add_location:
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
            st.session_state.fair['attractions'] = [attractions_array['keys'][attractions_array['values'].index(x)] for x in st.session_state.fair['attractions']]
            try:
                if hidden_fair:
                    create_hidden_fair(st.session_state.fair)
                else:
                    create_fair(st.session_state.fair)
            except Exception as e:
                st.error(e.message, icon=":material/close:")
            else:
                st.success("fair added", icon=":material/check_circle:")
                st.rerun()

    with col2:
        pass

fair_create()
