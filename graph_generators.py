import networkx as nx


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
    G = nx.Graph()
    node_offset = 0  # Offset to ensure unique node labels

    assert P_n > 0, "P_n must be a positive integer."
    assert B_n > 0, "B_n must be a positive integer."
    assert B_n <= K_n, "B_n must be less than or equal to K_n"
    assert P_n % B_n == 0, "P_n must be divisible by B_n"

    number_of_k_complete_graphs = P_n // B_n

    for _ in range(number_of_k_complete_graphs):
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


def create_cycle_connected_k_complete_graphs(P_n, B_n, K_n) -> nx.Graph:
    assert B_n == 2, "Works correctly when B_n == 2"
    G = create_path_connected_k_complete_graphs(P_n, B_n, K_n)
    G.add_edge(0, G.number_of_nodes() - 1 - 3)  # TODO: should not be dependent on indexing of the vertices
    return G
