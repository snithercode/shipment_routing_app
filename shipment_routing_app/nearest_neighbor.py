from globals import loader


# Function to get the distance between two nodes (addresses)
# Time-Complexity: O(1) / Space-Complexity: 0(1)
# Involves a few simple operations (comparisons, assignments, array access) - no scaling with size of input.
# Uses a fixed amount of space that also does not scale with size of input.
def get_distance_between_nodes(node_a, node_b, distance_table):
    node_a = int(node_a)
    node_b = int(node_b)
    # Sort nodes to make sure the indices fit the distance table
    if node_b > node_a:
        node_a, node_b = node_b, node_a
    return distance_table[node_a][node_b]


# Nearest Neighbor Algorithm
# Time-Complexity: O(n^3)
# N is the number of nodes. In the worst-case scenario, the function iterates over all the nodes (n) in the list and
# for each node, get_address_id() function is called which has a time-complexity of O(n), leading to complexity o(n^2).
# With the recursive call, it may do this up to (n) times, contributing to n^3 complexity.
# Space-Complexity: O(n) Stores shortest path to every node in 'shortest_route' list, which can have n elements in
# worst-case scenario (all nodes visited).
def calculate_shortest_route(current_node, nodes, shortest_route=None, total_distance=0):
    # Initialize the route
    if shortest_route is None:
        shortest_route = []

    shortest_route.append(current_node)

    # If there are no unvisited nodes left, return the route and the total distance
    if not nodes:
        return shortest_route, total_distance

    # Initially set shortest_distance infinite so that the first checked node will be closer
    shortest_distance = float('inf')
    next_node = None

    # Now we loop over all the unvisited nodes
    for node in nodes:
        node_address_id = loader.get_address_id(node)
        distance = get_distance_between_nodes(loader.get_address_id(current_node), node_address_id, loader.distances)

        # Greedy choice: if this node is closer than the current closest, update shortest_distance and next_node
        if distance < shortest_distance:
            shortest_distance = distance
            # print(shortest_distance)
            next_node = node

    total_distance += shortest_distance
    nodes.remove(next_node)

    # Recursive call to the function for the next node
    return calculate_shortest_route(next_node, nodes, shortest_route, total_distance)
