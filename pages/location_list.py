
import streamlit as st

from backend.models.location_model import Location
from backend.services.location_service import (
    create_location,
    delete_location,
    list_locations,
)
from pages.const import _

st.title(_("LOCATION_LIST_LOCATION_MANAGEMENT"))

@st.dialog(_("LOCATION_LIST_ADD_LOCATION"))
def add_location_dialog() -> None:
    location = dict()
    colA, colB = st.columns([.5, .5])
    with colA:
        location["street"] = st.text_input(_("STREET"))
        location["area"] = st.text_input(_("AREA"))
        location["lat"] = st.text_input(f'{_("LATITUDE")}*')
        location["lng"] = st.text_input(f'{_("LONGITUDE")}*')
    with colB:
        location["city"] = st.text_input(f'{_("CITY")}*')
        location["postal_code"] = st.text_input(f'{_("POSTAL_CODE")}*')
        location["state"] = st.text_input(f'{_("STATE")}*')
        location["country"] = st.text_input(f'{_("COUNTRY")}*', value="France")

    if st.button(_("SUBMIT")):
        try:
            create_location(location)
        except Exception as e:
            st.error(e)
        else:
            st.rerun()


@st.dialog(_("LOCATION_LIST_DELETE_LOCATION"))
def delete_location_dialog(location: Location) -> None:
    st.subheader(_("LOCATION_LIST_DELETE_A_LOCATION"))
    st.write(f"{_('LOCATION_LIST_ARE_YOU_SURE_TO_DELETE')} {location.name}")
    if st.button(_("DELETE")):
        delete_location(location.id)
        st.rerun()


def location_list() -> None:

    locations_list: list[Location] = list_locations()
    col_search, col_add = st.columns([0.9, 0.1])


    with col_add:
        if getattr(st.session_state, "admin", False) and st.button("", icon=":material/add:"):
            add_location_dialog()

    col_location, col_delete = st.columns([0.9, 0.1], vertical_alignment="top" )
    for index, location in enumerate(locations_list):
        with col_location:
            st.write(", ".join([text for text in[
                location.street or "", location.area or "", location.city,location.postal_code, location.state, location.country,
            ] if text]))
        with col_delete:
            if getattr(st.session_state, "admin", False) and st.button("", key=f"del_location_{index}", icon=":material/delete:"):
                delete_location_dialog(location)

location_list()
