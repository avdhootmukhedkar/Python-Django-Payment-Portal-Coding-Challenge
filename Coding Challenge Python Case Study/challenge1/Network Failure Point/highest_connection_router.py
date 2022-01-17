"""
Problem Overview: Network Failure Point
We have a mesh network connected by routers labeled from 1 to 6 in a directed manner. Write an algorithm that can detect the routers with the highest number of connections so we might know which routers will cause a network failure if removed. Multiple connections between the same routers should be treated as separate connections. A tie for the most number of connections is possible. 
Requirements
Implement a identify_router function that accepts an input graph of nodes representing the total network and identifies the node with the most number of connections. 
Return the label of the node. 
Implement a directed graph data structure using Python 3.6 and up.
Each node is unique thus there will be no cases of having multiple nodes with the same label.
Each node will have an infinite number of both inbound and outbound links.
Test Cases

1 -> 2 -> 3 -> 5 -> 2 -> 1 = 2 *since router 2 has 2 inbound links and 2 outbound links

1 -> 3 -> 5 -> 6 -> 4 -> 5 -> 2 -> 6 = 5 * since router 5 has 2 inbound links and 2 outbound link

2 -> 4 -> 6 -> 2 -> 5 -> 6 = 2, 6 * since router 2 has 1 inbound link and 2 outbound links and 6 has 2 inbound links and 1 outbound link
Explanation
Explain time complexity of the identify_router function written.

"""


def identify_router(graph):
    """
    This function identifies the node with the most number of connections.
    """
    # Initialize the graph in adjacency list format
    # Time Complexity: O(E) where E is the number of edges in the graph
    directed_graph = dict()
    node_inbound_outbound_connections = dict()
    for i in range(0, len(graph) - 1):
        if graph[i] not in directed_graph:
            directed_graph[graph[i]] = [graph[i + 1]]
            node_inbound_outbound_connections[graph[i]] = [
                0,
                0,
                0,
            ]  # [inbound, outbound, total]
        else:
            directed_graph[graph[i]].append(graph[i + 1])

    # Calculate inbound and outbound links for each nodes
    # Time Complexity: O(V + E) where V and E are the numbers of nodes and edges in the graph respectively
    n = len(
        directed_graph.keys()
    )  # n is the number of nodes in the graph (n = 6)

    for node, adjacency_list in directed_graph.items():
        #  Out degree for node will be the count of direct paths from current node to other nodes
        node_inbound_outbound_connections[node][1] = len(adjacency_list)
        for (
            adjacent_node
        ) in (
            adjacency_list
        ):  # Every node that has an incoming edge from current node
            node_inbound_outbound_connections[adjacent_node][0] += 1

    # Calculate total number of connections for each node from node inbound-outbound matrix and return max connections nodes
    # Time Complexity: O(V) where V is the number of nodes in the graph
    highest_connection_nodes = []
    max_inbound_outbound_connections = 0
    for node, adjacency_list in directed_graph.items():
        node_inbound_outbound_connections[node][2] = (
            node_inbound_outbound_connections[node][0]
            + node_inbound_outbound_connections[node][1]
        )
        if (
            node_inbound_outbound_connections[node][2]
            > max_inbound_outbound_connections
        ):

            max_inbound_outbound_connections = (
                node_inbound_outbound_connections[node][2]
            )
            highest_connection_nodes = [node]
        elif (
            node_inbound_outbound_connections[node][2]
            == max_inbound_outbound_connections
        ):
            highest_connection_nodes.append(node)
    # print(directed_graph)
    # print(node_inbound_outbound_connections)
    print(*highest_connection_nodes, sep=",")
    return highest_connection_nodes


if "__main__" == __name__:
    identify_router([1, 2, 3, 5, 2, 1])
    identify_router([1, 3, 5, 6, 4, 5, 2, 6])
    identify_router([2, 4, 6, 2, 5, 6])

"""
Explain time complexity of the identify_router function written.
Step 1: Input array to adjacency_list representation ,Time Complexity: O(E) where E is the number of edges in the graph
Step 2: Calculate inbound and outbound links for each node ,Time Complexity: O(V + E) where V and E are the numbers of nodes and edges in the graph respectively
Step 3: Calculate total number of connections for each node ,Time Complexity: O(V) where V is the number of nodes in the graph
Total Time Complexity: O(E) + O(V + E) + O(V) = O(E + V)
"""
