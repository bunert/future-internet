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

from multiprocessing.dummy import Pool


def is_in_path(edge, path):
    return edge in [(path[i], path[i + 1]) for i in range(len(path) - 1)]


def solve(n, in_graph_filename, in_demands_filename, in_paths_filename, out_rates_filename):
    # Read in input
    graph = wanteutility.read_graph(in_graph_filename)
    demands = wanteutility.read_demands(in_demands_filename)
    all_paths = wanteutility.read_all_paths(in_paths_filename)
    paths_x_to_y = wanteutility.get_paths_x_to_y(all_paths, graph)

    # Write the linear program
    lp_path = f"../myself/output/b/program_{n}.lp"
    with open(lp_path, "w+") as program_file:
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
    var_val_map = wanteutility.ortools_solve_lp_and_get_var_val_map(
        lp_path
    )

    # Finally, write the rates to the output file
    with open(out_rates_filename, "w+") as rate_file:
        output = ["{:.6f}".format(var_val_map["p_{}".format(all_paths.index(path))]) if (
                var_val_map["p_{}".format(all_paths.index(path))] > 0) else 0 for path in all_paths]
        rate_file.write("\n".join("{}".format(bw) for bw in output))


def solve_wrapper(appendix):
    print(appendix)
    solve(
        appendix,
        "../ground_truth/input/b/graph%s.graph" % appendix,
        "../ground_truth/input/b/demand%s.demand" % appendix,
        "../ground_truth/input/b/path%s.path" % appendix,
        "../myself/output/b/rate%s.rate" % appendix
    )


def main():
    pool = Pool()
    pool.map(solve_wrapper, range(assignment_parameters.num_tests_b))
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
