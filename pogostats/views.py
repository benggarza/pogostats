#!/usr/bin/env python

from pogostats import app, helpers
from .api.pokedex import *
from pogostats.models import *
from pogostats.forms import *
from flask import render_template
from sqlalchemy import select

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mypokemon')
def mypokemon():
    return render_template('table.html', title="My Pokemon", data=None)

@app.route('/pokedex')
def pokedex():
    columns=['pokedex_number', 'name', 'first_type_id', 'second_type_id', 'base_atk', 'base_def', 'base_sta']
    return render_template('table.html', title='Pokedex', columns=columns)