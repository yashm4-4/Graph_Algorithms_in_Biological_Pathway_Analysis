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
    """
    plt.figure(figsize=(12, 6))

    manual_pos = {
        "glucose": (0, 0),
        "g6p": (1, 0),
        "f6p": (2, 0.4),
        "f16bp": (3, 0),
        "dhap": (3.2, -0.7),
        "g3p": (4, 0),
        "13bpg": (5, 0.2),
        "3pg": (6, 0.4),
        "2pg": (7, 0.6),
        "pep": (8, 0.8),
        "pyruvate": (9, 1.0),
    }

    # Fallback: use spring_layout for any nodes we didn't explicitly place:
   
    spring_pos = nx.spring_layout(G, seed=1)
    pos = {}
    for n in G.nodes():
        pos[n] = manual_pos.get(n, spring_pos[n])

    # Draw nodes and edges:
   
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="#ADD8E6",
        node_size=2000,
        arrowsize=20,
        font_size=12,
        linewidths=1.0,
        edgecolors="black",
    )

    # Build edge labels that show enzyme and capacity:
   
    edge_labels = {}
    for u, v, data in G.edges(data=True):
        cap = data.get("capacity", "")
        rid = data.get("reaction_id", "")
        edge_labels[(u, v)] = f"{rid}\ncap={cap}"

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=9,
        label_pos=0.5,  
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7),
    )

    plt.title("Glycolysis Network (Metabolites and Reactions)", fontsize=14)
    plt.axis("off")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
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

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Glycolysis Network Flow Analysis\n")

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

    # Build graph from CSV:
   
    G = build_metabolic_network()

    # Compute results using the shared helper functions:
   
    flow_value, flow_dist = run_max_flow(G)
    cut_value, cut_edges = run_min_cut(G)
    best_path, best_cost = run_shortest_path(G)

    # Save visualization and summary:
   
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
