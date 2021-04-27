import csv

import pandas as pd


def stupid():
    results = [[x, x + 1] for x in range(1599)]
    results = pd.DataFrame(results)

    results.to_csv('../output_data/sat_links.txt', index=False, header=False)


def grid():
    satellites = pd.read_csv(
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

    next_adjacent = satellites.copy()
    next_adjacent['orbit_id'] = next_adjacent['orbit_id'].map(lambda x: x + 1)
    joined_adjacent = satellites.merge(next_adjacent, on=['satellite_orbit_id', 'orbit_id'])

    next_orbit = satellites.copy()
    next_orbit['satellite_orbit_id'] = next_orbit['satellite_orbit_id'].map(lambda x: x + 1)
    joined_orbit = satellites.merge(next_orbit, on=['satellite_orbit_id', 'orbit_id'])

    joined = joined_orbit.append(joined_adjacent)

    joined[['satellite_id_x', 'satellite_id_y']] \
        .to_csv('../output_data/sat_links.txt', index=False, header=False)


if __name__ == '__main__':
    stupid()
    # grid()
