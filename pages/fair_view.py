

import streamlit as st

from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.endpoints.fairEndpoint import get_fair_detailed_endpoint
from components.display_attraction_in_list import display_ride_as_item_in_list

from backend.models.fairModel import FairDTO

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
                st.header(f":material/location_on: {_('LOCATIONS')}")
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
                st.header(":material/calendar_month: "+ _("DATES"))
                st.write(f"**{_("FAIR_FROM_DATE")}** {fair.start_date.strftime('%d %B %Y')}")
                st.write(f"**{_("FAIR_UNTIL_DATE")}** {fair.end_date.strftime('%d %B %Y')}")
                st.write(f"**{_("FAIR_FOR_DATE")}**: {(fair.end_date - fair.start_date).days} {_('DAYS')}")

                if fair.fair_incoming:
                    st.write(f"**{_("FAIR_DAYS_BEFORE_THE_FAIR")}**:  {fair.days_before_start_date} {_("DAYS")}")

                if fair.fair_available_today:
                    st.write(f"**{_("FAIR_DAYS_LEFT_UNTIL_END")}**:  {fair.days_before_end_date} {_("DAYS")}")

        with col2:
            if fair.official_ad_page:
                st.image(fair.official_ad_page)
            if fair.image:
                st.image(fair.image)

        st.divider()
        st.subheader(f":material/link: {_('FAIR_VIEW_SOURCES_AND_USEFUL_LINKS')}")

        markdown_table = f"| {_("FAIR_URL_TYPE")} | {_("FAIR_URL")} |\n"
        markdown_table += "|------|------|\n"

        if fair.official_ad_page:
            markdown_table += f"| {_("FAIR_AD_URL")} | [{fair.official_ad_page}]({fair.official_ad_page}) |\n"
        if fair.city_event_page:
            markdown_table += f"| {_("FAIR_CITY_PAGE")} | [{fair.city_event_page}]({fair.city_event_page}) |\n"
        if fair.facebook_event_page:
            markdown_table += f"| {_("FAIR_FACEBOOK_EVENT_PAGE_URL")} | [{fair.facebook_event_page}]({fair.facebook_event_page}) |\n"
        if fair.walk_tour_video:
            markdown_table += f"| {_("FAIR_WALKTOUR_VIDEO")} | [{fair.walk_tour_video}]({fair.walk_tour_video}) |\n"

        for url in fair.sources:
            markdown_table += f"| {_("FAIR_VIEW_OTHER")} | [{url}]({url}) |\n"

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
