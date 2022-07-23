from typing import Type
from sqlalchemy import create_engine, insert, select, delete
from pogostats import Session, Base
from pogostats.models import *
import pandas as pd
import requests
import os

def load_db_session():
    session = Session()
    return session

def get_query_columns(query):
    column_descriptions = query.column_descriptions
    columns = [column_desc['name'] for column_desc in column_descriptions]
    return columns

def table_is_empty(table):
    session = load_db_session()
    return session.execute(select(table)).first() is None

def insert_df_to_table(df, table):
    session = load_db_session()
    insert_stmt = insert(table)
    session.execute(insert_stmt, df.to_dict('records'))
    session.commit()
    
def get_all_pokemon_ids():
    session = load_db_session()
    pokemon_ids = session.execute(select(Pokemon.id))
    return [p[0] for p in pokemon_ids]

def get_all_pokemon_options():
    session = load_db_session()
    pokemon_options =session.execute(select(Pokemon.id, Pokemon.name))
    return [{'label': p[1], 'value': p[0]} for p in pokemon_options]

def get_fast_moves(pokemon_id=None):
    session = load_db_session()
    stmt = select(PokemonFastMove.fast_move_id)
    if pokemon_id is not None:
        stmt = stmt.where(PokemonFastMove.pokemon_id == pokemon_id)
    fast_moves = session.execute(stmt)
    return [(f[0], f[0]) for f in fast_moves]

def get_charged_moves(pokemon_id=None):
    session = load_db_session()
    stmt = select(PokemonChargedMove.charged_move_id)
    if pokemon_id is not None:
        stmt = stmt.where(PokemonChargedMove.pokemon_id == pokemon_id)
    charged_moves = session.execute(stmt)
    return [(c[0], c[0]) for c in charged_moves]

def initialize_database():
    print("Initializing empty tables...")
    session = load_db_session()

    # Pokemon Types Table
    if table_is_empty(PokemonType):
        print("pokemon_type is empty")
        poke_types = pd.read_csv('pogostats/static/pokemon_types.csv', delimiter=',', header=0)
        poke_types.rename(columns={'type':'id'}, inplace=True)
        insert_df_to_table(poke_types, PokemonType)

    # Pokemon Level Table
    if table_is_empty(PokemonLevel):
        print("pokemon_level is empty")
        level_stats = pd.read_csv('pogostats/static/level_cpm.csv', delimiter=',', header=0)
        level_stats.rename(columns={'level':'id'}, inplace=True)
        insert_df_to_table(level_stats, PokemonLevel)

    # Type Effectiveness Table
    if table_is_empty(TypeEffectiveness):
        print("type_effectiveness is empty")
        type_effectiveness = pd.read_csv('pogostats/static/type_effectiveness.csv', delimiter=',', header=0) #, index_col='Attacking'
        insert_df_to_table(type_effectiveness, TypeEffectiveness)

    # Weather Boost Table
    if table_is_empty(WeatherBoost):
        print("weather_boost is empty")
        weather_boost = pd.read_csv('pogostats/static/weather_boost.csv', delimiter=',',header=0)
        insert_df_to_table(weather_boost, WeatherBoost)

    # The Gamemaster tables - if one is empty, replace them all
    if table_is_empty(FastMove)\
            or table_is_empty(ChargedMove)\
            or table_is_empty(Pokemon)\
            or table_is_empty(PokemonFastMove)\
            or table_is_empty(PokemonChargedMove):

        print("Gamemaster tables are empty")
        # First and foremost delete all rows from the tables
        session.execute(delete(FastMove))
        session.execute(delete(ChargedMove))
        session.execute(delete(Pokemon))
        session.execute(delete(PokemonFastMove))
        session.execute(delete(PokemonChargedMove))
        session.commit()

        # Get latest gamemaster from pokeminers github repo
        gm_url = 'https://github.com/PokeMiners/game_masters/raw/master/latest/latest.json'
        response = requests.get(gm_url)
        gm_df = pd.DataFrame.from_dict(response.json())
        
        # Fast Move Table
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
        insert_df_to_table(fast_fmt, FastMove)

        # Charged Move Table
        charged_moves = gm_df[gm_df['templateId'].str.match(r'^V\d\d\d\d_MOVE_(\w+)(?!_FAST)$')==True]

        charged_move_data = pd.DataFrame(pd.DataFrame(charged_moves['data'].to_list())['moveSettings'].to_list())
        charged_move_data.fillna(0, inplace=True)
        charged_fmt = pd.DataFrame()
        charged_fmt['id'] = charged_move_data['movementId'].str.extract(r'^(\w+)$')
        charged_fmt['move_type_id'] = charged_move_data['pokemonType'].str.extract(r'^POKEMON_TYPE_(\w+)$')
        charged_fmt['pow'] = charged_move_data['power']
        charged_fmt['duration_ms'] = charged_move_data['durationMs']
        charged_fmt['energy_cost'] = abs(charged_move_data['energyDelta'])
        print('charged move sample: ', list(charged_fmt.itertuples(name=None, index=False))[0])
        print()
        insert_df_to_table(charged_fmt, ChargedMove)

        # Pokemon Table
        pokemon = gm_df[gm_df['templateId'].str.match(r'^V\d\d\d\d_POKEMON_(\w+)(?<!_REVERSION)$')==True]#.set_index('templateId')
        pokemon_wrapper = pd.DataFrame(pokemon['data'].to_list())
        pokemon_data = pd.DataFrame(pokemon_wrapper['templateId']).join(pokemon_wrapper['pokemonSettings'].apply(pd.Series))
        pokemon_sql = "INSERT INTO pokemon (id, name, pokedex_number, first_type_id, second_type_id, base_atk, base_def, base_sta, legendary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

        pokemon_fmt = pd.DataFrame()
        pokemon_fmt['id'] = pokemon_data['form'].fillna(pokemon_data['pokemonId'])
        pokemon_fmt['name'] = pokemon_data['pokemonId']
        pokemon_fmt['pokedex_number'] = pd.to_numeric(pokemon_data['templateId'].str.extract(r'^V(\d\d\d\d)')[0])
        pokemon_fmt['first_type_id'] = pokemon_data['type'].str.extract(r'^POKEMON_TYPE_([A-Z]+)$')
        pokemon_fmt['second_type_id'] = pokemon_data['type2'].str.extract(r'^POKEMON_TYPE_([A-Z]+)$') # no type = NaN?
        pokemon_stats = pd.DataFrame(pokemon_data['stats'].to_list())
        pokemon_fmt['base_atk'] = pokemon_stats['baseAttack'].fillna(0)
        pokemon_fmt['base_def'] = pokemon_stats['baseDefense'].fillna(0)
        pokemon_fmt['base_sta'] = pokemon_stats['baseStamina'].fillna(0)
        pokemon_fmt['legendary'] = pokemon_data['pokemonClass'].notna()

        pokemon_cross = pokemon_fmt.merge(pokemon_fmt, how='cross')
        pokemon_duplicates = pokemon_cross[pokemon_cross['id_x'] == pokemon_cross['id_y'] + "_NORMAL"]['id_y']
        pokemon_fmt = pokemon_fmt[~pokemon_fmt['id'].isin(pokemon_duplicates)]

        # The Nidoran problem
        pokemon_fmt = pokemon_fmt[pokemon_fmt['id'] != 'NIDORAN_NORMAL']

        print('pokemon sample: ', list(pokemon_fmt.itertuples(name=None, index=False))[0])
        print()
        insert_df_to_table(pokemon_fmt, Pokemon)

        
        # Pokemon Evolution Table
        # Get all pokemonIds with not-NaN evolution branches
        evo_lists = pokemon_data[pokemon_data['evolutionBranch'].notna()][['pokemonId', 'form', 'evolutionBranch']]# .set_index('pokemonId')

        # Expand evolution branch lists into columns
        evo_df = evo_lists[['pokemonId', 'form']].join(evo_lists['evolutionBranch'].apply(pd.Series))

        # Un-pivot dataframe so each item in evolution branch is in its own row
        # remove excess rows
        evolution_dict = evo_df.melt(id_vars=['pokemonId','form'], value_name='evolution').dropna(subset=['evolution'])
        evolution_data = evolution_dict[['pokemonId', 'form']].join(evolution_dict['evolution'].apply(pd.Series), rsuffix='_evo')
        evolution_data.dropna(subset=['evolution'], inplace=True)
        #print(evolution_data[evolution_data['pokemonId'].str.contains("RATTATA")][['pokemonId','evolution','form','form_evo']])

        # Filter out mega evolutions and excess rows with NaNs
        evolution_fmt = pd.DataFrame()
        evolution_fmt['pokemon_id'] = evolution_data['form'].fillna(evolution_data['pokemonId'])
        evolution_fmt['evolution_id'] = evolution_data['form_evo'].fillna(evolution_data['evolution'])
        evolution_fmt['evolution_cost'] = evolution_data['candyCost']

        evolution_cross = evolution_fmt.merge(evolution_fmt, how='cross')
        evolution_duplicates = evolution_cross[evolution_cross['pokemon_id_x'] == evolution_cross['pokemon_id_y'] + "_NORMAL"]['pokemon_id_y']
        evolution_fmt = evolution_fmt[~evolution_fmt['pokemon_id'].isin(evolution_duplicates)]

        # The Nidoran problem - Both Nidoran-F and Nidoran-M's forms are "NIDORAN_NORMAL",
        #                       causing unique constraint to fail
        evolution_fmt = evolution_fmt[evolution_fmt['pokemon_id'] != "NIDORAN_NORMAL"]

        # Bad evolution ids: some pokemon instead of listing the specific form to evolve to gives the name
        # we want to replace this with the basic form *_NORMAL
        valid_id = pokemon_fmt['id']#.drop_duplicates()
        bad_evo_id_locs = ~evolution_fmt['evolution_id'].isin(valid_id)
        evolution_fmt.loc[bad_evo_id_locs, 'evolution_id'] += "_NORMAL"

        print('pokemon evolution sample: ', list(evolution_fmt.itertuples(name=None, index=False))[0])
        print()
        insert_df_to_table(evolution_fmt, PokemonEvolution)

        _pokemon_fast_data = pokemon_data[['pokemonId', 'form']].join(pokemon_data['quickMoves'].apply(pd.Series))
        pokemon_fast_data = _pokemon_fast_data.melt(id_vars=['pokemonId', 'form'], value_name='fastMove').dropna(subset=['fastMove'])
        pokemon_fast_fmt = pd.DataFrame()
        pokemon_fast_fmt['pokemon_id'] = pokemon_fast_data['form'].fillna(pokemon_fast_data['pokemonId'])
        pokemon_fast_fmt['fast_move_id'] = pokemon_fast_data['fastMove'].str.extract(r'^(\w+)_FAST$')

        # Remove pokemon ids from the duplicates df
        pokemon_fast_fmt = pokemon_fast_fmt[~pokemon_fast_fmt['pokemon_id'].isin(pokemon_duplicates)]

        # Nidoran problem
        pokemon_fast_fmt = pokemon_fast_fmt[pokemon_fast_fmt['pokemon_id'] != "NIDORAN_NORMAL"]

        # Remove fast moves that aren't in the gamemaster yet
        pokemon_fast_fmt = pokemon_fast_fmt[pokemon_fast_fmt['fast_move_id'].isin(fast_fmt['id'])]

        print('pokemon<>fast move sample:', list(pokemon_fast_fmt.itertuples(name=None, index=False))[0])
        print()

        insert_df_to_table(pokemon_fast_fmt, PokemonFastMove)

        #print(pokemon_data[['pokemonId', 'form', 'cinematicMoves']])
        pokemon_charged_move_sql = "INSERT INTO pokemon_charged_move (pokemon_id, charged_move_id) VALUES (?, ?)"

        _pokemon_charged_data = pokemon_data[['pokemonId', 'form']].join(pokemon_data['cinematicMoves'].apply(pd.Series))
        pokemon_charged_data = _pokemon_charged_data.melt(id_vars=['pokemonId', 'form'], value_name='chargedMove').dropna(subset=['chargedMove'])
        pokemon_charged_fmt = pd.DataFrame()
        pokemon_charged_fmt['pokemon_id'] = pokemon_charged_data['form'].fillna(pokemon_charged_data['pokemonId'])
        pokemon_charged_fmt['charged_move_id'] = pokemon_charged_data['chargedMove'].str.extract(r'^(\w+)$')

        # Remove pokemon ids from the duplicates df
        pokemon_charged_fmt = pokemon_charged_fmt[~pokemon_charged_fmt['pokemon_id'].isin(pokemon_duplicates)]

        # Nidoran problem
        pokemon_charged_fmt = pokemon_charged_fmt[pokemon_charged_fmt['pokemon_id'] != "NIDORAN_NORMAL"]

        # Remove charged moves that aren't in the gamemaster yet
        pokemon_charged_fmt = pokemon_charged_fmt[pokemon_charged_fmt['charged_move_id'].isin(charged_fmt['id'])]

        # Remove duplicates
        # July 6 - duplicates (Trubbish, Gunk Shot), (Galarian Weezing, Hyper Beam), (Chimecho, Psyshock)
        pokemon_charged_fmt.drop_duplicates(inplace=True)

        print('pokemon<>charged move sample:', list(pokemon_charged_fmt.itertuples(name=None, index=False))[0])
        print()

        insert_df_to_table(pokemon_charged_fmt, PokemonChargedMove)

    print("Finished initializing tables")