import time

from graph_generators import create_path_connected_k_complete_graphs, create_cycle_connected_k_complete_graphs
from packing_coloring_optimizer import solve_packing_coloring
from utilities import save_to_file, save_coloring_to_file, save_colored_drawing


def main():
    for P_n in range(101):
        start_time = time.time()

        B_n = 2
        K_n = 5
        try:
            G = create_cycle_connected_k_complete_graphs(P_n, B_n, K_n)
        except AssertionError:
            continue

        color_assignment, packing_chromatic_number = solve_packing_coloring(G)

        save_to_file(G, P_n, B_n, K_n)
        save_coloring_to_file(color_assignment, packing_chromatic_number, P_n, B_n, K_n)
        save_colored_drawing(G, color_assignment, packing_chromatic_number, f"graphs/P{P_n}_♦{B_n}_K{K_n}_colored.png")

        print(f"Packing Chromatic Number for P{P_n}_♦{B_n}_K{K_n}: {int(packing_chromatic_number)}"
              f" in {time.time() - start_time:.2f} seconds")


if __name__ == '__main__':
    main()
