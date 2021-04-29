import pandas as pd
from util import *

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
        ]
    )


def read_isls() -> dict:
    return read_valid_isls(
        '../input_data/valid_isls.txt',
    )


# def read() -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, dict):
#     cities = pd.read_csv(
#         '../input_data/cities.txt',
#         names=[
#             'id',
#             'name',
#             'latitude',
#             'longitude',
#             'weight',
#         ]
#     )
#
#     coverage = pd.read_csv(
#         '../input_data/city_coverage.txt',
#         names=[
#             'city_id',
#             'satellite_id',
#             'length',
#         ]
#     )
#
#     return cities, coverage


def stupid():
    results = [[x, x + 1] for x in range(1599)]
    results = pd.DataFrame(results)

    results.to_csv('../output_data/sat_links.txt', index=False, header=False)


def grid():
    satellites = read_satellites()
    valid_isls = read_isls()

    next_adjacent = satellites.copy()
    next_adjacent['orbit_id'] = next_adjacent['orbit_id'].map(lambda x: x - 1)
    joined_adjacent = satellites.merge(next_adjacent, on=['satellite_orbit_id', 'orbit_id'])

    next_orbit = satellites.copy()
    next_orbit['satellite_orbit_id'] = next_orbit['satellite_orbit_id'].map(lambda x: x - 1)
    joined_orbit = satellites.merge(next_orbit, on=['satellite_orbit_id', 'orbit_id'])

    joined = joined_orbit.append(joined_adjacent)

    joined[['satellite_id_x', 'satellite_id_y']] \
        .to_csv('../output_data/sat_links.txt', index=False, header=False)


if __name__ == '__main__':
    stupid()
    # grid()

    exec(open("check_score.py").read())  # who needs modules anyway
