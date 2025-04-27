from typing import List

import streamlit as st

from backend.endpoints.attractionsEndpoint import create_attraction_endpoint
from backend.endpoints.manufacturerEndpoint import delete_manufacturer_endpoint
from backend.endpoints.manufacturerEndpoint import list_manufacturer_endpoint

from backend.dto.list_dto import ListResponse
from backend.dto.manufacturer_dto import ManufacturerDto
from backend.dto.error_dto import ErrorResponse
from backend.dto.response_dto import ResponseDto
from backend.dto.success_dto import SuccessResponse

from backend.models.manufacturerModel import Manufacturer

st.title("Manufacturer Management")

@st.dialog("add manufacturer")
def add_manufacturer_dialog():
    name = st.text_input("Name of the manufacturer")
    if st.button("submit"):
        response: ResponseDto = create_attraction_endpoint({"name": name})
        if isinstance(response, SuccessResponse):
            st.success(response.message, icon=":material/check_circle:")
            st.rerun()
        elif isinstance(response, ErrorResponse):
            st.error(response.message, icon=":material/close:")
            st.error(response.errors, icon=":material/close:")


@st.dialog("delete manufacturer")
def delete_manufacturer_dialog(manufacturer: ManufacturerDto):
    st.subheader("Delete a manufacturer")
    st.write(f"Are you sure to delete {manufacturer.name}")
    if st.button("Delete"):
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
        search_manufacturer = st.text_input("search", label_visibility="collapsed")
        if search_manufacturer:
            st.rerun()

    with col_add:
        if st.button("", icon=":material/add:"):
            add_manufacturer_dialog()


    for index, manufacturer in enumerate(manufacturers_list):
            title, view = st.columns([9, 1])
            with title:
                st.subheader(manufacturer.name)
            with view:
                if st.button("", key=f"del_manufacturer_{index}", icon=":material/delete:"):
                    delete_manufacturer_dialog(manufacturer)

manufacturer_list()