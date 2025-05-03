import locale
import gettext
import builtins
from pathlib import Path
from typing import List
import streamlit as st

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

locale_path = Path(__file__).parent / 'locales' 
language = gettext.translation('messages', localedir=locale_path, languages=['fr'])
language.install()

builtins._ = language.gettext

icon: Path = Path(__file__).parent / "statics" / "logo.png"
st.logo(icon, size="large")

list_fairs = st.Page("pages/fair_list.py", title=_("List fairs"), icon=":material/list:")
view_fair = st.Page("pages/fair_view.py", title=_("View a fair"), icon=":material/visibility:")
create_fair = st.Page("pages/fair_create.py", title=_("Create a fair"), icon=":material/add:")
edit_fair = st.Page("pages/fair_edit.py", title=_("Edit a fair"), icon=":material/edit:")

list_rides = st.Page("pages/ride_list.py", title=_("List rides"), icon=":material/list:")
view_ride = st.Page("pages/ride_view.py", title=_("View a ride"), icon=":material/visibility:")
create_ride = st.Page("pages/ride_create.py", title=_("Add a new ride"), icon=":material/add:")
edit_ride = st.Page("pages/ride_edit.py", title=_("Edit a ride"), icon=":material/edit:")

list_manufacturer = st.Page("pages/manufacturer_list.py", title=_("List manufacturers"), icon=":material/list:")

if 'admin' not in st.session_state:
    st.session_state.admin = False

fair: List = [list_fairs, view_fair]
ride: List = [list_rides, view_ride]
manu: List = [list_manufacturer]

if st.session_state.admin:
    fair.append(create_fair)
    fair.append(edit_fair)
    ride.append(create_ride)
    ride.append(edit_ride)

pg = st.navigation(
    {
        _("Fairs"): fair,
        _("rides"): ride,
        _("manufacturer"): manu
    }
)

st.set_page_config(layout="wide", page_icon=icon)

with st.sidebar:
    st.write("""
        Ce site n’a en aucun cas vocation à faire de la promotion ou du classement.
        Il s'agit d'une base de données dédiée aux attractions d’intensité moyenne, forte et extrême.
        Mon objectif est de centraliser des informations sur certains manèges présents lors des foires dans les Hauts-de-France (proche de Lille), 
        car je trouve que, même avec Internet, certaines informations restent difficiles à trouver.
    """)
    
    

pg.run()


st.sidebar.toggle(
    "admin", key="admin", value=st.session_state.admin
)
