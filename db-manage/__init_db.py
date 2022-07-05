#import mysql.connector
from math import nan
import sqlite3
import pandas as pd
import requests
import re
import os

# If we are running this, make a new database
if os.path.exists('../pogostats/pogostats.db'):
    os.remove('../pogostats/pogostats.db')

cxn = sqlite3.connect('../pogostats/pogostats.db')

cursor = cxn.cursor()

cursor.execute('PRAGMA foreign_keys = ON')
# Reset pogo database
with open('pogo_schema.sql') as f:
    cxn.executescript(f.read())


# Download gamemaster from pokeminers repository
gm_url = 'https://github.com/PokeMiners/game_masters/raw/master/latest/latest.json'
response = requests.get(gm_url)
gm_df = pd.DataFrame.from_dict(response.json())

# Pokemon Types - DONE
poke_types = pd.read_csv('pokemon_types.csv', delimiter=',', header=0)
poke_types_sql = "INSERT INTO pokemon_type (id) VALUES (?)"
for (_, row) in poke_types.iterrows():
    cursor.execute(poke_types_sql, (row['type'],))
cxn.commit()


# Level Table - DONE
level_stats = pd.read_csv('level_cpm.csv', delimiter=',', header=0)
level_stats_sql = "INSERT INTO pokemon_level (id, cpm, stardust_cost_total, candy_cost_total, xl_candy_cost_total) VALUES (?, ?, ?, ?, ?)"
cursor.executemany(level_stats_sql, list(level_stats.itertuples(name=None, index=False)))
cxn.commit()


# Type effectiveness table - DONE
type_effectiveness = pd.read_csv('type_effectiveness.csv', delimiter=',', header=0) #, index_col='Attacking'
effectiveness_sql = "INSERT INTO type_effectiveness (attack_type_id, defender_type_id, multiplier) VALUES (?, ?, ?)"
cursor.executemany(effectiveness_sql, list(type_effectiveness.itertuples(name=None, index=False)))
cxn.commit()

# Rows that countain fast move data - DONE
fast_moves = gm_df[gm_df['templateId'].str.match(r'^V\d\d\d\d_MOVE_(\w+)_FAST$')==True]
# the actual move settings are in a series of dictionaries in a series of dictionaries
fast_move_data = pd.DataFrame(pd.DataFrame(fast_moves['data'].to_list())['moveSettings'].to_list())
fast_move_data.fillna(0, inplace=True)
fast_fmt = pd.DataFrame()
fast_fmt['id'] = fast_move_data['movementId'].str.extract(r'^(\w+)_FAST$')
fast_fmt['move_type_id'] = fast_move_data['pokemonType'].str.extract(r'^POKEMON_TYPE_(\w+)$')
fast_fmt['pow'] = fast_move_data['power']
fast_fmt['duration_ms'] = fast_move_data['durationMs']
fast_fmt['energy_gain'] = fast_move_data['energyDelta']
print('fast move sample: ', list(fast_fmt.itertuples(name=None, index=False))[0])
print()
fast_move_sql = "INSERT INTO fast_move (id, move_type_id, pow, duration_ms, energy_gain) VALUES (?, ?, ?, ?, ?)"

cursor.executemany(fast_move_sql, list(fast_fmt.itertuples(name=None, index=False)))
cxn.commit()

# Rows that contain charged move data - DONE
charged_moves = gm_df[gm_df['templateId'].str.match(r'^V\d\d\d\d_MOVE_(\w+)(?!_FAST)$')==True]

charged_move_data = pd.DataFrame(pd.DataFrame(charged_moves['data'].to_list())['moveSettings'].to_list())
charged_move_data.fillna(0, inplace=True)
charged_fmt = pd.DataFrame()
charged_fmt['id'] = charged_move_data['movementId'].str.extract(r'^(\w+)$')
charged_fmt['move_type_id'] = charged_move_data['pokemonType'].str.extract(r'^POKEMON_TYPE_(\w+)$')
charged_fmt['pow'] = charged_move_data['power']
charged_fmt['duration_ms'] = charged_move_data['durationMs']
charged_fmt['energy_gain'] = abs(charged_move_data['energyDelta'])
print('charged move sample: ', list(charged_fmt.itertuples(name=None, index=False))[0])
print()

charged_move_sql = "INSERT INTO charged_move (id, move_type_id, pow, duration_ms, energy_cost) VALUES (?, ?, ?, ?, ?)"

cursor.executemany(charged_move_sql, list(charged_fmt.itertuples(name=None, index=False)))
cxn.commit()

# Rows that contain pokemon data
pokemon = gm_df[gm_df['templateId'].str.match(r'^V\d\d\d\d_POKEMON_(\w+)(?<!_REVERSION)$')==True]
pokemon_data = pd.DataFrame(pd.DataFrame(pokemon['data'].to_list())['pokemonSettings'].to_list())
pokemon_sql = "INSERT INTO pokemon (id, first_type_id, second_type_id, base_atk, base_def, base_sta, legendary) VALUES (?, ?, ?, ?, ?, ?, ?)"

pokemon_fmt = pd.DataFrame()
pokemon_fmt['name'] = pokemon_data['pokemonId']
pokemon_fmt['type1'] = pokemon_data['type'].str.extract(r'^POKEMON_TYPE_([A-Z]+)$')
pokemon_fmt['type2'] = pokemon_data['type2'].str.extract(r'^POKEMON_TYPE_([A-Z]+)$') # no type = NaN?
pokemon_stats = pd.DataFrame(pokemon_data['stats'].to_list())
pokemon_fmt['base_atk'] = pokemon_stats['baseAttack'].fillna(0)
pokemon_fmt['base_def'] = pokemon_stats['baseDefense'].fillna(0)
pokemon_fmt['base_sta'] = pokemon_stats['baseStamina'].fillna(0)
pokemon_fmt['legendary'] = pokemon_data['pokemonClass'].notna()

print('pokemon sample: ', list(pokemon_fmt.itertuples(name=None, index=False))[0])
print()


# Current problem - we have different forms with same pokemon id causing unique constraint to fail
cursor.executemany(pokemon_sql, list(pokemon_fmt.itertuples(name=None, index=False)))
cxn.commit()

# evolution branch column is all 'list' dtype

# Get all pokemonIds with not-NaN evolution branches
# Use pokemonId as index for next step
evo_lists = pokemon_data[pokemon_data['evolutionBranch'].notna()][['pokemonId', 'evolutionBranch']].set_index('pokemonId')

# Expand evolution branch lists into columns
evo_df = evo_lists['evolutionBranch'].apply(pd.Series)

# Un-pivot dataframe so each item in evolution branch is in its own row
# Change pokemonId back to a column
evolution_data = evo_df.melt(ignore_index=False, value_name='evolution')['evolution'].apply(pd.Series).reset_index()

# Filter out mega evolutions and excess rows with NaNs
evolution_fmt = evolution_data[evolution_data['evolution'].notna()][['pokemonId', 'evolution', 'candyCost']]
print(evolution_fmt['evolution'].to_list())
print('pokemon evolution sample: ', list(evolution_fmt.itertuples(name=None, index=False))[0])

evolution_sql = "INSERT INTO pokemon_evolution (pokemon_id, evolution_id, evolution_cost) VALUES (?, ?, ?)"
#cursor.executemany(evolution_sql, list(evolution_fmt.itertuples(name=None, index=False)))
for evo_entry in evolution_fmt.itertuples(name=None, index=False):
    print('executing ', evo_entry)
    cursor.execute(evolution_sql, evo_entry)
cxn.commit()


pokemon_charged_move_sql = "INSERT INTO pokemon_charged_move (pokemon_id, charged_move_id) VALUES (?, ?)"
pokemon_fast_move_sql = "INSERT INTO pokemon_fast_move (pokemon_id, fast_move_id) VALUES (?, ?)"
#pokemon_fast_move_vars = [(name, fast_move) for fast_move in fast_moves]
#cursor.executemany(pokemon_fast_move_sql, pokemon_fast_move_vars)

#pokemon_charged_move_vars = [(name, charged_move) for charged_move in charged_moves]
#cursor.executemany(pokemon_charged_move_sql, pokemon_charged_move_vars)


cxn.commit()

cxn.close()