#import mysql.connector
import sqlite3
import pandas as pd
import requests
import re

cxn = sqlite3.connect('pogo.db')

# Reset pogo database
with open('pogo_schema.sql') as f:
    cxn.executescript(f.read())

cursor = cxn.cursor()

# Download gamemaster from pokeminers repository
gm_url = 'https://github.com/PokeMiners/game_masters/raw/master/latest/latest.json'
response = requests.get(gm_url)
gm_df = pd.DataFrame.from_dict(response.json())

# Rows that countain fast move data
fast_moves = gm_df[re.fullmatch(r'^V\d\d\d_MOVE_(\w)_FAST$', gm_df['templateId']) is not None]
fast_move_sql = "INSERT INTO fast_move (id, move_type_id, pow, duration_ms, energy_gain) VALUES (?, ?, ?, ?, ?)"
for fast_move_data in fast_moves['data']['moveSettings']:
    fast_move_vars = (fast_move_data['movementId'],
                    fast_move_data['pokemonType'],
                    fast_move_data['power'],
                    fast_move_data['durationMs'],
                    fast_move_data['energyDelta'])
    cursor.execute(fast_move_sql, fast_move_vars)

# Rows that contain charged move data
charged_moves = gm_df[re.fullmatch(r'^V\d\d\d_MOVE_(?!_FAST)$', gm_df['templateId']) is not None]
charged_move_sql = "INSERT INTO charged_move (id, move_type_id, pow, duration_ms, energy_gain) VALUES (?, ?, ?, ?, ?)"
for charged_move_data in charged_moves['data']['moveSettings']:
    charged_move_vars = (charged_move_data['movementId'],
                        charged_move_data['pokemonType'],
                        charged_move_data['power'],
                        charged_move_data['durationMs'],
                        charged_move_data['energyDelta'])
    cursor.execute(charged_move_sql, charged_move_vars)


# Rows that contain pokemon data
pokemon = gm_df[re.fullmatch(r'^V\d\d\d_POKEMON_(\w)$', gm_df['templateId']) is not None]
pokemon_charged_move_sql = "INSERT INTO pokemon_charged_move (pokemon_id, charged_move_id) VALUES (?, ?)"
pokemon_fast_move_sql = "INSERT INTO pokemon_fast_move (pokemon_id, fast_move_id) VALUES (?, ?)"
pokemon_sql = "INSERT INTO pokemon (id, first_type_id, second_type_id, base_atk, base_def, base_sta, evolution_pokemon_id, evoultion_cost, legendary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
for pokemon_data in pokemon['data']['pokemonSettings']:
    name = pokemon_data['pokemonId']
    type1 = pokemon_data['type']
    type2 = pokemon_data['type2']
    base_atk = pokemon_data['stats']['baseAttack']
    base_def = pokemon_data['stats']['baseDefense']
    base_sta = pokemon_data['stats']['baseStamina']
    fast_moves = pokemon_data['quickMoves']
    charged_moves = pokemon_data['cinematicMoves']
    evolution = pokemon_data['evolutionBranch']['evolution'] if pokemon_data['evolutionBranch'] is not None else None
    evolution_candy_cost = pokemon_data['evolutionBranch']['candyCost'] if pokemon_data['evolutionBranch'] is not None else None
    legendary = 1 if pokemon_data['pokemonClass'] is not None else 0 # a boolean

    pokemon_vars = (name, type1, type2, base_atk, base_def, base_sta, evolution, evolution_candy_cost, legendary)
    cursor.execute(pokemon_sql, pokemon_vars)

    pokemon_fast_move_vars = [(name, fast_move) for fast_move in fast_moves]
    cursor.executemany(pokemon_fast_move_sql, pokemon_fast_move_vars)

    pokemon_charged_move_vars = [(name, charged_move) for charged_move in charged_moves]
    cursor.executemany(pokemon_charged_move_sql, pokemon_charged_move_vars)



# Level Table
level_stats = pd.read_csv('level-cpm.csv', delimiter=',', header=0)
level_stats_sql = "INSERT INTO pokemon_level (id, cpm, stardust_cost_total, candy_cost_total, xl_candy_cost_total) VALUES (?, ?, ?, ?, ?)"
for row in level_stats:
    level_stats_vars = (row['level'], row['CPM'], row['stardust_total'], row['candy_total'], row['xl_total'])
    cursor.execute(level_stats_sql, level_stats_vars)


# Type effectiveness table
type_effectiveness = pd.read_csv('type_effectiveness.csv', delimiter=',', header=0, index_col='Attacking')
effectiveness_sql = "INSERT INTO type_effectiveness (attack_type_id, defender_type_id, multiplier) VALUES (?, ?, ?)"
for attack_type in type_effectiveness.index:
    for defender_type in type_effectiveness.columns:
        multiplier = 1.0
        mlg_multiplier = type_effectiveness.loc[attack_type, defender_type]
        if mlg_multiplier == 2:
            multiplier = 1.6
        elif mlg_multiplier == 0.5:
            multiplier = 0.625
        elif mlg_multiplier == 0.0:
            multiplier = 0.390625
        effectiveness_vars = (attack_type.upper(), defender_type.upper(), multiplier)
        cursor.execute(effectiveness_sql, effectiveness_vars)


cxn.commit()
cxn.close()