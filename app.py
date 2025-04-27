
import streamlit as st


list_fairs = st.Page("pages/fair_list.py", title="List fairs", icon=":material/list:")
view_fair = st.Page("pages/fair_view.py", title="View a fair", icon=":material/visibility:")
create_fair = st.Page("pages/fair_create.py", title="Create a fair", icon=":material/edit:")

list_rides = st.Page("pages/ride_list.py", title="List rides", icon=":material/list:")
view_ride = st.Page("pages/ride_view.py", title="View a ride", icon=":material/visibility:")
create_ride = st.Page("pages/ride_create.py", title="Add a new ride", icon=":material/edit:")

list_manufacturer = st.Page("pages/manufacturer_list.py", title="List manufacturers", icon=":material/list:")

pg = st.navigation(
    {
        "Fairs": [list_fairs, view_fair, create_fair],
        "rides": [list_rides, view_ride, create_ride],
        "manufacturer": [list_manufacturer]
    }
)

st.set_page_config(layout="wide")

with st.sidebar:
    st.write("""
        Ce site n’a en aucun cas vocation à faire de la promotion ou du classement.
        Il s'agit d'une base de données dédiée aux attractions d’intensité moyenne, forte et extrême.
        Mon objectif est de centraliser des informations sur certains manèges présents lors des foires dans les Hauts-de-France (proche de Lille), 
        car je trouve que, même avec Internet, certaines informations restent difficiles à trouver.
    """)

pg.run()