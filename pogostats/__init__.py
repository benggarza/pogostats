import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#app.config.from_object('app.config.Config') # do i want this?

db = SQLAlchemy(app)

from pogostats import views, models

#app.run(debug=True)