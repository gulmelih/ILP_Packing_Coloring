import itertools
import time

import networkx as nx
from matplotlib import pyplot as plt
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpBinary, LpInteger, CPLEX


def main():
    for i in itertools.count(1):
        start_time = time.time()
        G = create_path_connected_k_complete_graphs(i, 5)
        color_assignment, packing_chromatic_number = solve_packing_coloring_pulp(G)
        duration = time.time() - start_time
        print(f"for {i} many K5 graphs, Packing chromatic number: {packing_chromatic_number}"
              f", Duration: {duration:.2f} seconds")
        if color_assignment:
            draw_colored_graph(G, color_assignment, packing_chromatic_number)


def create_path_connected_k_complete_graphs(n, k_n) -> nx.Graph:
    """
    Creates a graph with n copies of K_{k_n} connected in a path-like fashion.

    :param n: Number of copies of K_{k_n}
    :param k_n: Size of each complete graph (number of nodes in each K_{k_n})
    :return: A NetworkX graph representing the structure
    """
    G = nx.Graph()  # Initialize an empty graph
    prev_last_node = None  # Track last node of the previous complete graph
    node_offset = 0  # Offset to ensure unique node labels

    for _ in range(n):
        # Create a complete graph K_{k_n}
        K = nx.complete_graph(k_n)

        # Relabel nodes uniquely
        mapping = {node: node + node_offset for node in K.nodes()}
        K = nx.relabel_nodes(K, mapping)

        # Add the current K_{k_n} to the main graph
        G.add_edges_from(K.edges())

        # Connect the current K_{k_n} to the previous one with a single edge
        if prev_last_node is not None:
            G.add_edge(prev_last_node, node_offset)  # Connect last node of previous to first of current

        # Update variables for the next iteration
        prev_last_node = node_offset + (k_n - 1)  # Last node of current K_{k_n}
        node_offset += k_n  # Shift offset for the next K_{k_n}

    return G


def solve_packing_coloring_pulp(G):
    """
    Solves the packing coloring problem on graph G using up to k colors with PuLP.

    Parameters:
      - G: a NetworkX graph.

    Returns:
      - color_assignment: a dictionary mapping each vertex to its assigned color.
      - z_val: the minimum maximum color used (i.e. the packing chromatic number found).
    """
    k = G.number_of_nodes()

    # Create the optimization model.
    model = LpProblem(name='PackingColoring', sense=LpMinimize)

    # Decision variables: x[(v, i)] equals 1 if vertex v is assigned color i, 0 otherwise.
    x = {(v, i): LpVariable(name=f"x_{v}_{i}", cat=LpBinary) for v in G.nodes for i in range(1, k + 1)}

    # Variable z representing the maximum color used (1 to k).
    z = LpVariable(name="z", lowBound=1, upBound=k, cat=LpInteger)

    # Objective: minimize z (the maximum color number used).
    model += z

    # Constraint (2): Each vertex must receive exactly one color.
    for v in G.nodes:
        model += lpSum(x[(v, i)] for i in range(1, k + 1)) == 1, f"OneColor_{v}"

    # Constraint (3): For every pair of distinct vertices (v,u) and each color i,
    # if the distance between v and u is <= i, they cannot both be assigned color i.
    for i in range(1, k + 1):
        for v, u in itertools.combinations(G.nodes, 2):
            try:
                d = nx.shortest_path_length(G, source=v, target=u)
            except nx.NetworkXNoPath:
                continue  # No path => no constraint needed
            if d <= i:
                model += x[(v, i)] + x[(u, i)] <= 1, f"Pack_{v}_{u}_color_{i}"

    # Constraint (4): If a vertex v is assigned color i then i must be <= z.
    for v in G.nodes:
        for i in range(1, k + 1):
            model += i * x[(v, i)] <= z, f"MaxColor_{v}_{i}"

    # Solve the model
    model.solve(CPLEX(msg=False))

    if model.status == 1:  # Optimal solution found
        z_val = z.varValue

        # Extract color assignment for each vertex.
        color_assignment = {}
        for v in G.nodes:
            for i in range(1, k + 1):
                if x[(v, i)].varValue > 0.5:
                    color_assignment[v] = i
                    break
        return color_assignment, z_val
    else:
        return None, None


def draw_colored_graph(G, color_assignment, packing_chromatic_number):
    """Draws the graph with nodes colored according to the packing coloring solution."""
    # Create a list of colors for each node in order, starting from 1
    nodes = list(G.nodes())
    colors = [color_assignment[node] for node in nodes]

    # Draw the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)  # Position nodes using the spring layout
    nx.draw(G, pos, node_color=[c - 1 for c in colors], cmap=plt.get_cmap("tab20"),
            with_labels=False, node_size=500, font_size=10)

    # Draw labels (color numbers) inside the nodes
    labels = {node: color_assignment[node] for node in nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_color='white')

    plt.title("Packing Coloring Solution")
    plt.show()


if __name__ == '__main__':
    main()
