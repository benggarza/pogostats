# PoGO Stats
a Flask app containing utilities for the mobile game Pokemon GO

Utilities include: Pokedex searching; Pokemon storage management; Raid simulation and statistics

## Dependencies

(all package dependencies can be installed by running 'pip install -e .' in directory)

Python 3.9, flask, flask-wtf, sqlalchemy, pandas

## Structure

\* indicates file has active TODOs

**pogostats/__init__.py** - initializes flask app and database session factory
                        flask app configuration values are pulled from pogostats/settings.py

**\*pogostats/views.py** - all webpage views are defined here, for the mypokemon, pokedex, and raid sub-apps

**\*pogostats/models.py** - imports database Models from sub-apps, and declares additional Models. All models are created in database here.

**pogostats/forms.py** - imports Forms from sub-apps

**\*pogostats/helpers.py** - general helper functions

**pogostats/pogostats.db** - SQLite database file storing all Models

***pogostats/mypokemon*** - sub-app for managing and searching user's pokemon

**pogostats/mypokemon/models.py** - declares MyPokemon database Model

**pogostats/mypokemon/forms.py** - defines Form for adding new Pokemon to MyPokemon

***pogostats/pokedex*** - sub-app for searching the Pokedex

**pogostats/pokedex/models.py** - declares Pokemon database Model (species stats)

***pogostats/raid*** - a raid simulation sub-app, able to simulate raids with general counters or user's pokemon (MyPokemon)

**\*pogostats/raid/models.py** - declares RaidResult database Model for recording raid simulation results

**pogostats/raid/forms.py** - defines Form for setting up a raid simulation

***pogostats/api*** - internal api endpoints to aid in server-side processing and dynamic form filling

**pogostats/api/mypokemon.py** - api endpoints for server-side processing of MyPokemon table

**\*pogostats/api/pokedex.py** - api endpoints for server-side processing of tables and fast move/charged move queries

**\*pogostats/api/util.py** - helper functions for api endpoints. may move to pogostats/helpers.py

**pogostats/templates** - contains Jinja2 html template files

**pogostats/static** - contains css stylesheets and javascript utility files

## Installation Instructions

Open terminal in pogostats directory

Run 'pip setup -e .' to install dependencies

Export FLASK_APP=pogostats to environment

Run 'flask run' to start app