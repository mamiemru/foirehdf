
import gettext
import locale
from pathlib import Path
from types import SimpleNamespace

import tornado.ioloop
import tornado.web
from tornado.web import Application, RequestHandler

from backend.models.attraction_model import AttractionType
from backend.services.attractionService import (
    create_attraction,
    get_attraction_by_id,
    list_attractions,
    list_attractions_names_and_id,
    update_attraction,
)
from backend.services.fair_service import (
    create_fair,
    get_fair,
    list_fair_sort_by_status,
    list_fairs_containing_ride_id,
    update_fair,
)
from backend.services.locationService import (
    create_location,
    delete_location,
    list_locations,
    list_locations_cities,
)
from backend.services.manufacturerService import (
    create_manufacturer,
    delete_manufacturer,
    list_manufacturers,
    list_manufacturers_names,
)
from pages.form_input import DotDict

locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

locale_path = Path(__file__).parent / "locales"
language = gettext.translation("messages", localedir=locale_path, languages=["fr"])
language.install()

_ = gettext.gettext

class BaseHandler(RequestHandler):
    def render_template(self, template_name, **kwargs):
        self.render(template_name, **kwargs)

class RootRedirectHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/fairs")

class RideListHandler(BaseHandler):
    def get(self):
        search_query = SimpleNamespace(
            attraction_type=self.get_argument("attraction_type", ""),
            manufacturers=self.get_argument("manufacturers", ""),
        )
        rides = list_attractions(search_query)
        manufacturers = list_manufacturers()
        rides.reverse()
        self.render_template("ride_list.html", _=_, rides=rides, manufacturers=manufacturers, search_query=search_query)

class RideViewHandler(BaseHandler):
    def get(self, ride_id):
        ride = get_attraction_by_id(attraction_id=ride_id)
        if not ride:
            self.redirect("/rides")

        fairs = list_fairs_containing_ride_id(ride.id)
        video_cols = 3

        self.render("ride_view.html",
                    ride=ride,
                    fairs=fairs,
                    video_cols=video_cols,
                    admin=True,
                    _=_,
        )

class FairListHandler(tornado.web.RequestHandler):
    def get(self):
        search_query = SimpleNamespace(
            cities=self.get_argument("cities", default="").split(",") if self.get_argument("cities", default="") else [],
            date_min=self.get_argument("date_min", default=None),
            date_max=self.get_argument("date_max", default=None),
        )

        fairs_data = list_fair_sort_by_status(search_fair_query=search_query)
        fairs_struct = fairs_data["fairs"]
        data_map = fairs_data["map"]
        gantt_chart = fairs_data["gantt"]
        print(fairs_struct.keys())

        cities = list_locations_cities()

        self.render("fair_list.html",
            _=_,
            admin=True,
            search_query=search_query,
            cities=cities,
            fairs_struct=fairs_struct,
            data_map=data_map,
            gantt_chart=gantt_chart,
        )

class FairViewHandler(tornado.web.RequestHandler):
    def get(self, fair_id):
        fair = get_fair(id=fair_id)

        if not fair:
            self.set_status(404)
            self.render("404.html", message="Fair not found")
            return

        self.render("fair_view.html",
            fair=fair,
            _=_,
            admin=True,
        )

class FairFormHandler(tornado.web.RequestHandler):
    def get(self, fair_id=None):
        is_edit = fair_id is not None
        fair = get_fair(fair_id) if is_edit else DotDict()
        attractions_map = list_attractions_names_and_id()
        self.render("fair_create.html", fair=fair, is_edit=is_edit, attractions_map=attractions_map)

    def post(self, fair_id=None):
        is_edit = fair_id is not None

        form = self.request.arguments
        # Map form fields
        fair_data = {
            "name": self.get_argument("name"),
            "start_date": self.get_argument("start_date"),
            "end_date": self.get_argument("end_date"),
            "walk_tour_video": self.get_argument("walk_tour_video", ""),
            "official_ad_page": self.get_argument("official_ad_page", ""),
            "facebook_event_page": self.get_argument("facebook_event_page", ""),
            "city_event_page": self.get_argument("city_event_page", ""),
            "attractions": self.get_arguments("attractions"),  # multi-select
            "location": {
                "street": self.get_argument("street"),
                "area": self.get_argument("area"),
                "city": self.get_argument("city"),
                "postal_code": self.get_argument("postal_code"),
                "state": self.get_argument("state"),
                "country": self.get_argument("country"),
                "lat": self.get_argument("lat"),
                "lng": self.get_argument("lng"),
            },
        }

        try:
            if is_edit:
                update_fair(fair_data, id=fair_id)
            else:
                create_fair(fair_data)
            self.redirect("/fairs")
        except Exception as e:
            self.write(f"Error: {e!s}")

class ManufacturerListHandler(tornado.web.RequestHandler):
    def get(self):
        search_query = self.get_argument("q", "").strip()
        manufacturers = list_manufacturers()

        if search_query:
            manufacturers = [m for m in manufacturers if search_query.lower() in m.name.lower()]

        self.render("manufacturer_list.html",
                    manufacturers=manufacturers,
                    search_query=search_query,
                    admin=True,
                    _=_)

    def post(self):
        action = self.get_argument("action")
        if action == "add":
            name = self.get_argument("name")
            url = self.get_argument("website_url")
            create_manufacturer({"name": name, "website_url": url})
        elif action == "delete":
            manufacturer_id = self.get_argument("id")
            delete_manufacturer(manufacturer_id)
        self.redirect(self.request.uri)

class RideFormHandler(tornado.web.RequestHandler):
    def get(self, ride_id=None):
        manufacturers = list_manufacturers_names()
        attraction_types = list(AttractionType)

        ride = None
        if ride_id:
            ride = get_attraction_by_id(ride_id)

        self.render("ride_create.html",
                    ride=ride,
                    manufacturers=manufacturers,
                    attraction_types=attraction_types,
                    is_edit=ride is not None,
                    _=gettext.gettext)

    def post(self, ride_id=None):
        data = {
            "name": self.get_body_argument("name"),
            "description": self.get_body_argument("description", ""),
            "ticket_price": float(self.get_body_argument("ticket_price", 0)),
            "manufacturer": self.get_body_argument("manufacturer"),
            "technical_name": self.get_body_argument("technical_name", ""),
            "attraction_type": self.get_body_argument("attraction_type"),
            "manufacturer_page_url": self.get_body_argument("manufacturer_page_url", ""),
            "owner": self.get_body_argument("owner", ""),
            "news_page_url": self.get_body_argument("news_page_url", ""),
            "videos_url": self.get_body_argument("videos_url"),
            "images_url": self.get_body_argument("images_url"),
        }

        try:
            if ride_id:
                update_attraction(id=ride_id, attraction_dict=data)
            else:
                create_attraction(data)
        except Exception as e:
            self.set_status(400)
            self.write(str(e))
            return

        self.redirect("/rides")

class LocationListHandler(tornado.web.RequestHandler):
    def get(self):
        search = self.get_argument("search", "")
        locations = list_locations()
        if search:
            search = search.lower()
            locations = [l for l in locations if search in l.city.lower() or search in l.street.lower()]
        self.render("locations.html", locations=locations, search=search)

    def post(self):
        # Handle create from form
        location = {
            "street": self.get_argument("street", ""),
            "area": self.get_argument("area", ""),
            "lat": self.get_argument("lat"),
            "lng": self.get_argument("lng"),
            "city": self.get_argument("city"),
            "postal_code": self.get_argument("postal_code"),
            "state": self.get_argument("state"),
            "country": self.get_argument("country", "France"),
        }
        try:
            create_location(location)
        except Exception as e:
            self.set_status(400)
            self.write(f"Error: {e!s}")
        else:
            self.redirect("/locations")

class LocationDeleteHandler(tornado.web.RequestHandler):
    def post(self, location_id):
        try:
            delete_location(location_id)
        except Exception as e:
            self.set_status(400)
            self.write(f"Error: {e!s}")
        else:
            self.redirect("/locations")

def make_app():
    return Application([
        (r"", RootRedirectHandler),
        (r"/", RootRedirectHandler),
        (r"/rides", RideListHandler),
        (r"/ride/create", RideFormHandler),
        (r"/ride/edit/([0-9]+)", RideFormHandler),
        (r"/ride/(.+)", RideViewHandler),
        (r"/fairs", FairListHandler),
        (r"/fairs/create", FairFormHandler),
        (r"/ridfairse/edit/([0-9]+)", FairFormHandler),
        (r"/fair/(.+)", FairViewHandler),
        (r"/manufacturers", ManufacturerListHandler),
        (r"/locations", LocationListHandler),
        (r"/locations/delete/([a-zA-Z0-9\-]+)", LocationDeleteHandler),
    ],
        template_path="templates",
        static_path="static",
        debug=True,
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server started at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
