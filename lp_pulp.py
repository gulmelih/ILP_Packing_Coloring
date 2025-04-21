import itertools
import time

import networkx as nx
from matplotlib import pyplot as plt

from packing_coloring_solver import solve_packing_coloring


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


def main():
    for i in itertools.count(1):
        start_time = time.time()
        G = create_path_connected_k_complete_graphs(i, 5)
        color_assignment, packing_chromatic_number = solve_packing_coloring(G)
        duration = time.time() - start_time
        print(f"for {i} many K5 graphs, Packing chromatic number: {packing_chromatic_number}"
              f", Duration: {duration:.2f} seconds")
        if color_assignment:
            draw_colored_graph(G, color_assignment, packing_chromatic_number)


if __name__ == '__main__':
    main()
