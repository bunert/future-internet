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

def is_in_path(edge, path):
    return edge in [(path[i],path[i+1]) for i in range(len(path)-1)]

def solve(in_graph_filename, in_demands_filename, in_paths_filename, out_rates_filename):

    # Read in input
    graph = wanteutility.read_graph(in_graph_filename)
    demands = wanteutility.read_demands(in_demands_filename)
    all_paths = wanteutility.read_all_paths(in_paths_filename)
    paths_x_to_y = wanteutility.get_paths_x_to_y(all_paths, graph)

    edges = list(graph.edges)

    # print("demands:")
    # print(demands)
    # print("all_paths length:{}".format(len(all_paths)))
    # print(all_paths)
    # print("paths_x_to_y:")
    # print(paths_x_to_y)
    # get list of paths from x to y:
    # paths_x_t_y[x][y]
    # print(paths_x_to_y[0][1])

    # Write the linear program
    with open("../myself/output/b/program.lp", "w+") as program_file:
        LP = []
        # print("write LP:")
        # TODO: (goal)
        LP.append("max: Z;")

        # TODO: (1)
        # print("(1):")
        for dem in demands:
            constraint = "Z"
            for path in paths_x_to_y[dem[0]][dem[1]]:
                constraint += " - p_{}".format(all_paths.index(path))

            constraint += " <= 0;"
            LP.append(constraint)
        # print(LP)

        # TODO: (2)
        # print("(2):")
        for edge in edges:
            constraint = ""
            # print("edge: {}".format(edge))
            first = True
            for i, path in enumerate(all_paths):
                if (is_in_path(edge, path)):
                    if not first:
                        constraint += " + "
                    constraint += "p_{}".format(all_paths.index(path))
                    first = False
                    # print(path)
            if not first:
                constraint += " <= {};".format(graph.get_edge_data(edge[0], edge[1])["weight"])
                LP.append(constraint)
        # print(LP)

        # TODO: (3)
        # print("(3):")
        for path in all_paths:
            constraint = "p_{} >= 0;".format(all_paths.index(path))
            LP.append(constraint)
        # print(LP)

        # write constraints to file
        program_file.write("\n".join(line for line in LP))

    # Solve the linear program
    var_val_map = wanteutility.ortools_solve_lp_and_get_var_val_map(
        '../myself/output/b/program.lp'
    )

    # Retrieve the rates from the variable values
    # print(type(var_val_map))
    # for var in var_val_map:
    #     print("{}: {}".format(var, var_val_map[var]))
    #     # TODO: ...

    # Finally, write the rates to the output file
    with open(out_rates_filename, "w+") as rate_file:
        output = ["{:.6f}".format(var_val_map["p_{}".format(all_paths.index(path))]) if (var_val_map["p_{}".format(all_paths.index(path))] >0) else 0 for path in all_paths]
        rate_file.write("\n".join("{}".format(bw) for bw in output))


def main():
    for appendix in range(assignment_parameters.num_tests_b):
        # if appendix != 1:
        #     continue
        print(appendix)
        solve(
            "../ground_truth/input/b/graph%s.graph" % appendix,
            "../ground_truth/input/b/demand%s.demand" % appendix,
            "../ground_truth/input/b/path%s.path" % appendix,
            "../myself/output/b/rate%s.rate" % appendix
        )


if __name__ == "__main__":
    main()
