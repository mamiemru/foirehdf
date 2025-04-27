
import gettext
import streamlit as st

from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.endpoints.fairEndpoint import get_fair_detailed_endpoint
from backend.models.fairModel import FairDTO
from components.display_attraction_in_list import display_ride_as_item_in_list

_ = gettext.gettext

def fair_view():

    response: ResponseDto = get_fair_detailed_endpoint(st.session_state.view_fair_id)
    if isinstance(response, SuccessResponse):
        fair: FairDTO = response.data

        st.title(fair.name)
        col1, col2 = st.columns([2, 1])
        with col1:
            cola, colb = st.columns([2, 1])
            with cola:
                st.header(":material/location_on: Locations")
                st.write(
                    ", ".join([
                        text for text in
                        [
                            fair.location.street or "", fair.location.area or "", fair.location.city,
                            fair.location.postal_code, fair.location.state, fair.location.country
                        ] if text
                    ]
                    )
                )
                if fair.location.lat and fair.location.lng:
                    st.map(
                        data=[{'lat': fair.location.lat, 'lng': fair.location.lng}], height=250,
                        latitude="lat", longitude="lng", size=15, color='#ffff00', zoom=8
                    )
            with colb:
                st.header(":material/calendar_month: "+ _("Dates"))
                st.write(f"**From** {fair.start_date} **Until** {fair.end_date}")

        with col2:
            if fair.image:
                st.image(fair.image)
            else:
                st.image("backend\\images\\placeholder.png", caption="Fair Screenshot Placeholder")

        st.divider()
        st.subheader(_("Sources and useful links"))
        for source in fair.sources:
            st.write(source)

        st.divider()
        st.subheader(_("Attractions"))
        for attraction in fair.attractions:
            if attraction:
                display_ride_as_item_in_list(_, st, attraction)


if "view_fair_id" in st.session_state and st.session_state.view_fair_id:
    fair_view()
