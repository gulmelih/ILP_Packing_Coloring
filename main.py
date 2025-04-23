import itertools
import os
import time

import networkx as nx
from matplotlib import pyplot as plt

from packing_coloring_optimizer import solve_packing_coloring


def create_path_connected_k_complete_graphs(P_n, B_n, K_n) -> nx.Graph:
    """
    Creates a graph with n copies of K_{k_n} connected in a path-like fashion.

    :param n: Number of copies of K_{k_n}
    :param k_n: Size of each complete graph (number of nodes in each K_{k_n})
    :return: A NetworkX graph representing the structure
    """
    G = nx.Graph()  # Initialize an empty graph
    node_offset = 0  # Offset to ensure unique node labels

    assert B_n != 0, "B_n must not be zero"
    assert B_n <= K_n, "B_n must be less than or equal to K_n"
    assert P_n % B_n == 0, "P_n must be divisible by B_n"

    n_of_k_complete_graphs = P_n // B_n  # Number of K_{k_n} graphs to create

    for _ in range(n_of_k_complete_graphs):
        # Create a complete graph K_{k_n}
        K = nx.complete_graph(K_n)

        # Relabel nodes uniquely
        mapping = {node: node + node_offset for node in K.nodes()}
        K = nx.relabel_nodes(K, mapping)

        # Add the current K_{k_n} to the main graph
        G.add_edges_from(K.edges())

        if node_offset != 0:
            G.add_edge(node_offset - (K_n - B_n + 1), node_offset)

        # Update variables for the next iteration
        node_offset += K_n  # Shift offset for the next K_{k_n}

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


def draw_graph_without_colors(G):
    """Draws the graph without any colors."""
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)  # Position nodes using the spring layout
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightgray', edge_color='black')
    plt.title("Graph Without Colors")
    plt.show()


def main():
    if not os.path.exists("graphs"):
        os.makedirs("graphs")

    for P_n in itertools.count(1):
        # for B_n in range(1, P_n + 1):
        start_time = time.time()

        B_n = 1
        K_n = 5
        try:
            G = create_path_connected_k_complete_graphs(P_n, B_n, K_n)
        except Exception:
            continue

        nx.write_adjlist(G, f"graphs/P{P_n}_♦{B_n}_K{K_n}.txt")

        color_assignment, packing_chromatic_number = solve_packing_coloring(G)

        print(f"Packing Chromatic Number for P{P_n} with B{B_n} and K{K_n}: {packing_chromatic_number}"
              f" in {time.time() - start_time:.2f} seconds")

        if packing_chromatic_number > 14:
            draw_colored_graph(G, color_assignment, packing_chromatic_number)
            draw_graph_without_colors(G)
            exit("Packing chromatic number exceeded 14, stopping execution")


        # if color_assignment:
        #     draw_colored_graph(G, color_assignment, packing_chromatic_number)


if __name__ == '__main__':
    main()
