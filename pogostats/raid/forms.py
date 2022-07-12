from flask_wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired, Optional, ValidationError

class RaidSetupForm(Form):
    friendship_levels = ['None', 'Good', 'Great', 'Ultra', 'Best']

    # Species select list created in view function
    boss_pokemon_id = SelectField('Raid Boss', validators=[DataRequired()])
    tier = SelectField('Raid Tier', validators=[DataRequired()], choices=[5])
    # Fast moves and Charged moves to be dynamically allocated via ajax-api endpoint
    fast_move_id = SelectField('Fast Move', validators=[Optional()])
    charged_move_id = SelectField('Charged Move', validators=[Optional()])
    # weather select list creatd in view function
    weather_id = SelectField('Weather', validators=[Optional()])
    friendship_level = SelectField('Friendship Level', validators=[Optional()], choices=friendship_levels)
    dodge_freq = SelectField('Dodging Amount', validators=[Optional()], choices=['None', 'Half', 'All'])
    pokemon_choice = SelectField('Simulate using My Pokemon or All Pokemon', validators=[DataRequired()], choices=['My Pokemon', 'All Pokemon'])