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

def solve(in_graph_filename, in_demands_filename, in_paths_filename, out_rates_filename):

    # Read in input
    graph = wanteutility.read_graph(in_graph_filename)
    demands = wanteutility.read_demands(in_demands_filename)
    all_paths = wanteutility.read_all_paths(in_paths_filename)
    paths_x_to_y = wanteutility.get_paths_x_to_y(all_paths, graph)

    # Write the linear program
    with open("../myself/output/b/program.lp", "w+") as program_file:
        # TODO: ...
        # TODO: ...
        print("TODO")
        # TODO: ...
        # TODO: ...

    # Solve the linear program
    var_val_map = wanteutility.ortools_solve_lp_and_get_var_val_map(
        '../myself/output/b/program.lp'
    )

    # Retrieve the rates from the variable values
    for var in var_val_map:
        # TODO: ...
        # TODO: ...
        print("TODO")
        # TODO: ...
        # TODO: ...

    # Finally, write the rates to the output file
    with open(out_rates_filename, "w+") as rate_file:
        # TODO: ...
        # TODO: ...
        print("TODO")
        # TODO: ...
        # TODO: ...


def main():
    for appendix in range(assignment_parameters.num_tests_b):
        solve(
            "../ground_truth/input/b/graph%s.graph" % appendix,
            "../ground_truth/input/b/demand%s.demand" % appendix,
            "../ground_truth/input/b/path%s.path" % appendix,
            "../myself/output/b/rate%s.rate" % appendix
        )


if __name__ == "__main__":
    main()
