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
    return render_template('table.html', title="mypokemon", columns=columns, button_url=url_for('mypokemon-add'), button_name="Add a Pokemon")

@app.route('/mypokemon/add', methods=('GET', 'POST'), endpoint='mypokemon-add')
def add_mypokemon():
    form = EditMyPokemonForm()
    if form.validate_on_submit():
        print("we got a submission!")

        session = helpers.load_db_session()

        pokedex_selection = select(Pokemon.base_atk, Pokemon.base_def, Pokemon.base_sta).where(Pokemon.id == form.pokemon_id)
        pokedex_entry = session.execute(pokedex_selection).first()
        level_selection = select(PokemonLevel.cpm).where(PokemonLevel.id == form.pokemon_level_id)
        cpm = session.execute(level_selection).first().cpm

        atk_stat = (pokedex_entry.base_atk + form.atk_iv) * cpm * (1.2 if form.is_shadow else 1.0)
        def_stat = (pokedex_entry.base_def + form.def_iv) * cpm * 1/(1.2 if form.is_shadow else 1.0)
        hp = (pokedex_entry.base_sta + form.sta_iv) * cpm

        new_my_pokemon = MyPokemon()
        form.populate_obj(new_my_pokemon)
        new_my_pokemon.shadow_multiplier = 1.2 if form.is_shadow else 1.0
        new_my_pokemon.purified_multiplier = 0.9 if form.is_purified else 1.0
        new_my_pokemon.lucky_multiplier = 0.5 if form.is_lucky else 1.0

        new_my_pokemon.atk_stat = atk_stat,
        new_my_pokemon.def_stat = def_stat,
        new_my_pokemon.hp = hp

        session.add(new_my_pokemon)
        session.commit()
        return redirect('/mypokemon')
    print(form.errors)
    # TODO - change field types, mostly to selectfields
    fields=[
            {'name':'pokemon_id', 'type':'text'},
            {'name':'pokemon_level_id', 'type':'text'},
            {'name':'atk_iv', 'type':'text'}, {'name':'def_iv', 'type':'text'}, {'name':'sta_iv', 'type':'text'},
            {'name':'is_shadow', 'type':'checkbox'}, {'name':'is_purified','type':'checkbox'}, {'name':'is_lucky', 'type':'checkbox'},
            {'name':'fast_move_id', 'type':'text'}, {'name':'first_charged_move_id', 'type':'text'}, {'name':'second_charged_move_id', 'type':'text'}
            ]
    return render_template('form.html', title='Add My Pokemon', fields=fields)

@app.route('/mypokemon/edit/<int:pokemon_id>', methods=('GET', 'POST'), endpoint='mypokemon-edit')
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
    return render_template('table.html', title='pokedex', columns=columns, button_url=None, button_name=None)

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

@app.route('/raid/results/mypokemon', endpoint='raidresults-mypokemon')
def raid_results_mypokemon():
    # TODO - define columns
    columns = []
    return render_template('mypokemon_raid.html', title='Raid Results', columns=columns)

@app.route('/raid/results/allpokemon', endpoint='raidresults-allpokemon')
def raid_results_allpokemon():
    # TODO - define columns
    columns = []
    return render_template('table.html', title='Raid Results', columns=columns)
