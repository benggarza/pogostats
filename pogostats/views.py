#!/usr/bin/env python

from pogostats import app, helpers
from .api.pokedex import *
from .api.mypokemon import *
from pogostats.models import *
from pogostats.forms import *
from flask import render_template
from sqlalchemy import select

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mypokemon')
def mypokemon():
    columns=['pokemon_id',
        'pokemon_level_id',
        'atk_iv',
        'def_iv',
        'sta_iv',
        'fast_move_id',
        'first_charged_move_id',
        'second_charged_move_id',
        'shadow_multiplier',
        'purified_multiplier',
        'lucky_multiplier']
    return render_template('table.html', title="mypokemon", columns=columns)

@app.route('/pokedex')
def pokedex():
    columns=['pokedex_number', 'name', 'first_type_id', 'second_type_id', 'base_atk', 'base_def', 'base_sta']
    return render_template('table.html', title='pokedex', columns=columns)