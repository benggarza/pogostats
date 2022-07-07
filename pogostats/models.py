from sqlalchemy import Float

from pogostats import engine, Base

from .mypokemon.models import *
from .pokedex.models import *

class PokemonType(Base):
    __tablename__ = 'pokemon_type'

    id = Column(String, primary_key=True)

class TypeEffectiveness(Base):
    __tablename__ = 'type_effectiveness'

    attack_type_id = Column(String, ForeignKey('pokemon_type.id'), primary_key=True)
    defender_type_id = Column(String, ForeignKey('pokemon_type.id'), primary_key=True)
    multiplier = Column(Float, nullable=False)

    UniqueConstraint('attack_type_id', 'defender_type_id')
    CheckConstraint('multiplier IN (0.390625, 0.625, 1.0, 1.6)', 'chk_valid_multiplier')

    def __repr__(self):
        eff = 'normally effective'
        if self.multiplier > 1:
            eff = 'super effective'
        elif self.multiplier < 1:
            eff ='not very effective'
        return "%s moves are %s against %s types" %(self.attack_type_id, eff, self.defender_type_id)

class PokemonLevel(Base):
    __tablename__ = 'pokemon_level'

    id = Column(Float, primary_key=True)
    cpm = Column(Float, nullable=False)
    stardust_cost_total = Column(Integer, nullable=False)
    candy_cost_total = Column(Integer, nullable=False)
    xl_candy_cost_total = Column(Integer, nullable=False)

    def __repr__(self):
        return "level %f : cpm %f" %(self.id, self.cpm)

class FastMove(Base):
    __tablename__ = 'fast_move'

    id = Column(String, primary_key=True)
    move_type_id = Column(String, ForeignKey('pokemon_type.id'), nullable=False)
    pow = Column(Integer, nullable=False)
    duration_ms = Column(Integer, nullable=False)
    energy_gain = Column(Integer, nullable=False)

    CheckConstraint('energy_gain >= 0', 'chk_energy_gain')

class ChargedMove(Base):
    __tablename__ = 'charged_move'

    id = Column(String, primary_key=True)
    move_type_id = Column(String, ForeignKey('pokemon_type.id'), nullable=False)
    pow = Column(Integer, nullable=False)
    duration_ms = Column(Integer, nullable=False)
    energy_cost = Column(Integer, nullable=False)

    CheckConstraint('energy_cost >= 0', 'chk_energy_cost')

Base.metadata.create_all(engine, checkfirst=True)
