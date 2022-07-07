from colorama import Fore
from pogostats import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, CheckConstraint, UniqueConstraint

class MyPokemon(Base):
    __tablename__ = 'my_pokemon'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pokemon_id = Column(String, ForeignKey('pokemon.id'), nullable=False)
    atk_iv = Column(Integer, nullable=False)
    def_iv = Column(Integer, nullable=False)
    sta_iv = Column(Integer, nullable=False)
    pokemon_level_id = Column(Float, ForeignKey('pokemon_level.id'), nullable=False)
    shadow_multiplier = Column(Float, nullable=False)
    purified_multiplier = Column(Float, nullable=False)
    lucky_multiplier = Column(Float, nullable=False)
    fast_move_id = Column(String, ForeignKey('fast_move.id'), nullable=False)
    first_charged_move_id = Column(String, ForeignKey('charged_move.id'), nullable=False)
    second_charged_move_id = Column(String, ForeignKey('charged_move.id'))
    atk_stat = Column(Float, nullable=False)
    def_stat = Column(Float, nullable=False)
    hp = Column(Integer, nullable=False)

    CheckConstraint('atk_iv >= 0 AND atk_iv <= 15', 'chk_atk_iv')
    CheckConstraint('def_iv >= 0 AND def_iv <= 15', 'chk_def_iv')
    CheckConstraint('sta_iv >= 0 AND sta_iv <= 15', 'chk_sta_iv')
    CheckConstraint('shadow_multiplier IN (1.2, 1.0)', 'chk_valid_shadow')
    CheckConstraint('purified_multiplier IN (0.9, 1.0)', 'chk_valid_purified')
    CheckConstraint('shadow_multiplier=1.0 OR purified_multiplier=1.0','chk_shadow_or_purified')
    CheckConstraint('shadow_multiplier=1.0 OR lucky_multiplier=1.0','chk_shadow_or_lucky')
    CheckConstraint('lucky_multiplier IN (0.5, 1.0)', 'chk_valid_lucky')

    def __repr__(self):
        return "%d: %s%s (%f) IV (%d, %d, %d)" % (
                self.id, ("Shadow " if self.shadow_multiplier == 1.0 else ""),
                self.pokemon_id,
                self.pokemon_level_id,
                self.atk_iv,
                self.def_iv,
                self.sta_iv
            )
