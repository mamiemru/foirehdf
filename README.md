
### Description:

This project store and display ride for almost all funfairs located closed to Lille (France postalcode=59000).
The idea is to build a database that can store an history of where a ride goes and trace it. store some data about manufacturer, owner and where it could be next.

### Technical:

Run in python 3.12.X use typing.

There is a docker compose if as me you are too lazy to care of it running during and between dev sessions.

The main frameowrk is Nicegui that is a python builder to Quaser (vuejs) framework.
it also use fastapi but we are not gonna use much of this framework because its a simple app that does not require complexe stuff neither API exposition.
We use MVC pattern, that mean if at some point the back need to be standalone the only ony layer to do is the endpoint layer (for both front and back).

Tiny db is fun but will be changed to Sqlite at some point, im still figure out a good data model as the project grow.

Use uv to install and run the app.
My vscode setting tell ruff and mypy to be very very annoying. 

The only working translation lang is French, but you are free to add a lang (follow how python handle lang with .mo .po files).

### Cosmetic:

I do not own any photos or videos, that all link to thiers sources (mostly yt or google image).
Except for the logo (that is a two-color freakout from kmg), and 'no picture' notting is stored here.

