import builtins
import gettext
import locale
from pathlib import Path

from shiny import App, Inputs, Outputs, Session, ui

from pages import fair_create, fair_edit, fair_list, fair_view, location_list, manufacturer_list, ride_create, ride_edit, ride_list, ride_view

# --- Localization ---
locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
locale_path = Path(__file__).parent / "locales"
language = gettext.translation("messages", localedir=locale_path, languages=["fr"])
language.install()
builtins._ = language.gettext

# --- Static resources ---
icon_path = Path(__file__).parent / "statics" / "logo.png"

# --- Admin toggle (default True) ---
admin_default = True

# --- Page groups ---
fair_pages = [
    fair_list.ui,
    fair_view.ui,
]
ride_pages = [
    ride_list.ui,
    ride_view.ui,
]
manu_pages = [manufacturer_list.ui]
loc_pages = [location_list.ui]

if admin_default:
    fair_pages.extend([fair_create.ui, fair_edit.ui])
    ride_pages.extend([ride_create.ui, ride_edit.ui])

# --- App UI ---
app_ui = ui.page_navbar(
    *fair_pages,
    *ride_pages,
    *manu_pages,
    *loc_pages,
    title="Rides App",
    window_title=_("APP_FAIRS"),
    sidebar=ui.sidebar(
        ui.input_switch("admin", _("Admin Mode"), value=admin_default),
        ui.hr(),
        ui.p("""
            Ce site n’a en aucun cas vocation à faire de la promotion ou du classement.
            Il s'agit d'une base de données dédiée aux rides d’intensité moyenne, forte et extrême.
            Mon objectif est de centraliser des informations sur certains manèges présents lors des foires 
            dans les Hauts-de-France (proche de Lille), car je trouve que, même avec Internet, certaines 
            informations restent difficiles à trouver.
            Je ne stock aucune images ou vidéos, toutes les ressources vienent d'ailleurs (page crédits à faire).
        """),
    ),
)

# --- Server (for admin toggle reactivity if needed later) ---
def server(input: Inputs, output: Outputs, session: Session):
    pass  # Optional: reactively hide pages or persist admin state

app = App(app_ui, server)
