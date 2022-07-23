from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, DecimalField, FloatField
from wtforms.validators import DataRequired, Optional, ValidationError
from pogostats.helpers import get_all_pokemon_ids, get_fast_moves, get_charged_moves

class EditMyPokemonForm(FlaskForm):
    # list of species to be created in addmypokemon view function
    pokemon_id = SelectField("Species", validators=[DataRequired()], choices=get_all_pokemon_ids())
    pokemon_level_id = DecimalField("Level", validators=[DataRequired()])
    atk_iv = IntegerField("Attack IV", validators=[DataRequired()])
    def_iv = IntegerField("Defense IV", validators=[DataRequired()])
    sta_iv = IntegerField("Stamina IV", validators=[DataRequired()])
    #stardust_cost -- these are easier to see for the user
    #cp -- and can calculate IV range and level
    #hp --
    is_shadow = BooleanField("Shadow", validators=[])
    is_purified = BooleanField("Purified", validators=[])
    is_lucky = BooleanField("Lucky", validators=[])
    # lists of fast moves, charged moves to be dynamically created via DataTables-ajax request and api endpoint
    fast_move_id = SelectField("Fast Move", validators=[DataRequired()], choices=get_fast_moves())
    first_charged_move_id = SelectField("Charged Move", validators=[DataRequired()], choices=get_charged_moves())
    second_charged_move_id = SelectField("Second Charged MOve", validators=[Optional()], choices=get_charged_moves())

    def validate_pokemon_level_id(form, field):
        if field.data > 50 or field.data < 1 or float(field.data) % 0.5 != 0:
            raise ValidationError("Valid levels are 1.0, 1.5, 2.0, ..., 49.5, 50.0")
    
    def validate_iv(form, field):
        if field.data > 15 or field.data < 0:
            raise ValidationError("Invalid IV value - IV's are between 0 and 15")
    validate_atk_iv = validate_def_iv = validate_sta_iv = validate_iv


    def validate_is_shadow(form, field):
        if field.data and form.is_purified.data:
            raise ValidationError("Pokemon cannot be both shadow and purified")
        if field.data and form.is_lucky.data:
            raise ValidationError("Pokemon cannot be both shadow and lucky")
