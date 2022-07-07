from pogostats import engine, Base

from .mypokemon.models import *
from .pokedex.models import *

class PokemonType(Base):
    __tablename__ = 'pokemon_type'

    id = Column(String, primary_key=True)

Base.metadata.create_all(engine, checkfirst=True)
