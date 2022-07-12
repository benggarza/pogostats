import os
from flask import Flask
# out of spite of lack of documentation and clarity we are not using flask_sqlalchemy
# from flask_sqlalchemy import SQLAlchemy
# and instead normal sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pogostats.settings import *

basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize Flask app
app = Flask(__name__)
app.config.from_pyfile('settings.py') # do i want this?

# Initialize SQLAlchemy engine and session factory

# engine is a factory for connections to the db
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
# Base stores the structure of the db
Base = declarative_base(engine)
# Session is a factory for query sessions
Session = sessionmaker(bind=engine)

from pogostats import views, models, forms, helpers

# If we set the RESET_DATABASE config to true, database will be refilled at the beginning of each run
# useful for debugging
if RESET_DATABASE and os.path.exists('../pogostats/pogostats.db'):
    os.remove('../pogostats/pogostats.db')

# initialize database and fill any reference tables that shouldn't be empty #
Base.metadata.create_all(engine, checkfirst=True)
helpers.initialize_database()

#app.run(debug=True)