
import streamlit as st

from backend.models.manufacturer_model import Manufacturer
from backend.services.manufacturer_service import create_manufacturer, delete_manufacturer, list_manufacturers
from pages.const import _

st.title(_("MANUFACTURER_LIST_MANUFACTURER_MANAGEMENT"))

@st.dialog(_("MANUFACTURER_LIST_ADD_MANUFACTURER"))
def add_manufacturer_dialog() -> None:
    name = st.text_input(_("MANUFACTURER_LIST_NAME_OF_THE_MANUFACTURER"))
    website_url = st.text_input(_("MANUFACTURER_LIST_WEBSITE_URL"))
    if st.button(_("SUBMIT")):
        create_manufacturer({"name": name, "website_url": website_url})
        st.rerun()


@st.dialog(_("MANUFACTURER_LIST_DELETE_MANUFACTURER"))
def delete_manufacturer_dialog(manufacturer: Manufacturer) -> None:
    st.subheader(_("MANUFACTURER_LIST_DELETE_A_MANUFACTURER"))
    st.write(f"{_('MANUFACTURER_LIST_ARE_YOU_SURE_TO_DELETE')} {manufacturer.name}")
    if st.button(_("DELETE")):
        delete_manufacturer(manufacturer.id)
        st.rerun()


def manufacturer_list() -> None:

    manufacturers_list: list[Manufacturer] = list_manufacturers()
    col_search, col_add = st.columns([0.9, 0.1])

    with col_search:
        search_manufacturer = st.text_input(_("MANUFACTURER_SEARCH"), label_visibility="collapsed")
        if search_manufacturer:
            st.rerun()

    with col_add:
        if getattr(st.session_state, "admin", False) and st.button("", icon=":material/add:"):
            add_manufacturer_dialog()


    title, view = st.columns([9, 1])
    for index, manufacturer in enumerate(manufacturers_list):
        with title:
            if manufacturer.website_url:
                st.markdown(f"[{manufacturer.name}]({manufacturer.website_url})")
            else:
                st.markdown(manufacturer.name)
        with view:
            if getattr(st.session_state, "admin", False) and st.button("", key=f"del_manufacturer_{index}", icon=":material/delete:"):
                delete_manufacturer_dialog(manufacturer)

manufacturer_list()
