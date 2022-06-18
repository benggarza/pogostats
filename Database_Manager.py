import mysql.connector;
import pandas as pd;
import re;
class DatabaseManager:
    def __init__(self, hostname):
        self.server = mysql.connector.connect(user = 'root', password='',
                                              host=hostname,
                                              database='pogo')
                                        
    def close(self):
        self.server.close()

    def fill_db(self, gamemaster):
        gm_df = pd.read_json(gamemaster)

        # Rows that contain pokemon data
        pokemon = gm_df[re.fullmatch(r'^V\d\d\d_POKEMON_(\w)$', gm_df['templateId']) is not None]
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
            pokemon_sql = "INSERT INTO pokemon (id, first_type_id, second_type_id, base_atk, base_def, base_sta, evolution_pokemon_id, evoultion_cost, legendary) VALUES (%s, %s, %s, %d, %d, %d, %s, %d, %d)"
            self.server.execute(pokemon_sql, pokemon_vars)

            pokemon_fast_move_vars = [(name, fast_move) for fast_move in fast_moves]
            pokemon_fast_move_sql = "INSERT INTO pokemon_fast_move (pokemon_id, fast_move_id) VALUES (%s, %s)"
            self.server.execute(pokemon_fast_move_sql, pokemon_fast_move_vars)

            pokemon_charged_move_vars = [(name, charged_move) for charged_move in charged_moves]
            pokemon_charged_move_sql = "INSERT INTO pokemon_charged_move (pokemon_id, charged_move_id) VALUES (%s, %s)"
            self.server.execute(pokemon_charged_move_sql, pokemon_charged_move_vars)


        # Rows that countain fast move data
        fast_moves = gm_df[re.fullmatch(r'^V\d\d\d_MOVE_(\w)_FAST$', gm_df['templateId']) is not None]
        for fast_move_data in fast_moves['data']['moveSettings']:
            name = fast_move_data['movementId']
            move_type = fast_move_data['pokemonType']
            move_power = fast_move_data['power']
            duration = fast_move_data['durationMs']
            energy_gain = fast_move_data['energyDelta']

            fast_move_vars = (name, move_type, move_power, duration, energy_gain)
            fast_move_sql = "INSERT INTO fast_move (id, move_type_id, pow, duration_ms, energy_gain) VALUES (%s, %s, %d, %d, %d)"
            self.server.execute(fast_move_sql, fast_move_vars)

        # Rows that contain charged move data
        charged_moves = gm_df[re.fullmatch(r'^V\d\d\d_MOVE_(?!_FAST)$', gm_df['templateId']) is not None]
        for charged_move_data in charged_moves['data']['moveSettings']:
            name = charged_move_data['movementId']
            move_type = charged_move_data['pokemonType']
            move_power = charged_move_data['power']
            duration = charged_move_data['durationMs']
            energy_cost = charged_move_data['energyDelta']

            charged_move_vars = (name, move_type, move_power, duration, energy_cost)
            charged_move_sql = "INSERT INTO charged_move (id, move_type_id, pow, duration_ms, energy_gain) VALUES (%s, %s, %d, %d, %d)"
            self.server.execute(charged_move_sql, charged_move_vars)

        # Level Table

        # Type effectiveness table


    def add_my_pokemon(self, my_pokemon):

        vars = ()
        sql = "INSERT INTO my_pokemon (id, pokemon_id, atk_iv, def_iv, sta_iv, pokemon_level_id, shadow_multiplier, purified_multiplier, lucky_multiplier, fast_move_id, first_charged_move_id, second_charged_move_id, atk_stat, def_stat, hp) VALUES (%d, %s, %d, %d, %d, %f, %f, %f, %f, %s, %s, %s, %f, %f, %d)"
        self.server.execute(sql, vars)

