from typing import List

import streamlit as st

from backend.endpoints.attractionsEndpoint import create_attraction_endpoint
from backend.endpoints.manufacturerEndpoint import delete_manufacturer_endpoint
from backend.endpoints.manufacturerEndpoint import list_manufacturer_endpoint
from backend.endpoints.manufacturerEndpoint import create_manufacturer_endpoint

from backend.dto.list_dto import ListResponse
from backend.dto.manufacturer_dto import ManufacturerDto
from backend.dto.error_dto import ErrorResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse


st.title(_("MANUFACTURER_LIST_MANUFACTURER_MANAGEMENT"))

@st.dialog(_("MANUFACTURER_LIST_ADD_MANUFACTURER"))
def add_manufacturer_dialog():
    name = st.text_input(_("MANUFACTURER_LIST_NAME_OF_THE_MANUFACTURER"))
    if st.button(_("SUBMIT")):
        response: ResponseDto = create_manufacturer_endpoint({"name": name})
        if isinstance(response, SuccessResponse):
            st.success(response.message, icon=":material/check_circle:")
            st.rerun()
        elif isinstance(response, ErrorResponse):
            st.error(f"{response.message}\n \n {'\n - '.join([f'**{k}**: {v}' for k,v in response.errors.items()])})", icon=":material/close:")


@st.dialog(_("MANUFACTURER_LIST_DELETE_MANUFACTURER"))
def delete_manufacturer_dialog(manufacturer: ManufacturerDto):
    st.subheader(_("MANUFACTURER_LIST_DELETE_A_MANUFACTURER"))
    st.write(f"{_('MANUFACTURER_LIST_ARE_YOU_SURE_TO_DELETE')} {manufacturer.name}")
    if st.button(_("DELETE")):
        message = delete_manufacturer_endpoint(manufacturer.id)
        st.success(message)
        st.rerun()


def manufacturer_list():

    manufacturers_list: List[ManufacturerDto] = list()
    response: ResponseDto = list_manufacturer_endpoint()
    if isinstance(response, ListResponse):
        manufacturers_list = response.data

    col_search, col_add = st.columns([0.9, 0.1])

    with col_search:
        search_manufacturer = st.text_input(_("MANUFACTURER_SEARCH"), label_visibility="collapsed")
        if search_manufacturer:
            st.rerun()

    with col_add:
        if getattr(st.session_state, 'admin', False):
            if st.button("", icon=":material/add:"):
                add_manufacturer_dialog()


    for index, manufacturer in enumerate(manufacturers_list):
            title, view = st.columns([9, 1])
            with title:
                st.subheader(manufacturer.name)
            with view:
                if getattr(st.session_state, 'admin', False):
                    if st.button("", key=f"del_manufacturer_{index}", icon=":material/delete:"):
                        delete_manufacturer_dialog(manufacturer)

manufacturer_list()