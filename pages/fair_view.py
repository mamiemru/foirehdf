
import gettext
import streamlit as st

from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.endpoints.fairEndpoint import get_fair_detailed_endpoint
from backend.models.fairModel import FairDTO
from components.display_attraction_in_list import display_ride_as_item_in_list

_ = gettext.gettext

def fair_view():

    response: ResponseDto = get_fair_detailed_endpoint(id=st.session_state.fair_id)
    if isinstance(response, SuccessResponse):
        fair: FairDTO = response.data

        cola1, cola2 = st.columns([.8, .2])
        with cola1:
            st.title(fair.name)
        with cola2:
            if getattr(st.session_state, 'admin', False):
                if st.button("", key="edit_fair", icon=":material/edit:"):
                    st.session_state.fair_id = fair.id
                    st.switch_page("pages/fair_edit.py")
              
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
                st.write(f"**{_("From")}** {fair.start_date.strftime('%d %B %Y')}")
                st.write(f"**{_("Until")}** {fair.end_date.strftime('%d %B %Y')}")
                st.write(f"**{_("For")}**: {(fair.end_date - fair.start_date).days} days")

                if fair.fair_incoming:
                    st.write(f"{_("Days before the fair")}:  {fair.days_before_start_date} {_("Days")}")

                if fair.fair_available_today:
                    st.write(f"{_("Days left until end")}:  {fair.days_before_end_date} {_("Days")}")

        with col2:
            if fair.official_ad_page:
                st.image(fair.official_ad_page)
            if fair.image:
                st.image(fair.image)

        st.divider()
        st.subheader(f":material/link: {_('Sources and useful links')}")

        markdown_table = f"| {_("Url type")} | {_("Url")} |\n"
        markdown_table += "|------|------|\n"

        if fair.official_ad_page:
            markdown_table += f"| {_("Ad")} | [{fair.official_ad_page}]({fair.official_ad_page}) |\n"
        if fair.city_event_page:
            markdown_table += f"| {_("City page")} | [{fair.city_event_page}]({fair.city_event_page}) |\n"
        if fair.facebook_event_page:
            markdown_table += f"| {_("Facebook page")} | [{fair.facebook_event_page}]({fair.facebook_event_page}) |\n"
        if fair.walk_tour_video:
            markdown_table += f"| {_("Walk tour")} | [{fair.walk_tour_video}]({fair.walk_tour_video}) |\n"

        for url in fair.sources:
            markdown_table += f"| {_("Other")} | [{url}]({url}) |\n"

        st.markdown(markdown_table)

        st.divider()
         
        for attraction in fair.attractions:
            if attraction:
                display_ride_as_item_in_list(_, st, attraction)
    else:
        st.error(response)

if "fair_id" in st.session_state and st.session_state.fair_id:
    fair_view()
else:
    st.error("no fair_id")
    st.page_link("pages/fair_list.py")
