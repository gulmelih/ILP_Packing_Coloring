from docplex.mp.model import Model
import networkx as nx
import itertools

def solve_packing_coloring_cplex(G):
    """
    Solves the packing coloring problem on graph G with CPLEX.

    Parameters:
      - G: a NetworkX graph.

    Returns:
      - color_assignment: a dictionary mapping each vertex to its assigned color.
      - z_val: the minimum maximum color used (i.e. the packing chromatic number found).
    """
    k = G.number_of_nodes()

    # Create the optimization model.
    mdl = Model(name='PackingColoring')

    # Decision variables: x[(v,i)] equals 1 if vertex v is assigned color i, 0 otherwise.
    x = {(v, i): mdl.binary_var(name=f"x_{v}_{i}") for v in G.nodes for i in range(1, k+1)}

    # Variable z representing the maximum color used (1 to k).
    z = mdl.integer_var(lb=1, ub=k, name="z")

    # Objective: minimize z (the maximum color number used).
    mdl.minimize(z)

    # Constraint (2): Each vertex must receive exactly one color.
    for v in G.nodes:
        mdl.add_constraint(mdl.sum(x[(v, i)] for i in range(1, k+1)) == 1, ctname=f"OneColor_{v}")

    # Constraint (3): For every pair of distinct vertices (v,u) and each color i,
    # if the distance between v and u is <= i, they cannot both be assigned color i.
    for i in range(1, k+1):
        for v, u in itertools.combinations(G.nodes, 2):
            try:
                d = nx.shortest_path_length(G, source=v, target=u)
            except nx.NetworkXNoPath:
                continue  # no path => no constraint needed
            if d <= i:
                mdl.add_constraint(x[(v, i)] + x[(u, i)] <= 1, ctname=f"Pack_{v}_{u}_color_{i}")

    # Constraint (4): If a vertex v is assigned color i then i must be <= z.
    for v in G.nodes:
        for i in range(1, k+1):
            mdl.add_constraint(i * x[(v, i)] <= z, ctname=f"MaxColor_{v}_{i}")

    # Solve the model
    solution = mdl.solve(log_output=True)

    if solution:
        print("Solution found!")
        z_val = solution[z]
        print("Minimum z (packing chromatic number):", z_val)

        # Extract color assignment for each vertex.
        color_assignment = {}
        for v in G.nodes:
            for i in range(1, k+1):
                if solution.get_value(x[(v, i)]) > 0.5:
                    color_assignment[v] = i
                    break
        print("Color assignment:", color_assignment)
        return color_assignment, z_val
    else:
        print("No solution found")
        return None, None

# Example usage:
if __name__ == '__main__':
    edge_list = [
        (0, 1), (0, 2), (0, 4),
        (1, 4),
        (2, 1), (2, 4),
        (4, 18),
        (5, 7), (5, 8), (5, 9),
        (6, 5), (6, 9), (6, 11),
        (7, 6), (7, 9),
        (8, 6), (8, 7), (8, 9),
        (10, 11), (10, 12), (10, 13), (10, 14),
        (11, 13), (11, 14),
        (12, 11), (12, 13), (12, 14),
        (13, 14),
        (18, 0), (18, 1), (18, 2), (18, 7)
    ]

    G = nx.Graph()
    G.add_edges_from(edge_list)

    assignment, z_val = solve_packing_coloring_cplex(G)
