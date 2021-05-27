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
import assignment_parameters
from multiprocessing import Pool
from logger import Log
import logging


def solve_lp(n, log: Log, in_graph_filename, in_demands_filename, in_paths_filename, out_rates_filename):
    # Read in input
    graph = wanteutility.read_graph(in_graph_filename)
    all_paths = wanteutility.read_all_paths(in_paths_filename)
    demands = wanteutility.read_demands(in_demands_filename)
    paths_x_to_y = wanteutility.get_paths_x_to_y(all_paths, graph)

    # Write the linear program
    log.info("write LP")
    lp_path = f"../myself/output/b/program_{n}.lp"
    lp = ["max: Z;"]

    for dem in demands:
        variables = ["Z"]
        for path in paths_x_to_y[dem[0]][dem[1]]:
            variables.append(f"p_{all_paths.index(path)}")

        lp.append(f"{' - '.join(variables)} <= 0;")

    edge_to_paths = {}  # edge -> [paths]
    for i, path in enumerate(all_paths):
        cur_node = path[0]
        for next_node in path[1:]:
            edge_to_paths.setdefault((cur_node, next_node), []).append(i)
            cur_node = next_node

    for edge, paths in edge_to_paths.items():
        lp.append(
            f"{' + '.join(map(lambda x: 'p_' + str(x), paths))} <= {graph.get_edge_data(edge[0], edge[1])['weight']};")

    for i, path in enumerate(all_paths):
        lp.append(f"p_{i} >= 0;")

    with open(lp_path, "w+") as program_file:
        program_file.write("\n".join(lp))

    # Solve the linear program
    log.info("solve LP")
    var_val_map = wanteutility.ortools_solve_lp_and_get_var_val_map(lp_path)

    # Finally, write the rates to the output file
    with open(out_rates_filename, "w+") as rate_file:
        output = ["{:.6f}".format(var_val_map[f"p_{all_paths.index(path)}"]) if (
                var_val_map[f"p_{all_paths.index(path)}"] > 0) else 0 for path in all_paths]
        rate_file.write("\n".join(f"{bw}" for bw in output))

    log.info("finished LP")


def solve_wrapper(n):
    solve_lp(
        n,
        Log(n),
        "../ground_truth/input/b/graph%s.graph" % n,
        "../ground_truth/input/b/demand%s.demand" % n,
        "../ground_truth/input/b/path%s.path" % n,
        "../myself/output/b/rate%s.rate" % n
    )


def main():
    start = time.time()

    # with Pool() as pool:
    #     logging.info(f"Running part b with {pool._processes} processes")
    #     pool.map(solve_wrapper, range(assignment_parameters.num_tests_b))

    for n in range(assignment_parameters.num_tests_b):
        solve_wrapper(n)

    logging.info(f"Finished part b in {(time.time() - start):.02f} seconds")


if __name__ == "__main__":
    main()
