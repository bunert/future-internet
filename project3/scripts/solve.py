import pandas as pd
import networkx as nx
import numpy as np

try:
    from . import util
except (ImportError, SystemError):
    import util
from random import randrange

from progressbar import ProgressBar
pbar = ProgressBar()


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
    print("snake")
    results = [(x, x + 1) for x in range(1599)]

    return results


def full_grid():
    print("full grid")
    satellites = read_satellites()
    valid_isls = read_isls()

    # Mapping orbit_id -> satellite_orbit_id -> satellite_id
    orbits = {}
    for idx, row in satellites.iterrows():
        if row['orbit_id'] not in orbits:
            orbits[row['orbit_id']] = {}

        orbits[row['orbit_id']][row['satellite_orbit_id']] = row['satellite_id']

    # print(orbits)
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


def build_graph(city_positions, city_coverage, sat_positions, valid_isls, sat_conn_count, connections):
    g = nx.Graph()

    for city in city_positions:
        g.add_node(city)
    for city, sat in city_coverage:
        g.add_edge(city, sat, length=city_coverage[city, sat])

    for sat in sat_positions:
        g.add_node(sat)
    for key, distance in valid_isls.items():
        from_hop = min(key[0], key[1])
        to_hop = max(key[0], key[1])
        if (from_hop, to_hop) in connections or (sat_conn_count[from_hop] < 4 and sat_conn_count[to_hop] < 4):
            g.add_edge(from_hop, to_hop, length=distance)

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
            g = build_graph(city_positions, city_coverage, sat_positions, valid_isls, sat_conn_count, connections)

            path = nx.single_source_dijkstra_path(g, i, weight='length')[j]

            cur_hop = path[0]
            for next_hop in path[1:]:
                from_hop = min(cur_hop, next_hop)
                to_hop = max(cur_hop, next_hop)

                if is_satellite(from_hop) and is_satellite(to_hop) and (from_hop, to_hop) not in connections:
                    connections[(from_hop, to_hop)] = True
                    sat_conn_count[from_hop] += 1
                    sat_conn_count[to_hop] += 1

                cur_hop = next_hop

            print(f"connected {i} to {j}")

    return dict_to_list(connections)

def simple_grid():
    print("simple grid")
    sat_positions = util.read_sat_positions("../input_data/sat_positions.txt")
    valid_isls = read_isls()

    result = []
    for idx, sat in sat_positions.items():
        # add +1 and -1 of same orbit
        if idx+1 in sat_positions and (idx, idx+1) in valid_isls:
            result.append((idx, idx+1))
        if idx-1 in sat_positions and (idx, idx-1) in valid_isls:
            result.append((idx, idx-1))

        # add same id of the orbit +1 and -1
        for idx2, sat2 in sat_positions.items():
            if sat["orbit_id"] == sat2["orbit_id"]+1 and sat["sat_id_in_orbit"] == sat2["sat_id_in_orbit"] and (idx, idx2) in valid_isls:
                result.append((idx, idx2))
            if sat["orbit_id"] == sat2["orbit_id"]-1 and sat["sat_id_in_orbit"] == sat2["sat_id_in_orbit"] and (idx, idx2) in valid_isls:
                result.append((idx, idx2))
                
        
    # print(sat_positions)
    
    result_set = set(map(tuple, map(sorted, result)))
    # print(result_set)
    write_mapping(result_set)

def brute_force():
    print("brute_force")

    G = nx.Graph()

    sat_pos_file = "../input_data/sat_positions.txt"
    city_pos_file = "../input_data/cities.txt"
    city_coverage_file = "../input_data/city_coverage.txt"
    city_pair_file = "../input_data/city_pairs.txt"
    valid_isls_file = "../input_data/valid_isls.txt"
    sat_links_file = "../output_data/sat_links.txt"

    top_file = "static_html/top.html"
    bottom_file = "static_html/bottom.html"
    html_file = "viz.html"

    sat_positions = util.read_sat_positions(sat_pos_file)
    city_positions = util.read_city_positions(city_pos_file)
    city_coverage = util.read_coverage(city_coverage_file)
    city_avg = sum(city_coverage.values())/len(city_coverage)
    # print(city_avg)
    valid_isls = util.read_valid_isls(valid_isls_file)
    isls_avg = sum(valid_isls.values())/len(valid_isls)
    # print(isls_avg)
    city_pairs = util.read_city_pairs_distinct(city_pair_file)

    for sat in sat_positions:
        G.add_node(sat)
    for city in city_positions:
        G.add_node(city)
    for city, sat in city_coverage:
        G.add_edge(city, sat, length=city_coverage[city, sat]+city_avg)
    for sat, sat2 in valid_isls:
        G.add_edge(sat, sat2, length=valid_isls[sat, sat2]+isls_avg)

    sat_counters = np.zeros(1600)
    result = []
    
    weighted_pairs = map(lambda x: (x[0], x[1], city_positions[x[0]]["gdp"]*city_positions[x[1]]["gdp"]), city_pairs)
    # sort by weight (descending)
    sorted_pairs = list(map(lambda x: (x[0], x[1]), list(sorted(weighted_pairs, key=lambda x: int(x[2]), reverse=True))))

    # city_pairs (read_city_pairs):         6.97
    # city_pairs (read_city_pairs_distinct) 6.98
    #   - use length=1 (min hops):          7.06
    # sorted_pairs (desc, reverse=True):    6.99
    #   - use length=1 (min hops):          7.01
    #   - use length= _ * 1.2               6.99
    #   - use length= _ * 2                 6.99
    #   - use length= _ + avg               6.50
    # sorted_pairs (asc, reverse=False):    7.20
    #   - use length=1 (min hops):          7.24

    for src, dest in pbar(sorted_pairs):
        # print("src: " + str(src) + " dest: " + str(dest))
        path = nx.shortest_path(G, source=src, target=dest, weight='length')
        # print("shortest path (src: "+ str(src) + ", dest: " + str(dest) + ")")
        # print(path)
        if (path.__len__() <= 3):
            # print("direct link with just one sattelite")
            continue
        else:
            for j in range(1, path.__len__()-2):
                # ignore up/down links
                if (path[j] > 1599 or path[j+1] > 1599):
                    continue
                u = path[j]
                v = path[j+1]

                if ((u,v) in result or (v,u) in result):
                    # print("already inserted")
                    continue
                else:
                    result.append((u, v))

                    # print("add to result ("+ str(u) + ", " + str(v)+ ")")
                    sat_counters[u] += 1
                    sat_counters[v] += 1
                    if (sat_counters[u] >= 3):
                        iterator = G.neighbors(u)
                        # print("iterator:")
                        removable = []
                        for i in iterator:
                            # build list of connected nodes which are not cities and are not already added to result
                            if (i > 1599 or (u,i) in result or (i,u) in result):
                                # print("city or in result")
                                continue
                            removable.append((u, i))

                        G.remove_edges_from(removable)
                    if (sat_counters[v] >= 3):
                        iterator = G.neighbors(v)
                        # print("iterator:")
                        removable = []
                        for i in iterator:
                            # build list of connected nodes which are not cities and are not already added to result
                            if (i > 1599 or (v,i) in result or (i,v) in result):
                                # print("city or in result")
                                continue
                            removable.append((v, i))

                        G.remove_edges_from(removable)


    result_set = set(map(tuple, map(sorted, result)))
    # print(result_set)
    write_mapping(result_set)


if __name__ == '__main__':
    # snake()
    # full_grid()
    # simple_grid()
    brute_force()

    exec(open("check_score.py").read())  # who needs modules anyway
    exec(open("visualize.py").read())  # who needs modules anyway
