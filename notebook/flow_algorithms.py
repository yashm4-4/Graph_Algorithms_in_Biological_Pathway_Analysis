"""
flow_algorithms.py

This script contains a small demonstration of how classical network flow
algorithms—max-flow/min-cut and shortest-path—can be applied to a simple
toy metabolic pathway. The goal is to show how graph algorithms can give
insight into pathway bottlenecks and efficient biochemical routes.

The graph used here is intentionally small so that the results are easy
to interpret and visualize. All values (capacities and costs) are made-up
but mimic how real metabolic pathways may have limits and energetic costs.
"""

import networkx as nx


def build_metabolic_network():
    """
    Creates and returns a directed graph representing a simplified
    metabolic pathway. Each edge has: 
        - capacity: maximum flux that reaction can carry
        - cost: energy or "difficulty" of the reaction

    Returns
    -------
    G : networkx.DiGraph
        A directed graph containing metabolites as nodes and reactions as edges.
    """
    G = nx.DiGraph()

    # Each tuple: (source, target, attributes):
  
    edges = [
        ('A', 'B', {'capacity': 10, 'cost': 2}),   # A -> B
        ('A', 'C', {'capacity': 5,  'cost': 1}),   # A -> C
        ('B', 'D', {'capacity': 4,  'cost': 2}),   # B -> D
        ('C', 'D', {'capacity': 3,  'cost': 1}),   # C -> D
        ('D', 'E', {'capacity': 6,  'cost': 1}),   # D -> E (final step)
    ]

    # Adding edges to the graph:
  
    for u, v, attr in edges:
        G.add_edge(u, v, **attr)

    return G


def run_max_flow(G):
    """
    Computes maximum flux (max-flow) from metabolite A to metabolite E.

    Parameters
    ----------
    G : networkx.DiGraph
        The metabolic network.

    Returns
    -------
    flow_value : int or float
        Maximum amount of flux that can pass from A to E.
    flow_dict : dict
        Dictionary describing how much flow goes through each edge.
    """
    flow_value, flow_dict = nx.maximum_flow(G, 'A', 'E', capacity='capacity')
    return flow_value, flow_dict


def run_min_cut(G):
    """
    Identifies bottleneck reaction(s) using the minimum cut between A and E.
    The min-cut tells us which reaction(s) limit the total flux.

    Parameters
    ----------
    G : networkx.DiGraph

    Returns
    -------
    cut_value : int or float
        The maximum amount of flux we can push through without breaking constraints.
    cut_edges : list of tuples
        Edges that form the bottleneck (the minimum cut).
    """
    cut_value, (S, T) = nx.minimum_cut(G, 'A', 'E', capacity='capacity')

    # Extracting the edges crossing the cut:
  
    cut_edges = []
    for u in S:
        for v in G[u]:
            if v in T:
                cut_edges.append((u, v))

    return cut_value, cut_edges


def run_shortest_path(G):
    """
    Computes the lowest-cost metabolic route from A to E using Dijkstra's algorithm.

    Parameters
    ----------
    G : networkx.DiGraph

    Returns
    -------
    path : list
        Ordered list of metabolites representing the optimal route.
    total_cost : int or float
        Sum of costs along the shortest path.
    """
    path = nx.dijkstra_path(G, 'A', 'E', weight='cost')
    total_cost = nx.dijkstra_path_length(G, 'A', 'E', weight='cost')
    return path, total_cost


def main():
    """
    Runs all analyses on the toy metabolic network and prints results in the terminal.
    This allows the script to be run without using Jupyter Notebook and makes the
    repository easier to test.
    """
    print("Metabolic Pathway Flow Analysis ")

    # Building the small metabolic network:
  
    G = build_metabolic_network()

    # Max-Flow:
  
    flow_value, flow_dist = run_max_flow(G)
    print("Maximum Flux from A → E:", flow_value)
    print("Flow Distribution Across Reactions:")
    print(flow_dist)

    # Min-Cut:
  
    cut_value, cut_edges = run_min_cut(G)
    print("\nMin-Cut Value (Bottleneck Capacity):", cut_value)
    print("Bottleneck Reaction(s):", cut_edges)

    # Shortest Path:
  
    best_path, best_cost = run_shortest_path(G)
    print("\nLowest-Cost Metabolic Route from A → E:", best_path)
    print("Total Route Cost:", best_cost)



if __name__ == "__main__":
    main()

