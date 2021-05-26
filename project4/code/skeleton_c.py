# The MIT License (MIT)
#
# Copyright (c) 2019 Simon Kassing (ETH)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import time

import wanteutility
import networkx as nx
from itertools import islice, permutations
from multiprocessing import Pool
import logging
from logger import Log
from skeleton_b import solve_lp
import assignment_parameters


def inverse_weight(source, target, attr):
    return attr['cap'] * -1


def k_shortest_paths(G, source, target, k):
    return islice(nx.shortest_simple_paths(G, source, target), k)


def is_in_path(edge, path):
    return edge in [(path[i], path[i + 1]) for i in range(len(path) - 1)]


def solve(log, n, in_graph_filename, in_demands_filename, out_paths_filename, out_rates_filename):
    # Read in input
    graph = wanteutility.read_graph(in_graph_filename)
    for source, target in graph.edges:
        attr = graph.get_edge_data(source, target)
        attr['cap'] = attr['weight']

    # Generate paths and write them to out_paths_filename
    log.info("generating paths")
    paths = []
    with open(out_paths_filename, "w+") as path_file:

        path_combinations = permutations(range(graph.number_of_nodes()), 2)

        for source, target in path_combinations:
            for path in k_shortest_paths(graph, source, target, 10):
                paths.append('-'.join(map(str, path)))

        path_file.write("\n".join(paths))

    solve_lp(n, log, in_graph_filename, in_demands_filename, out_paths_filename, out_rates_filename)


def solve_wrapper(n):
    log = Log(n)
    log.info(f"starting test")
    solve(
        log,
        n,
        "../ground_truth/input/c/graph%d.graph" % n,
        "../ground_truth/input/c/demand.demand",
        "../myself/output/c/path%d.path" % n,
        "../myself/output/c/rate%d.rate" % n
    )


def main():
    start = time.time()
    pool = Pool()
    logging.info(f"Running part c with {pool._processes} processes")
    pool.map(solve_wrapper, range(assignment_parameters.num_tests_c))
    pool.close()
    pool.join()

    logging.info(f"Finished part c in {(time.time() - start):.02f} seconds")


if __name__ == "__main__":
    main()
