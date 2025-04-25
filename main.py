import itertools
import os
import time

import networkx as nx
from matplotlib import pyplot as plt

from packing_coloring_optimizer import solve_packing_coloring


def create_path_connected_k_complete_graphs(P_n, B_n, K_n) -> nx.Graph:
    """
    Creates a path-connected graph consisting of complete graphs K_{k_n}.
    The graph is constructed such that it is path-connected.
    Parameters:
        P_n (int): Number of vertices of the path.
        B_n (int): Number of vertices in the complete graph K_{k_n} that are on the path.
        K_n (int): Number of vertices in the complete graph K_{k_n}.
    Returns:
        nx.Graph: A path-connected graph consisting of complete graphs K_{k_n}.
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

        # Connect with the previous K_{k_n} graph
        if node_offset != 0:
            G.add_edge(node_offset - (K_n - B_n + 1), node_offset)

        node_offset += K_n  # Shift offset for the next K_{k_n}

    return G


def draw_colored_graph(G, color_assignment, packing_chromatic_number, filename):
    """
    Draws the graph with nodes colored according to the packing coloring solution
    and saves the plot to a file.
    """
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

    plt.title(f"Packing Coloring Solution (Chromatic Number: {packing_chromatic_number})")
    # plt.show() # Uncomment to display the plot
    plt.savefig(filename)  # Save the plot to file
    plt.close()


def draw_graph_without_colors(G):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)  # Position nodes using the spring layout
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightgray', edge_color='black')
    plt.title("Graph Without Colors")
    plt.show()


def main():
    for P_n in range(1, 101):
        start_time = time.time()

        B_n = 2  # ♦ number of vertices in K_5 that are on the path
        K_n = 5  # complete graph K_5

        try:
            G = create_path_connected_k_complete_graphs(P_n, B_n, K_n)
        except AssertionError:
            continue

        color_assignment, packing_chromatic_number = solve_packing_coloring(G)

        # Write the graph to a file
        if not os.path.exists("graphs"):
            os.makedirs("graphs")

        nx.write_adjlist(G, f"graphs/P{P_n}_♦{B_n}_K{K_n}.txt")

        # Write color assignment and packing chromatic number to file
        with open(f"graphs/P{P_n}_♦{B_n}_K{K_n}_color_assignment.txt", "w") as f:
            f.write(f"Packing Chromatic Number: {packing_chromatic_number}\n")
            f.write("Color Assignment:\n")
            for node, color in color_assignment.items():
                f.write(f"Node {node}: Color {color}\n")

        # Draw the graph with colors and write to file
        draw_colored_graph(G, color_assignment, packing_chromatic_number, f"graphs/P{P_n}_♦{B_n}_K{K_n}_colored.png")

        print(f"Packing Chromatic Number for P{P_n}_♦{B_n}_K{K_n}: {packing_chromatic_number}"
              f" in {time.time() - start_time:.2f} seconds")


if __name__ == '__main__':
    main()
