from flask import request
from pogostats import app, helpers
from pogostats.models import Pokemon
from pogostats.api.util import *
from sqlalchemy import select
import json

# Template copied from https://github.com/miguelgrinberg/flask-tables
@app.route('/api/pokedex')
def pokedex_data():
    session = helpers.load_db_session()
    pokemon_query = select(
            Pokemon.pokedex_number,
            Pokemon.name,
            Pokemon.first_type_id,
            Pokemon.second_type_id,
            Pokemon.base_atk,
            Pokemon.base_def,
            Pokemon.base_sta
        ).distinct()
    total_records = len(session.execute(pokemon_query).all())
    pokemon_columns = helpers.get_query_columns(pokemon_query)

    # search filter
    search = request.args.get('search[value]')
    if search:
        pokemon_query = pokemon_query.where(
            Pokemon.name.like(f'%{search}%') |
            Pokemon.pokedex_number.like(f'%{search}%') |
            Pokemon.first_type_id.like(f'%{search}%') |
            Pokemon.second_type_id.like(f'%{search}%')
        )
    total_filtered = len(session.execute(pokemon_query).all())
    
    # sorting
    order = sorting(request.args, Pokemon, pokemon_columns)
    if order:
        pokemon_query = pokemon_query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    pokemon_query = pokemon_query.offset(start)
    pokemon_query = pokemon_query.limit(length)

    pokemon_result = session.execute(pokemon_query).all()

    # response
    return {
        'data': [pokemon._asdict() for pokemon in pokemon_result],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_records,
        'draw': request.args.get('draw', type=int),
    }

@app.route('/api/pokedex/moves')
def pokemon_moves():
    session = helpers.load_db_session()
    # TODO - build http response with lists of valid fast moves and charged moves for pokemon selected in mypokemon edit/add form and raid setup form