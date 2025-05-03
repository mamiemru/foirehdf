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


        st.markdown(f"**{_('Description')}:** {ride.description}")
        st.markdown(f"**{_('Ticket ')}:** €{ride.ticket_price}")
        st.markdown(f"**{_('Manufacturer')}:** {ride.manufacturer}")
        st.markdown(f"**{_('Technical Name')}:** {ride.technical_name}")
        st.markdown(f"**{_('Attraction Type')}:** {ride.attraction_type}")
        if ride.owner:
            st.markdown(f"**{_('Owner')}:** {ride.owner}")
        if ride.manufacturer_page_url:
            st.markdown(f"**{_('Manufacturer Page')}:** [Link]({ride.manufacturer_page_url})")
        if ride.news_page_url:
            st.markdown(f"**{_('News Page')}:** [Link]({ride.news_page_url})")

    with right_col:
        
        if getattr(st.session_state, 'admin', False):
            if st.button("", key="edit_fair", icon=":material/edit:"):
                st.session_state.ride_id = ride.id
                st.switch_page("pages/ride_edit.py")
    
        for image in ride.images:
            st.image(image.path, use_container_width=True)

    # Divider
    st.markdown("---")

    # Videos Section
    colA, colB = st.columns([.8, .2])
    with colA:
        st.header(_("Videos"))
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


if "ride_id" in st.session_state and st.session_state.ride_id:
    response: ResponseDto = get_attraction_by_id_endpoint(st.session_state.ride_id)
    if isinstance(response, SuccessResponse):
        ride = response.data
        ride_view(ride)
    else:
        st.error(response)
else:
    st.switch_page("pages/ride_list.py")
