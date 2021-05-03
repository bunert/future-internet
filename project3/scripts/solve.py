import pandas as pd
from util import *
from random import randrange


def read_satellites() -> pd.DataFrame:
    return pd.read_csv(
        '../input_data/sat_positions.txt',
        names=[
            'satellite_id',
            'orbit_id',
            'satellite_orbit_id',
            'latitude',
            'longitude',
            'altitude',
        ],
        dtype={
            'orbit_id': 'Int64'
        }
    )


def read_isls() -> dict:
    return read_valid_isls(
        '../input_data/valid_isls.txt',
    )


def read_cities() -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, dict):
    return pd.read_csv(
        '../input_data/cities.txt',
        names=[
            'id',
            'name',
            'latitude',
            'longitude',
            'weight',
        ]
    )


def read_coverage() -> pd.DataFrame:
    return pd.read_csv(
        '../input_data/city_coverage.txt',
        names=[
            'city_id',
            'satellite_id',
            'length',
        ]
    )


# Stores a mapping as output file
# Expected format: [(from, to)]
# e.g. [(0, 1). (0, 2)]
def write_mapping(mapping: list):
    pd.DataFrame(mapping).to_csv('../output_data/sat_links.txt', index=False, header=False)


# Converts a dict of mappings to a list that can be used in write_mapping
# Entries with false will be ignored
# Expected format: {(from, to): Boolean}
# e.g. {(0, 1): True, (0, 2): False} -> [(0, 1)]
def dict_to_list(mapping: dict) -> list:
    return list(map(lambda x: x[0], filter(lambda x: x[1], mapping.items())))


def snake():
    results = [(x, x + 1) for x in range(1599)]

    write_mapping(results)


def full_grid():
    satellites = read_satellites()
    valid_isls = read_isls()

    # Mapping orbit_id -> satellite_orbit_id -> satellite_id
    orbits = {}
    for idx, row in satellites.iterrows():
        if row['orbit_id'] not in orbits:
            orbits[row['orbit_id']] = {}

        orbits[row['orbit_id']][row['satellite_orbit_id']] = row['satellite_id']

    mapping = {}
    for orbit_idx, orbit in orbits.items():

        for satellite_orbit_id, satellite_id in orbit.items():

            # connect within orbit
            if satellite_orbit_id + 1 in orbit and (satellite_id, satellite_id + 1) in valid_isls:
                mapping[(satellite_id, satellite_id + 1)] = True

            # connect to next orbit
            if orbit_idx + 1 in orbits and satellite_orbit_id in orbits[orbit_idx + 1]:
                mapping[(satellite_id, orbits[orbit_idx + 1][satellite_orbit_id])] = True

    write_mapping(dict_to_list(mapping))


if __name__ == '__main__':
    snake()
    # full_grid()

    exec(open("check_score.py").read())  # who needs modules anyway
    exec(open("visualize.py").read())  # who needs modules anyway
