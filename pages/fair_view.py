

import streamlit as st
from pydantic import HttpUrl

from backend.models.fair_model import Fair
from backend.models.location_model import LocationBase
from backend.services.fair_service import get_fair
from backend.services.ride_service import get_ride_by_id
from components.display_ride_in_list import display_ride_as_item_in_list
from components.image_loader import fetch_cached_image
from pages.const import _


def get_markdown_link_table_row(td: str, url: HttpUrl) -> str:
    """Return a markdown ready table row with url."""
    return f"| {_(td)} | [{url}]({url}) |\n"


def get_markdown_link_tale(fair: Fair) -> str:
    """Return a markdown ready table with all urls."""
    markdown_table = f"| {_('FAIR_URL_TYPE')} | {_('FAIR_URL')} |\n"
    markdown_table += "|------|------|\n"

    if fair.official_ad_page:
        markdown_table += get_markdown_link_table_row(td="FAIR_AD_URL", url=fair.official_ad_page)
    if fair.city_event_page:
        markdown_table += get_markdown_link_table_row(td="FAIR_CITY_PAGE", url=fair.city_event_page)
    if fair.facebook_event_page:
        markdown_table += get_markdown_link_table_row(td="FAIR_FACEBOOK_EVENT_PAGE_URL", url=fair.facebook_event_page)
    if fair.walk_tour_video:
        markdown_table += get_markdown_link_table_row(td="FAIR_WALKTOUR_VIDEO", url=fair.walk_tour_video)

    for url in fair.sources:
        markdown_table += get_markdown_link_table_row(td="FAIR_VIEW_OTHER", url=url)
    return markdown_table


def location_to_str(location: LocationBase) -> str:
    """Turn a location into string."""
    return ", ".join([text for text in[
        location.street or "", location.area or "", location.city,
        location.postal_code, location.state, location.country,
    ] if text])


def fair_view() -> None:
    """Display a fair with details."""
    fair: Fair = get_fair(fair_id=st.session_state.fair_id)

    cola1, cola2 = st.columns([.8, .2])
    with cola1:
        st.title(fair.name)
    with cola2:
        if getattr(st.session_state, "admin", False) and st.button("", key="edit_fair", icon=":material/edit:"):
            st.session_state.fair_id = fair.id
            st.switch_page("pages/fair_edit.py")

    col1, col2 = st.columns([2, 1])
    with col1:
        cola, colb = st.columns([2, 1])
        with cola:
            st.header(f":material/location_on: {_('LOCATIONS')}")
            location = fair.locations[0]
            st.write(location_to_str(location=location))
            if location.lat and location.lng:
                st.map(
                    data=[{"lat": location.lat, "lng": location.lng}], height=250,
                    latitude="lat", longitude="lng", size=15, color="#ffff00", zoom=8,
                )
        with colb:
            st.header(":material/calendar_month: "+ _("DATES"))
            st.write(f"**{_("FAIR_FROM_DATE")}** {fair.start_date.strftime('%d %B %Y')}")
            st.write(f"**{_("FAIR_UNTIL_DATE")}** {fair.end_date.strftime('%d %B %Y')}")
            st.write(f"**{_("FAIR_FOR_DATE")}**: {(fair.end_date - fair.start_date).days} {_('DAYS')}")

            if fair.fair_incoming:
                st.write(f"**{_("FAIR_DAYS_BEFORE_THE_FAIR")}**:  {fair.days_before_start_date} {_("DAYS")}")

            if fair.fair_available_today:
                if fair.days_before_end_date:
                    st.write(f"**{_("FAIR_FOR_DATE")}**: {fair.days_before_end_date} {_("DAYS")}")
                else:
                    st.write(f"**{_("FAIR_LAST_DAY")}**")


    with col2:
        if fair.official_ad_page:
            banner = fetch_cached_image(fair.official_ad_page)
            if banner:
                st.image(banner)
        for image in fair.images:
            img = fetch_cached_image(image)
            if img:
                st.image(img)

    st.divider()
    st.subheader(f":material/link: {_('FAIR_VIEW_SOURCES_AND_USEFUL_LINKS')}")
    st.markdown(get_markdown_link_tale(fair=fair))

    st.divider()

    for ride_id in fair.rides:
        ride = get_ride_by_id(ride_id=ride_id)
        if ride:
            display_ride_as_item_in_list(_, st, ride)


if "fair_id" in st.session_state and st.session_state.fair_id:
    fair_view()
else:
    st.error("no fair_id")
    st.page_link("pages/fair_list.py")
