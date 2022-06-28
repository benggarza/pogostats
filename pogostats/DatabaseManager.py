#import mysql.connector
import sqlite3
import pandas as pd
import re
class DatabaseManager:
    def __init__(self, hostname):
        self.cxn = sqlite3.connect('pogo.db')
        self.cursor = self.cxn.cursor()
                                        
    def close(self):
        self.cxn.close()

    def query(self, sql_query):
        result = self.cursor.execute(sql_query).fetchall()
        return pd.DataFrame(result)

    # param my_pokemon: a DataFrame or DataFrame-like?
    # or pokemon object?
    def add_my_pokemon(self, poke):
        vars = (
            poke['name'].upper(),
            poke['atk_iv'],
            poke['def_iv'],
            poke['sta_iv'],
            poke['level'],
            1.2 if poke['shadow'] else 1.0,
            0.9 if not poke['shadow'] else 1.0,

        )
        sql = "INSERT INTO my_pokemon (pokemon_id, atk_iv, def_iv, sta_iv, pokemon_level_id, shadow_multiplier, purified_multiplier, lucky_multiplier, fast_move_id, first_charged_move_id, second_charged_move_id, atk_stat, def_stat, hp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(sql, vars)
        self.cxn.commit()

