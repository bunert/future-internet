Our approach builds a complete graph using all the valid ISL links and then runs the shortest path algorithm between each city pair. For each satallite we maintain a connection counter to keep enforce the maximum of 4 ISL. If we reach the point where a satallite has already added 4 ISL to the output graph we remove all remaining valid ISL to this satallite from the graph. In order to also minimize the number of hops we modified the weights of the edges and added the avg of all the edges to it which enforces shortest paths with a lower hop count. 