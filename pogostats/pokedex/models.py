from pogostats import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, CheckConstraint, UniqueConstraint

class Pokemon(Base):
    __tablename__ = 'pokemon'

    id= Column(String, primary_key=True)
    name= Column(String, nullable=False)
    pokedex_number = Column(Integer, nullable=False)
    first_type_id = Column(String, ForeignKey('pokemon_type.id'), nullable=False)
    second_type_id = Column(String, ForeignKey('pokemon_type.id'))
    base_atk = Column(Integer, nullable=False)
    base_def = Column(Integer, nullable=False)
    base_sta = Column(Integer, nullable=False)
    legendary = Column(Boolean, nullable=False)

    UniqueConstraint('id', 'name', 'first_type_id', 'second_type_id','base_atk', 'base_def', 'base_sta', name='unique_pokemon')
    CheckConstraint('pokedex_number > 0', name='chk_pokedex')

    def __repr__(self):
        return "%d - %s" % (self.pokedex_number, self.id)

class PokemonEvolution(Base):
    __tablename__ = 'pokemon_evolution'

    pokemon_id = Column(String, ForeignKey('pokemon.id'), primary_key=True)
    evolution_id = Column(String, ForeignKey('pokemon.id'), primary_key=True)
    evolution_cost = Column(Integer, nullable=False)

    CheckConstraint('evolution_cost > 0', 'chk_evolution_cost')

    def __repr__(self):
        return "%s -> %s" % (self.pokemon_id, self.evolution_id)


class PokemonFastMove(Base):
    __tablename__ = 'pokemon_fast_move'

    pokemon_id = Column(String, ForeignKey('pokemon.id'), primary_key=True)
    fast_move_id = Column(String, ForeignKey('fast_move.id'), primary_key=True)

    def __repr__(self):
        return "%s: %s" % (self.pokemon_id, self.fast_move_id)

class PokemonChargedMove(Base):
    __tablename__ = 'pokemon_charged_move'

    pokemon_id = Column(String, ForeignKey('pokemon.id'), primary_key=True)
    charged_move_id = Column(String, ForeignKey('charged_move.id'), primary_key=True)

    def __repr__(self):
        return "%s: %s" % (self.pokemon_id, self.charged_move_id)
