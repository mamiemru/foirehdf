import os
from collections.abc import Callable
from functools import wraps
from typing import Annotated

from fastapi import FastAPI, Query, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from nicegui import ui
from tinydb import TinyDB

from backend import api_router
from backend.models.fair_model import SearchFairQuery
from backend.models.ride_model import SearchRideQuery
from backend.services.ride_service import get_ride_by_id
from frontend.fair_create import fair_create
from frontend.fair_list import fair_list
from frontend.fair_view import fair_view
from frontend.ride_create import ride_create
from frontend.ride_list import ride_list
from frontend.ride_view import ride_view


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the Database in state then yield the app."""
    app.state.db = TinyDB("fair_db.json")
    yield
    app.state.db.close()

def get_db(request: Request) -> TinyDB:
    """Return the instancied Database."""
    return request.app.state.db

app = FastAPI(
    lifespan=lifespan,
    title="Foire HDF",
    description="Une Base des foires et manèges des Haut de france",
    version="v2",
)

app.include_router(api_router)
app.mount("/statics", StaticFiles(directory="statics"), name="statics")


def with_sidebar(func: Callable) -> Callable:
    """Wrap page content with the sidebar layout."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> None:

        drawer = ui.left_drawer(top_corner=True, bottom_corner=True).classes("fixed top-0 left-0 z-50 w-64 bg-lightwhite shadow-lg h-full")
        with ui.header().classes("bg-white shadow p-2"):
            ui.button(icon="menu", on_click=lambda: drawer.toggle()).props("flat dense round")

        with drawer:
            ui.image("statics/logo-dark.png")
            ui.label(app.title).classes("text-lg font-bold mt-0 mb-1")
            ui.label(app.description).classes("text-sm font-italic mt-0 mb-4")
            ui.link("🏠 Accueil", "/")
            ui.link("📅 Foires", "/fair_list")
            ui.link("🎢 Manèges", "/ride_list")

        with ui.column().classes("w-full p-4"):
            func(*args, **kwargs)

        #with ui.footer().classes("bg-white w-full p-4"):
        #       ui.label("My Footer").classes("text-lg")

    return wrapper


@ui.page("/fair_list")
@with_sidebar
def route_fair_list(search_fair_query: Annotated[SearchFairQuery, Query()]) -> None:
    fair_list(search_fair_query=search_fair_query)

@ui.page("/fair_create")
@with_sidebar
def route_fair_create():
    fair_create()

@ui.page("/fair_view/{fair_id}")
@with_sidebar
def route_fair_view(fair_id: str):
    fair_view(fair_id)

@ui.page("/ride_list")
@with_sidebar
def route_ride_list(search_ride_query: Annotated[SearchRideQuery, Query()]) -> None:
    ride_list(search_ride_query=search_ride_query)

@ui.page("/ride_create")
@with_sidebar
def route_ride_create() -> None:
    ride_create()

@ui.page("/ride_view/{ride_id}")
@with_sidebar
def route_ride_view(ride_id: str):
    ride = get_ride_by_id(ride_id)
    ride_view(ride)

@ui.page("/")
@with_sidebar
def main_page():
    pass


ui.add_head_html("""<style>body { background-color: #f4f2ee; }</style>""")
ui.run_with(app=app)
ui.run(
    title=app.title,
    favicon="statics/logo.png",
    dark=False,
    language="fr",
    storage_secret=os.getenv("NICEGUI_SECRET","todochangethistoarealkeywaitthisisakey"),
)
