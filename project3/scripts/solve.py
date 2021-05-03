import pandas as pd
import util
import networkx as nx
from random import randrange

sat_pos_file = "../input_data/sat_positions.txt"
city_pos_file = "../input_data/cities.txt"
city_coverage_file = "../input_data/city_coverage.txt"
city_pair_file = "../input_data/city_pairs.txt"
valid_isls_file = "../input_data/valid_isls.txt"
sat_links_file = "../output_data/sat_links.txt"


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
    return util.read_valid_isls(
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

    return results


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

            next_satellite_id = satellite_id + 1

            # case for last satellite in orbit
            if satellite_orbit_id == max(orbit.keys()):
                next_satellite_id = orbit[0]

            # connect within orbit
            if next_satellite_id in orbit.values() and (satellite_id, next_satellite_id) in valid_isls:
                mapping[(satellite_id, next_satellite_id)] = True

            # connect to next orbit
            if orbit_idx + 1 in orbits and satellite_orbit_id in orbits[orbit_idx + 1]:
                mapping[(satellite_id, orbits[orbit_idx + 1][satellite_orbit_id])] = True

    return dict_to_list(mapping)


def is_satellite(hop_id: int) -> bool:
    return hop_id < 1600


def build_graph(city_positions, city_coverage, sat_positions, valid_isls, sat_conn_count):
    g = nx.Graph()

    for city in city_positions:
        g.add_node(city)
    for city, sat in city_coverage:
        g.add_edge(city, sat, length=city_coverage[city, sat])

    for sat in sat_positions:
        g.add_node(sat)
    for key, value in valid_isls.items():
        if sat_conn_count[key[0]] < 4 and sat_conn_count[key[1]] < 4:
            g.add_edge(key[0], key[1], length=value)

    return g


def djikstra():
    city_positions = util.read_city_positions(city_pos_file)
    city_coverage = util.read_coverage(city_coverage_file)
    sat_positions = util.read_sat_positions(sat_pos_file)
    valid_isls = util.read_valid_isls(valid_isls_file)
    city_pairs = util.read_city_pairs(city_pair_file)

    connections = {}
    sat_conn_count = [0 for _ in range(1600)]

    for i in range(10001, 10100):
        for j in range(i + 1, 10101):
            g = build_graph(city_positions, city_coverage, sat_positions, valid_isls, sat_conn_count)

            path = nx.single_source_dijkstra_path(g, i, weight='length')[j]

            cur_hop = path[0]
            for next_hop in path[1:]:
                if is_satellite(cur_hop) and is_satellite(next_hop):
                    connections[(cur_hop, next_hop)] = True
                    sat_conn_count[cur_hop] += 1
                    sat_conn_count[next_hop] += 1

                cur_hop = next_hop

            print(f"connected {i} to {j}")

    return dict_to_list(connections)


if __name__ == '__main__':
    # result = snake()
    # result = full_grid()
    result = djikstra()
    
    write_mapping(result)

    exec(open("check_score.py").read())  # who needs modules anyway
    exec(open("visualize.py").read())  # who needs modules anyway
