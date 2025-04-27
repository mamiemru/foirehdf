import gettext

import gettext
import streamlit as st

from backend.dto.attraction_dto import AttractionDTO
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.endpoints.attractionsEndpoint import get_attraction_by_id_endpoint

_ = gettext.gettext

def ride_view(ride: AttractionDTO):

    left_col, right_col = st.columns([.7, .3])

    with left_col:

        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:15px; margin-bottom:10px;">
                <h2 style="margin:0; font-size:48px; color:#FF8B17;">{ride.name}</h2>
            </div>
            """, unsafe_allow_html=True
        )


        st.markdown(f"**Description:** {ride.description}")
        st.markdown(f"**Ticket Price:** €{ride.ticket_price}")
        st.markdown(f"**Manufacturer:** {ride.manufacturer}")
        st.markdown(f"**Technical Name:** {ride.technical_name}")
        st.markdown(f"**Attraction Type:** {ride.attraction_type}")
        if ride.owner:
            st.markdown(f"**Owner:** {ride.owner}")
        if ride.manufacturer_page_url:
            st.markdown(f"**Manufacturer Page:** [Link]({ride.manufacturer_page_url})")
        if ride.news_page_url:
            st.markdown(f"**News Page:** [Link]({ride.news_page_url})")

    with right_col:
        for image in ride.images:
            st.image(image.path, use_container_width=True)

    # Divider
    st.markdown("---")

    # Videos Section
    colA, colB = st.columns([.8, .2])
    with colA:
        st.header("Videos")
    with colB:
        n_split = st.number_input(
            _("Show videos per rows of"), help=_("Show videos per rows of"), min_value=1, max_value=5, value=3
        )
    if ride.videos_url:
        for cursor in range(0, len(ride.videos_url), n_split):
            for i, col in enumerate(st.columns(n_split)):
                with col:
                    if cursor+i < len(ride.videos_url):
                        st.video(ride.videos_url[cursor+i])


if "view_ride_id" in st.session_state and st.session_state.view_ride_id:
    response: ResponseDto = get_attraction_by_id_endpoint(st.session_state.view_ride_id)
    if isinstance(response, SuccessResponse):
        ride = response.data
        ride_view(ride)
    else:
        st.error(response)
else:
    st.switch_page("pages/ride_list.py")
