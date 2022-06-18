CREATE DATABASE pogo;

CREATE TABLE pokemon_type (
    id VARCHAR(10) NOT NULL PRIMARY KEY UNIQUE,
)

CREATE TABLE pokemon (
    id VARCHAR(50) PRIMARY KEY NOT NULL UNIQUE,
    first_type_id VARCHAR(10) NOT NULL FOREIGN KEY REFERENCES pokemon_type.id,
    second_type_id VARCHAR(10) FOREIGN KEY REFERENCES pokemon_type.id,
    base_atk INT NOT NULL,
    base_def INT NOT NULL,
    base_sta INT NOT NULL,
    evolution_pokemon_id VARCHAR(50) FOREIGN KEY REFERENCES pokemon.id,
    evolution_cost INT,
    legendary BOOLEAN NOT NULL
);

CREATE TABLE fast_move (
    id VARCHAR(50) PRIMARY KEY NOT NULL UNIQUE,
    move_type_id VARCHAR(10) NOT NULL FOREIGN KEY REFERENCES pokemon_type.id,
    pow INT NOT NULL,
    duration_ms INT NOT NULL,
    energy_gain INT NOT NULL,
    CONSTRAINT chk_energy_gain CHECK (energy_gain > 0)
);

CREATE TABLE charged_move (
    id VARCHAR(50) PRIMARY KEY NOT NULL UNIQUE,
    move_type_id VARCHAR(10) NOT NULL FOREIGN KEY REFERENCES Types.id,
    pow INT NOT NULL,
    duration_ms INT NOT NULL,
    energy_cost INT NOT NULL,
    CONSTRAINT chk_energy_cost CHECK (energy_cost > 0)
);

CREATE TABLE pokemon_fast_move (
    pokemon_id VARCHAR(50) NOT NULL FOREIGN KEY REFERENCES pokemon.id,
    fast_move_id VARCHAR(50) NOT NULL FOREIGN KEY REFERENCES fast_move.id,
    CONSTRAINT uq_pokemon_fast_move UNIQUE(pokemon_id, fast_move_id)
);

CREATE TABLE pokemon_charged_move (
    pokemon_id VARCHAR(50) NOT NULL FOREIGN KEY REFERENCES pokemon.id,
    charged_move_id VARCHAR(50) NOT NULL FOREIGN KEY REFERENCES charged_move.id,
    CONSTRAINT uq_pokemon_charged_move UNIQUE(pokemon_id, charged_move_id)
);

CREATE TABLE pokemon_level (
    id INT PRIMARY KEY NOT NULL UNIQUE,
    cpm FLOAT NOT NULL,
    stardust_cost_total INT NOT NULL,
    candy_cost_total INT NOT NULL
);

CREATE TABLE type_effectiveness (
    attack_type_id VARCHAR(10) NOT NULL FOREIGN KEY REFERENCES pokemon_type.id,
    defender_type_id VARCHAR(10) NOT NULL FOREIGN KEY REFERENCES pokemon_type.id,
    CONSTRAINT uq_attack_defender_types UNIQUE(attack_type_id, defender_type_id),
    multiplier FLOAT NOT NULL,
    CONSTRAINT chk_valid_multiplier CHECK (multiplier IN (0.390625, 0.625, 1.0, 1.6))
);

CREATE TABLE my_pokemon (
    id PRIMARY KEY NOT NULL UNIQUE,
    pokemon_id VARCHAR(50) FOREIGN KEY REFERENCES pokemon.id,
    atk_iv INT,
    CONSTRAINT chk_atk_iv CHECK (atk_iv >=0 AND atk_iv <= 15),
    def_iv INT,
    CONSTRAINT chk_def_iv CHECK (def_iv >=0 AND def_iv <= 15),
    sta_iv INT,
    CONSTRAINT chk_sta_iv CHECK (sta_iv >=0 AND sta_iv <= 15),
    pokemon_level_id INT NOT NULL FOREIGN KEY REFERENCES pokemon_level.id,
    shadow_multiplier FLOAT NOT NULL,
    CONSTRAINT chk_valid_shadow CHECK (shadow_multiplier IN (1.2, 1.0)),
    purified_multiplier FLOAT NOT NULL,
    CONSTRAINT chk_valid_purified CHECK (purified_multiplier IN (0.9, 1.0)),
    CONSTRAINT chk_shadow_or_purified CHECK (shadow_multiplier=1.0 OR purified_multiplier=1.0)
    lucky_multiplier FLOAT NOT NULL,
    CONSTRAINT chk_valid_lucky CHECK (lucky_multiplier IN (0.5, 1.0)),
    CONSTRAINT chk_shadow_or_lucky CHECK (shadow_multiplier=1.0 OR lucky_multiplier=1.0),
    fast_move_id VARCHAR(50) NOT NULL FOREIGN KEY REFERENCES fast_move.id,
    first_charged_move_id VARCHAR(50) NOT NULL FOREIGN KEY REFERENCES charged_move.id,
    second_charged_move_id VARCHAR(50) FOREIGN KEY REFERENCES charged_move.id,
    atk_stat FLOAT NOT NULL,
    def_stat FLOAT NOT NULL,
    hp INT NOT NULL
);