import os

import networkx as nx
from matplotlib import pyplot as plt


def save_colored_drawing(G, color_assignment, packing_chromatic_number, filename):
    nodes = list(G.nodes())
    colors = [color_assignment[node] for node in nodes]

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_color=[c - 1 for c in colors], cmap=plt.get_cmap("tab20"),
            with_labels=False, node_size=500, font_size=10)

    labels = {node: color_assignment[node] for node in nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_color='white')

    plt.title(f"Packing Coloring Solution (Chromatic Number: {packing_chromatic_number})")
    plt.savefig(filename)
    plt.close()


def draw_graph_without_colors(G):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightgray', edge_color='black')
    plt.title("Graph Without Colors")
    plt.show()


def save_to_file(G: nx.Graph, P_n: int, B_n: int, K_n: int):
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
    nx.write_adjlist(G, f"graphs/P{P_n}_♦{B_n}_K{K_n}.txt")


def save_coloring_to_file(color_assignment, packing_chromatic_number, P_n: int, B_n: int, K_n: int):
    with open(f"graphs/P{P_n}_♦{B_n}_K{K_n}_color_assignment.txt", "w") as f:
        f.write(f"Packing Chromatic Number: {packing_chromatic_number}\n")
        f.write("Color Assignment:\n")
        for node, color in color_assignment.items():
            f.write(f"Node {node}: Color {color}\n")
