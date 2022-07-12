#!/usr/bin/env python

from flask import render_template, url_for, flash, redirect
from sqlalchemy import select

from pogostats import app, helpers

from .api.pokedex import *
from .api.mypokemon import *

from pogostats.models import *
from pogostats.forms import *

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

@app.route('/mypokemon/add', methods=('GET', 'POST'))
def add_mypokemon():
    form = EditMyPokemonForm()
    if form.validate_on_submit():
        # TODO - calculate other stats and add entry to database
        return redirect('/mypokemon')
    return render_template('form.html', title='Add My Pokemon', fields=None)

@app.route('/mypokemon/edit/<int:pokemon_id>', methods=('GET', 'POST'))
def edit_mypokemon(pokemon_id):
    session = helpers.load_db_session()
    my_pokemon =session.execute(select(MyPokemon).where(MyPokemon.id == pokemon_id)).first()
    form = EditMyPokemonForm(obj=my_pokemon,
                is_shadow = False if my_pokemon.shadow_multiplier == 1.0 else True,
                is_purified = False if my_pokemon.purified_multiplier == 1.0 else True,
                is_lucky = False if my_pokemon.lucky_multiplier == 1.0 else True
            )
    if form.validate_on_submit():
        # TODO - calculate other stats and replace entry in database
        return redirect('/mypokemon')
    return render_template('form.html', title='Edit My Pokemon', fields=None)

@app.route('/pokedex')
def pokedex():
    columns=['pokedex_number', 'name', 'first_type_id', 'second_type_id', 'base_atk', 'base_def', 'base_sta']
    return render_template('table.html', title='pokedex', columns=columns)

@app.route('/raid')
def raid_setup():
    form = RaidSetupForm()
    if form.validate_on_submit():
        if form.pokemon_choice == 'My Pokemon':
            # TODO - run simulations with My Pokemon
            redirect('/raid/results/mypokemon')
        else:
            # TODO - run simulations with All Pokemon
            redirect('/raid/results/allpokemon')
    return render_template('form.html', title='Raid Setup', fields=None)

@app.route('/raid/results/mypokemon')
def raid_results_mypokemon():
    # TODO - define columns
    columns = []
    return render_template('mypokemon_raid.html', title='Raid Results', columns=columns)

@app.route('/raid/results/allpokemon')
def raid_results_allpokemon():
    # TODO - define columns
    columns = []
    return render_template('table.html', title='Raid Results', columns=columns)
