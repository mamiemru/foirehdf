

import streamlit as st

from backend.models.ride_model import Ride
from backend.services.fair_service import list_fairs_containing_ride_id
from backend.services.ride_service import get_ride_by_id
from components.image_loader import fetch_cached_image
from pages.const import _


def ride_view(ride: Ride):

    left_col, right_col = st.columns([.7, .3])

    with left_col:

        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:15px; margin-bottom:10px;">
                <h2 style="margin:0; font-size:48px; color:#FF8B17;">{ride.name}</h2>
            </div>
            """, unsafe_allow_html=True,
        )

        if ride.description:
            st.markdown(ride.description)

        st.markdown(f"**{_('RIDE_TICKET_PRICE')}:** €{ride.ticket_price}")
        st.markdown(f"**{_('RIDE_MANUFACTURER')}:** {ride.manufacturer}")
        st.markdown(f"**{_('RIDE_TECHNICAL_NAME')}:** {ride.technical_name}")
        st.markdown(f"**{_('RIDE_ATTRACTION_TYPE')}:** {ride.ride_type}")
        if ride.owner:
            st.markdown(f"**{_('RIDE_OWNER')}:** {ride.owner}")
        if ride.manufacturer_page_url:
            st.markdown(f"**{_('RIDE_MANUFACTURER_PAGE')}:** [Link]({ride.manufacturer_page_url})")
        if ride.news_page_url:
            st.markdown(f"**{_('RIDE_NEWS_PAGE')}:** [Link]({ride.news_page_url})")

    with right_col:
        if getattr(st.session_state, "admin", False):
            if st.button("", key="edit_fair", icon=":material/edit:"):
                st.session_state.ride_id = ride.id
                st.switch_page("pages/ride_edit.py")

        if ride.images_url:
            image = fetch_cached_image(ride.images_url[0])
            if image:
                st.image(image, use_container_width=True)

    st.divider()

    st.header(_("RIDE_WAS_INSTALLED_IN_FAIRS"))
    for fair in list_fairs_containing_ride_id(st.session_state.ride_id):
        location: str = ", ".join([
            text for text in
            [
                fair.locations[0].street or "", fair.locations[0].area or "", fair.locations[0].city,
                fair.locations[0].postal_code, fair.locations[0].state,
            ] if text
        ])
        dates: str = ",".join([
            f"**{_("FAIR_FROM_DATE")}**: {fair.start_date.strftime('%d %B %Y')}",
            f"**{_("FAIR_UNTIL_DATE")}**: {fair.end_date.strftime('%d %B %Y')}",
        ])
        st.write(f"{fair.name} {location} {dates}")


    st.divider()

    colA, colB = st.columns([.8, .2])
    with colA:
        st.header(_("RIDE_LIST_OF_VIDEOS"))
    with colB:
        n_split = st.number_input(
            _("SHOW_VIDEOS_PER_ROWS_OF"), min_value=1, max_value=5, value=3,
        )
    if ride.videos_url:
        for cursor in range(0, len(ride.videos_url), n_split):
            for i, col in enumerate(st.columns(n_split)):
                with col:
                    if cursor+i < len(ride.videos_url):
                        st.video(str(ride.videos_url[cursor+i]))

    st.divider()
    colA, colB = st.columns([.8, .2])
    with colA:
        st.header(_("RIDE_LIST_OF_IMAGES"))
    with colB:
        nn_split = st.number_input(
            _("SHOW_IMAGES_PER_ROWS_OF"), min_value=1, max_value=5, value=3,
        )
    if ride.images_url:
        for cursor in range(0, len(ride.images_url), nn_split):
            for i, col in enumerate(st.columns(nn_split)):
                with col:
                    if cursor+i < len(ride.images_url):
                        image = fetch_cached_image(ride.images_url[cursor+i])
                        if image:
                            st.image(image)


if "ride_id" in st.session_state and st.session_state.ride_id:
    ride = get_ride_by_id(st.session_state.ride_id)
    ride_view(ride)
else:
    st.switch_page("pages/ride_list.py")
