#!/usr/bin/env python

from pogostats import app
from flask import render_template
#from sqlalchemy import true

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mypokemon')
def mypokemon():
    return render_template('mypokemon.html')