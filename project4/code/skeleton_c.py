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

try:
    from . import wanteutility
except (ImportError, SystemError):
    import wanteutility

try:
    from . import assignment_parameters
except (ImportError, SystemError):
    import assignment_parameters

import networkx as nx
from itertools import islice, permutations


def k_shortest_paths(G, source, target, k, weight=None):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))


def is_in_path(edge, path):
    return edge in [(path[i], path[i + 1]) for i in range(len(path) - 1)]


def solve(in_graph_filename, in_demands_filename, out_paths_filename, out_rates_filename):
    # Read in input
    graph = wanteutility.read_graph(in_graph_filename)
    demands = wanteutility.read_demands(in_demands_filename)

    # Generate paths and write them to out_paths_filename
    print("generate paths:")
    paths = []
    with open(out_paths_filename, "w+") as path_file:

        path_combinations = permutations(range(graph.number_of_nodes()), 2)

        for source, target in path_combinations:
            for path in k_shortest_paths(graph, source, target, 10):
                paths.append('-'.join(map(str, path)))

        path_file.write("\n".join(paths))

    # Read the paths from file
    all_paths = wanteutility.read_all_paths(out_paths_filename)
    paths_x_to_y = wanteutility.get_paths_x_to_y(all_paths, graph)

    # Apply max-min linear program from part B
    # Write the linear program
    with open("../myself/output/c/program.lp", "w+") as program_file:
        print("write LP")
        lp = ["max: Z;"]

        for dem in demands:
            constraint = "Z"
            for path in paths_x_to_y[dem[0]][dem[1]]:
                constraint += " - p_{}".format(all_paths.index(path))

            constraint += " <= 0;"
            lp.append(constraint)

        for edge in graph.edges:
            constraint = ""
            first = True
            for i, path in enumerate(all_paths):
                if is_in_path(edge, path):
                    if not first:
                        constraint += " + "
                    constraint += "p_{}".format(all_paths.index(path))
                    first = False
            if not first:
                constraint += " <= {};".format(graph.get_edge_data(edge[0], edge[1])["weight"])
                lp.append(constraint)

        for path in all_paths:
            constraint = "p_{} >= 0;".format(all_paths.index(path))
            lp.append(constraint)

        # write constraints to file
        program_file.write("\n".join(line for line in lp))

    # Solve the linear program
    print("solve LP")
    var_val_map = wanteutility.ortools_solve_lp_and_get_var_val_map(
        '../myself/output/c/program.lp'
    )

    # Finally, write the rates to the output file
    with open(out_rates_filename, "w+") as rate_file:
        output = ["{:.6f}".format(var_val_map["p_{}".format(all_paths.index(path))]) if (
                var_val_map["p_{}".format(all_paths.index(path))] > 0) else 0 for path in all_paths]
        rate_file.write("\n".join("{}".format(bw) for bw in output))


def main():
    for appendix in range(assignment_parameters.num_tests_c):
        # if appendix != 0:
        #     continue
        print("test: {}".format(appendix))
        solve(
            "../ground_truth/input/c/graph%d.graph" % appendix,
            "../ground_truth/input/c/demand.demand",
            "../myself/output/c/path%d.path" % appendix,
            "../myself/output/c/rate%d.rate" % appendix
        )


if __name__ == "__main__":
    main()
