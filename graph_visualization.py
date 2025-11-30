"""
graph_visualization.py

This script loads the glycolysis network from data/glycolysis_network.csv,
reuses the flow algorithms from flow_algorithms.py, and:

1. Computes:
   - max-flow (glucose → pyruvate)
   - min-cut (bottleneck reactions)
   - shortest path (lowest-cost route)

2. Saves:
   - A text summary of the results to Results/flow_results.txt
   - A PNG image of the metabolic graph to Results/glycolysis_network.png

This script is intended to generate a single, clean figure and a small
results file that can be included in the final report or slides.
"""

import os
import matplotlib.pyplot as plt
import networkx as nx

from flow_algorithms import (
    build_metabolic_network,
    run_max_flow,
    run_min_cut,
    run_shortest_path,
)


def ensure_results_dir(path="Results"):
    """
    Creates the Results directory if it does not already exist.

    Parameters
    ----------
    path : str
        Name of the results folder to create.
    """
    os.makedirs(path, exist_ok=True)


def draw_glycolysis_graph(G, output_path="Results/glycolysis_network.png"):
    """
    Draws the glycolysis network using NetworkX and Matplotlib and saves
    the figure as a PNG.

    Nodes are metabolites and edges are reactions. Edge labels show
    the capacity and reaction_id (enzyme).

    Parameters
    ----------
    G : networkx.DiGraph
        Metabolic network to visualize.
    output_path : str
        Path where the PNG file will be saved.
    """
    plt.figure(figsize=(8, 6))

    # Use a spring layout for a clean layout; seed for reproducibility
    pos = nx.spring_layout(G, seed=1)

    # Draw nodes and edges
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="#ADD8E6",
        node_size=1500,
        arrowsize=20,
        font_size=10,
    )

    # Build edge labels that show capacity and reaction_id
    edge_labels = {}
    for u, v, data in G.edges(data=True):
        cap = data.get("capacity", "")
        rid = data.get("reaction_id", "")
        edge_labels[(u, v)] = f"{rid}\ncap={cap}"

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Glycolysis Network (Metabolites and Reactions)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def write_results_summary(
    flow_value,
    flow_dist,
    cut_value,
    cut_edges,
    best_path,
    best_cost,
    output_path="Results/flow_results.txt",
):
    """
    Writes a short, human-readable summary of the flow analysis to a
    text file.

    Parameters
    ----------
    flow_value : float
        Maximum flux from glucose to pyruvate.
    flow_dist : dict
        Flow distribution across edges.
    cut_value : float
        Capacity of the minimum cut.
    cut_edges : list of tuple
        List of bottleneck edges (u, v).
    best_path : list of str
        Shortest (lowest-cost) metabolic route.
    best_cost : float
        Total cost of the shortest path.
    output_path : str
        File path where the summary should be written.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Glycolysis Network Flow Analysis\n")
        f.write("================================\n\n")

        f.write("1) Maximum Flux (glucose → pyruvate)\n")
        f.write(f"   Max-flow value: {flow_value}\n\n")

        f.write("   Flow distribution by edge:\n")
        for u, nbrs in flow_dist.items():
            for v, val in nbrs.items():
                if val > 0:
                    f.write(f"   {u} -> {v}: {val}\n")
        f.write("\n")

        f.write("2) Minimum Cut (Bottleneck Reactions)\n")
        f.write(f"   Min-cut value: {cut_value}\n")
        f.write("   Bottleneck edge(s):\n")
        for u, v in cut_edges:
            f.write(f"   {u} -> {v}\n")
        f.write("\n")

        f.write("3) Shortest Path (Lowest-Cost Route)\n")
        f.write("   Path: " + " -> ".join(best_path) + "\n")
        f.write(f"   Total path cost: {best_cost}\n")


def main():
    """
    Main entry point for the script.

    This function:
      - builds the metabolic network,
      - runs the three analyses,
      - saves a PNG of the graph,
      - saves a text summary of the results.
    """
    ensure_results_dir("Results")

    # Build graph from CSV (same as in flow_algorithms.py)
    G = build_metabolic_network()

    # Compute results using the shared helper functions
    flow_value, flow_dist = run_max_flow(G)
    cut_value, cut_edges = run_min_cut(G)
    best_path, best_cost = run_shortest_path(G)

    # Save visualization and summary
    draw_glycolysis_graph(G, output_path="Results/glycolysis_network.png")
    write_results_summary(
        flow_value,
        flow_dist,
        cut_value,
        cut_edges,
        best_path,
        best_cost,
        output_path="Results/flow_results.txt",
    )

    print("Graph visualization saved to: Results/glycolysis_network.png")
    print("Flow analysis summary saved to: Results/flow_results.txt")


if __name__ == "__main__":
    main()
