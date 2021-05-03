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


def stupid():
    results = [[x, x + 1] for x in range(1599)]
    results = pd.DataFrame(results)

    results.to_csv('../output_data/sat_links.txt', index=False, header=False)


def grid():
    satellites = read_satellites()

    next_adjacent = satellites.copy()
    next_adjacent['orbit_id'] = next_adjacent['orbit_id'].map(lambda x: x - 1)
    joined_adjacent = satellites.merge(next_adjacent, on=['satellite_orbit_id', 'orbit_id'])

    next_orbit = satellites.copy()
    next_orbit['satellite_orbit_id'] = next_orbit['satellite_orbit_id'].map(lambda x: x - 1)
    joined_orbit = satellites.merge(next_orbit, on=['satellite_orbit_id', 'orbit_id'])

    joined = joined_orbit.append(joined_adjacent)

    joined[['satellite_id_x', 'satellite_id_y']] \
        .to_csv('../output_data/sat_links.txt', index=False, header=False)


def grid2():
    satellites = read_satellites()
    n = satellites['satellite_id'].size

    # Mapping orbits[orbit_id][satellite_orbit_id] = satellite_id
    orbits = {}

    # for idx, row in satellites.iterrows():
    #     if row['orbit_id'] not in orbits:
    #         orbits[row['orbit_id']] = {}
    #
    #     orbits[row['orbit_id']][row['satellite_orbit_id']] = row['satellite_id']

    valid_isls = read_isls()

    connections = [0 for _ in range(n)]
    mapping = {}

    for i, _ in enumerate(connections):
        if connections[i] == 4:
            continue

        counts = 0
        j = randrange(n)
        while j == i or j < i or connections[j] == 4 or (i, j) not in valid_isls:
            j = randrange(n)
            counts += 1


        mapping[(i, j)] = True
        connections[i] += 1
        connections[j] += 1


if __name__ == '__main__':
    # stupid()
    # grid()

    grid2()

    exec(open("check_score.py").read())  # who needs modules anyway
