from nicegui import ui

from frontend.view_fair import view_fair


@ui.page("/other_page")
def other_page():
    view_fair(ui)

@ui.page("/dark_page", dark=True)
def dark_page():
    ui.label("Welcome to the dark side")

ui.link("Visit other page", other_page)
ui.link("Visit dark page", dark_page)

ui.run()
