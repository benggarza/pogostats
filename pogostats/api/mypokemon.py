from flask import request
from pogostats import app, helpers
from pogostats.models import MyPokemon
from pogostats.api.util import *
from sqlalchemy import select
import json


@app.route('/api/mypokemon')
def mypokemon_data():
    session = helpers.load_db_session()
    pokemon_query = select(
        MyPokemon.pokemon_id,
        MyPokemon.pokemon_level_id,
        MyPokemon.atk_iv,
        MyPokemon.def_iv,
        MyPokemon.sta_iv,
        MyPokemon.fast_move_id,
        MyPokemon.first_charged_move_id,
        MyPokemon.second_charged_move_id,
        MyPokemon.shadow_multiplier,
        MyPokemon.purified_multiplier,
        MyPokemon.lucky_multiplier
            )
    total_records = len(session.execute(pokemon_query).all())
    pokemon_columns = helpers.get_query_columns(pokemon_query)

    # search filter
    search = request.args.get('search[value]')
    if search:
        pokemon_query = pokemon_query.where(
            MyPokemon.pokemon_id.like(f'%{search}%') |
            MyPokemon.fast_move_id.like(f'%{search}%') |
            MyPokemon.first_charged_move_id.like(f'%{search}%') |
            MyPokemon.second_charged_move_id.like(f'%{search}%')
        )
    total_filtered = len(session.execute(pokemon_query).all())
    
    # sorting
    order = sorting(request.args, MyPokemon, pokemon_columns)
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

