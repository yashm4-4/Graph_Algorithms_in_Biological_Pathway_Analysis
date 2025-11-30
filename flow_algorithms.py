"""
flow_algorithms.py

This script shows how classical network flow algorithms
(max-flow / min-cut and shortest-path) can be applied to
a real biological pathway: glycolysis.

The graph is built from a small dataset stored in
data/glycolysis_network.csv, where each row represents
a reaction step:

    source metabolite -> target metabolite

Each edge has:
    - capacity: an approximate upper bound on flux
    - cost: a simple energy-related score

The goal is to see how these algorithms can highlight
bottlenecks, maximum pathway throughput, and efficient
routes from glucose to pyruvate.
"""

import networkx as nx
import pandas as pd


def build_metabolic_network(csv_path="data/glycolysis_network.csv"):
    """
    Creates and returns a directed graph representing a simplified
    glycolysis pathway. The reactions are loaded from a CSV file.

    The CSV file is expected to have the following columns:
        - source: substrate metabolite
        - target: product metabolite
        - capacity: maximum flux the reaction can carry
        - cost: energy or "difficulty" of the reaction
        - reaction_id: enzyme abbreviation (for reference)

    Parameters
    ----------
    csv_path : str
        Path to the CSV file that stores the glycolysis network.

    Returns
    -------
    G : networkx.DiGraph
        A directed graph where nodes are metabolites and edges are reactions.
    """
    df = pd.read_csv(csv_path)

    G = nx.DiGraph()

    # Add each reaction as a directed edge with attributes.
    for _, row in df.iterrows():
        G.add_edge(
            row["source"],
            row["target"],
            capacity=row["capacity"],
            cost=row["cost"],
            reaction_id=row["reaction_id"],
        )

    return G


def run_max_flow(G, source="glucose", sink="pyruvate"):
    """
    Computes maximum flux (max-flow) from the source metabolite
    to the sink metabolite.

    Parameters
    ----------
    G : networkx.DiGraph
        The metabolic network.
    source : str
        Name of the source metabolite (e.g., "glucose").
    sink : str
        Name of the sink metabolite (e.g., "pyruvate").

    Returns
    -------
    flow_value : int or float
        Maximum amount of flux that can pass from source to sink.
    flow_dict : dict
        Dictionary describing how much flow goes through each edge.
    """
    flow_value, flow_dict = nx.maximum_flow(G, source, sink, capacity="capacity")
    return flow_value, flow_dict


def run_min_cut(G, source="glucose", sink="pyruvate"):
    """
    Identifies bottleneck reaction(s) using the minimum cut
    between the source and sink metabolites.

    The min-cut tells us which reaction(s) limit the total flux.

    Parameters
    ----------
    G : networkx.DiGraph
        The metabolic network.
    source : str
        Name of the source metabolite.
    sink : str
        Name of the sink metabolite.

    Returns
    -------
    cut_value : int or float
        The maximum amount of flux we can push through without
        violating any capacity constraints.
    cut_edges : list of tuples
        Edges (u, v) that form the bottleneck (the minimum cut).
    """
    cut_value, (S, T) = nx.minimum_cut(G, source, sink, capacity="capacity")

    # Extract the edges crossing the cut from S to T.
    cut_edges = []
    for u in S:
        for v in G[u]:
            if v in T:
                cut_edges.append((u, v))

    return cut_value, cut_edges


def run_shortest_path(G, source="glucose", sink="pyruvate"):
    """
    Computes the lowest-cost metabolic route from source to sink
    using Dijkstra's algorithm.

    Parameters
    ----------
    G : networkx.DiGraph
        The metabolic network.
    source : str
        Name of the source metabolite.
    sink : str
        Name of the sink metabolite.

    Returns
    -------
    path : list of str
        Ordered list of metabolites representing the optimal route.
    total_cost : int or float
        Sum of costs along the shortest path.
    """
    path = nx.dijkstra_path(G, source, sink, weight="cost")
    total_cost = nx.dijkstra_path_length(G, source, sink, weight="cost")
    return path, total_cost


def main():
    """
    Runs all analyses on the glycolysis network and prints
    the results to the terminal. This makes it easy to test
    the repository without opening a Jupyter notebook.
    """
    print("\n--- Glycolysis Flow Analysis (Glucose → Pyruvate) ---\n")

    # Build the metabolic network from the CSV file.
    G = build_metabolic_network()

    # 1. Max-Flow: how much flux can we push from glucose to pyruvate?
    flow_value, flow_dist = run_max_flow(G)
    print("Maximum Flux from glucose → pyruvate:", flow_value)
    print("\nFlow Distribution Across Reactions:")
    print(flow_dist)

    # 2. Min-Cut: which reactions form the bottleneck?
    cut_value, cut_edges = run_min_cut(G)
    print("\nMin-Cut Value (Bottleneck Capacity):", cut_value)
    print("Bottleneck Reaction(s):", cut_edges)

    # 3. Shortest Path: which route is lowest-cost (energy-wise)?
    best_path, best_cost = run_shortest_path(G)
    print("\nLowest-Cost Metabolic Route from glucose → pyruvate:")
    print("Path:", best_path)
    print("Total Route Cost:", best_cost)



if __name__ == "__main__":
    main()
