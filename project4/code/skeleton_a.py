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


import matplotlib.pyplot as plt
import networkx as nx

def is_in_path(edge, path):
    return edge in [(path[i],path[i+1]) for i in range(len(path)-1)]

def step1(C, F, S, K):
    c_f_list = [C[i]/F[i] if (F[i]>0) else float("inf") for i in K]
    # find k in K minimizing C_j/F_j
    min_value = min(c_f_list)
    min_index = c_f_list.index(min_value)
    # set S_k
    S[min_index] = c_f_list[min_index]
    # remove k from index list
    K.pop(min_index)
    return min_index

def step2(C, F, S, all_flows, output, edges, min_index):
    print("do step 2 with edge: {}".format(edges[min_index]))
    # print("all_flows: {}".format(all_flows))
    # print(len(all_flows))
    removable = []
    for i, flow in enumerate(all_flows):
            # print(flow)
            if (is_in_path(edges[min_index], flow)):
                print(i)
                print("flow {} inlcudes the edge (bw: {})".format(flow, S[min_index]))
                output[i] = S[min_index]
                removable.append(flow)
                # print("all_flows: {}".format(all_flows))
            
    for elem in removable:
        all_flows.remove(elem)
    # print("all_flows afterwards: {}".format(all_flows))
    S.pop(min_index)
    edges.pop(min_index)
    # print(edges)

def solve(in_graph_filename, in_demands_filename, in_paths_filename, out_rates_filename):

    # Read in input
    graph = wanteutility.read_graph(in_graph_filename)
    demands = wanteutility.read_demands(in_demands_filename)
    all_paths = wanteutility.read_all_paths(in_paths_filename)
    paths_x_to_y = wanteutility.get_paths_x_to_y(all_paths, graph)
    all_flows = wanteutility.get_all_flows(all_paths, demands)

    # Perform max-min fair allocation algorithm
    # print("graph:")
    K_size = graph.number_of_edges()
    # print("number of edges: " + str(K))

    F = [0.0] * K_size
    C = [0.0] * K_size
    S = [0.0] * K_size
    K = [i for i in range(K_size)]

    output = [0.0] * len(all_flows)
    
    # prepare f_j:
    # be the number of connections routed through link and not intersecting any (previously) congested links.
    edges = list(graph.edges)
    # print(edges)
    for i, edge in enumerate(graph.edges):
        # print("{}: edge ({})".format(i, edge))
        # print("weight: {}".format(graph.get_edge_data(edge[0], edge[1])["weight"]))
        C[i] = graph.get_edge_data(edge[0], edge[1])["weight"]
        for path in all_flows:
            # print(path)
            if(is_in_path(edge, path)):
                F[i]+=1
        # print("F[{}]: {}".format(i, F[i]))
        # print("C[{}]: {}".format(i, C[i]))

    # print("demands:")
    # print(demands)

    # print("all_paths:")
    # print(all_paths)

    # print("paths_x_to_y:")
    # print(paths_x_to_y)

    print("all_flows:")
    print(all_flows)

    # iterate until there exists some flow not yet removed
    while(len(all_flows) > 0):
        print("iteration:")
        # step 1
        min_index = step1(C, F, S, K)

        # step 2
        print("write bw {}".format(S[min_index]))
        step2(C, F, S, all_flows, output, edges, min_index)
        print("output: {}".format(output))
        print("all_flows: {}".format(all_flows))


    # plotting:
    # options = {
    #     'node_color': 'blue',
    #     'node_size': 100,
    #     'width': 3,
    #     'arrowstyle': '-|>',
    #     'arrowsize': 12,
    # }
    # nx.draw_networkx(graph, arrows=True, **options)
    # plt.show()

    # Finally, write the rates to the output file
    with open(out_rates_filename, "w+") as rate_file:
        # rate_file.write("\n".join(str(bw) for bw in output))
        rate_file.write("\n".join("{:.6f}".format(bw) for bw in output))

def main():
    for appendix in range(assignment_parameters.num_tests_a):
        if appendix == 0:
            continue
        solve(
            "../ground_truth/input/a/graph%s.graph" % appendix,
            "../ground_truth/input/a/demand%s.demand" % appendix,
            "../ground_truth/input/a/path%s.path" % appendix,
            "../myself/output/a/rate%s.rate" % appendix
        )
        exit()


if __name__ == "__main__":
    main()
