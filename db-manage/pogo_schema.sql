CREATE TABLE pokemon_type (
    id VARCHAR(10) NOT NULL PRIMARY KEY UNIQUE
);

CREATE TABLE pokemon (
    id VARCHAR(50) PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    pokedex_number INTEGER NOT NULL,
    first_type_id VARCHAR(10) NOT NULL,
    second_type_id VARCHAR(10),
    base_atk INTEGER NOT NULL,
    base_def INTEGER NOT NULL,
    base_sta INTEGER NOT NULL,
    legendary BOOLEAN NOT NULL,
    FOREIGN KEY (first_type_id) REFERENCES pokemon_type(id),
    FOREIGN KEY (second_type_id) REFERENCES pokemon_type(id),
    CONSTRAINT unique_pokemon UNIQUE(id,name,first_type_id,second_type_id,base_atk,base_def,base_sta),
    CONSTRAINT chk_pokedex CHECK(pokedex_number >0)
);

CREATE TABLE pokemon_evolution (
    pokemon_id VARCHAR(50) NOT NULL,
    evolution_id VARCHAR(50) NOT NULL,
    evolution_cost INTEGER NOT NULL,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY (evolution_id) REFERENCES pokemon(id),
    CONSTRAINT chk_evolution_cost CHECK (evolution_cost >= 0)
);

CREATE TABLE fast_move (
    id VARCHAR(50) PRIMARY KEY NOT NULL UNIQUE,
    move_type_id VARCHAR(10) NOT NULL,
    pow INTEGER NOT NULL,
    duration_ms INTEGER NOT NULL,
    energy_gain INTEGER NOT NULL,
    CONSTRAINT chk_energy_gain CHECK (energy_gain >= 0),
    FOREIGN KEY (move_type_id) REFERENCES pokemon_type(id)
);

CREATE TABLE charged_move (
    id VARCHAR(50) PRIMARY KEY NOT NULL UNIQUE,
    move_type_id VARCHAR(10) NOT NULL,
    pow INTEGER NOT NULL,
    duration_ms INTEGER NOT NULL,
    energy_cost INTEGER NOT NULL,
    CONSTRAINT chk_energy_cost CHECK (energy_cost >= 0),
    FOREIGN KEY (move_type_id) REFERENCES pokemon_type(id)
);

CREATE TABLE pokemon_fast_move (
    pokemon_id VARCHAR(50) NOT NULL,
    fast_move_id VARCHAR(50) NOT NULL,
    CONSTRAINT uq_pokemon_fast_move UNIQUE(pokemon_id, fast_move_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY (fast_move_id) REFERENCES fast_move(id)
);

CREATE TABLE pokemon_charged_move (
    pokemon_id VARCHAR(50) NOT NULL,
    charged_move_id VARCHAR(50) NOT NULL,
    CONSTRAINT uq_pokemon_charged_move UNIQUE(pokemon_id,charged_move_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY (charged_move_id) REFERENCES charged_move(id)
);

CREATE TABLE pokemon_level (
    id FLOAT PRIMARY KEY NOT NULL UNIQUE,
    cpm FLOAT NOT NULL,
    stardust_cost_total INTEGER NOT NULL,
    candy_cost_total INTEGER NOT NULL,
    xl_candy_cost_total INTEGER NOT NULL
);

CREATE TABLE type_effectiveness (
    attack_type_id VARCHAR(10) NOT NULL,
    defender_type_id VARCHAR(10) NOT NULL,
    multiplier FLOAT NOT NULL,
    CONSTRAINT uq_attack_defender_types UNIQUE(attack_type_id,defender_type_id),
    CONSTRAINT chk_valid_multiplier CHECK (multiplier IN (0.390625, 0.625, 1.0, 1.6)),
    FOREIGN KEY (attack_type_id) REFERENCES pokemon_type(id),
    FOREIGN KEY (defender_type_id) REFERENCES pokemon_type(id)
);

CREATE TABLE my_pokemon (
    id PRIMARY KEY NOT NULL UNIQUE,
    pokemon_id VARCHAR(50),
    atk_iv INTEGER,
    def_iv INTEGER,
    sta_iv INTEGER,
    pokemon_level_id INTEGER NOT NULL,
    shadow_multiplier FLOAT NOT NULL,
    purified_multiplier FLOAT NOT NULL,
    lucky_multiplier FLOAT NOT NULL,
    fast_move_id VARCHAR(50) NOT NULL,
    first_charged_move_id VARCHAR(50) NOT NULL,
    second_charged_move_id VARCHAR(50),
    atk_stat FLOAT NOT NULL,
    def_stat FLOAT NOT NULL,
    hp INTEGER NOT NULL,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    CONSTRAINT chk_atk_iv CHECK (atk_iv >=0 AND atk_iv <= 15),
    CONSTRAINT chk_def_iv CHECK (def_iv >=0 AND def_iv <= 15),
    CONSTRAINT chk_sta_iv CHECK (sta_iv >=0 AND sta_iv <= 15),
    FOREIGN KEY (pokemon_level_id) REFERENCES pokemon_level(id),
    CONSTRAINT chk_valid_shadow CHECK (shadow_multiplier IN (1.2, 1.0)),
    CONSTRAINT chk_valid_purified CHECK (purified_multiplier IN (0.9, 1.0)),
    CONSTRAINT chk_shadow_or_purified CHECK (shadow_multiplier=1.0 OR purified_multiplier=1.0),
    CONSTRAINT chk_shadow_or_lucky CHECK (shadow_multiplier=1.0 OR lucky_multiplier=1.0),
    CONSTRAINT chk_shadow_or_lucky CHECK (shadow_multiplier=1.0 OR lucky_multiplier=1.0),
    FOREIGN KEY (fast_move_id) REFERENCES fast_move(id),
    FOREIGN KEY (first_charged_move_id) REFERENCES charged_move(id),
    FOREIGN KEY (second_charged_move_id) REFERENCES charged_move(id)
);