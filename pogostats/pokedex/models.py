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