

from typing import List
import streamlit as st

from backend.dto.attraction_dto import AttractionDTO
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.endpoints.attractionsEndpoint import get_attraction_by_id_endpoint
from backend.endpoints.fairEndpoint import list_fairs_containing_ride_id_endpoint


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

        st.markdown(f"**{_('RIDE_DESCRIPTION')}:** {ride.description}")
        st.markdown(f"**{_('RIDE_TICKET_PRICE')}:** €{ride.ticket_price}")
        st.markdown(f"**{_('RIDE_MANUFACTURER')}:** {ride.manufacturer}")
        st.markdown(f"**{_('RIDE_TECHNICAL_NAME')}:** {ride.technical_name}")
        st.markdown(f"**{_('RIDE_ATTRACTION_TYPE')}:** {ride.attraction_type}")
        if ride.owner:
            st.markdown(f"**{_('RIDE_OWNER')}:** {ride.owner}")
        if ride.manufacturer_page_url:
            st.markdown(f"**{_('RIDE_MANUFACTURER_PAGE')}:** [Link]({ride.manufacturer_page_url})")
        if ride.news_page_url:
            st.markdown(f"**{_('RIDE_NEWS_PAGE')}:** [Link]({ride.news_page_url})")

    with right_col:
        if getattr(st.session_state, 'admin', False):
            if st.button("", key="edit_fair", icon=":material/edit:"):
                st.session_state.ride_id = ride.id
                st.switch_page("pages/ride_edit.py")
    
        for image in ride.images:
            st.image(image.path, use_container_width=True)

    st.divider()
    
    st.header(_("RIDE_WAS_INSTALLED_IN_FAIRS"))
    fairs_table = st.columns([.25, .35, .25, .10])
    for col, head in zip(fairs_table, [_("FAIR_NAME"), _("FAIR_LOCATION"), _("FAIR_DATES")]):
        with col:
            st.write(head)
    for fair in list_fairs_containing_ride_id_endpoint(st.session_state.ride_id).data:
        with fairs_table[0]:
            st.write(fair.name)
        with fairs_table[1]:
            st.caption(
                ", ".join([
                    text for text in
                    [
                        fair.location.street or "", fair.location.area or "", fair.location.city,
                        fair.location.postal_code, fair.location.state, fair.location.country
                    ] if text
                ])
            )
        with fairs_table[2]:
            date_str: List[str] = [
                f"**{_("FAIR_FROM_DATE")}**: {fair.start_date.strftime('%d %B %Y')}", 
                f"**{_("FAIR_UNTIL_DATE")}**: {fair.end_date.strftime('%d %B %Y')}"
            ]
            st.caption(",".join(date_str))
        st.empty()
        
    st.divider()

    colA, colB = st.columns([.8, .2])
    with colA:
        st.header(_("RIDE_LIST_OF_VIDEOS"))
    with colB:
        n_split = st.number_input(
            _("SHOW_VIDEOS_PER_ROWS_OF"), min_value=1, max_value=5, value=3
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
