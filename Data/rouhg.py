import networkx as nx
import pandas as pd
from collections import deque
import copy
import matplotlib.pyplot as plt

def network_graph(csv_path, return_png = False, png_filename = None):
    """
    Build a directed graph from the metabolic CSV file,
    with capacity constraints on edges.
    """
    df = pd.read_csv(csv_path)
    G = nx.DiGraph()

    for _, reaction in df.iterrows():  # add nodes and edges
        G.add_edge(
            reaction["source"],
            reaction["target"],
            enzyme=reaction["enzyme"],
            capacity=float(reaction["capacity"]),
            flow=0.0   # initialize flow as 0 on all edges
        )

    if return_png == True:
        # pos = nx.spring_layout(G, k=2.0, iterations=100)
        pos = nx.kamada_kawai_layout(G, scale=8.0)
        # edge_labels = {(u, v): f"{G[u][v]['flow']}/{G[u][v]['capacity']}\n{G[u][v]['enzyme']}" for u, v in G.edges()}
        edge_labels = {(u, v): f"{G[u][v]['enzyme']}" for u, v in G.edges()}
        plt.figure(figsize=(4, 12))
        nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=800, arrows=True, arrowsize=20)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="black")
        plt.savefig(png_filename, format="png", dpi=300)

    return G


def bfs_augmenting_path(G, source, sink):
    """
    Find an augmenting path using breadth-first search over residual graph.
    Visit nodes in FIFO (first-in, first-out) order, traversing only edges
    with positive residual capacity (capacity - flow > 0).  Record node
    predecessors so that augmenting path can be reconstructed once sink
    is reached.
    """
    visited = set()
    queue = deque([source])
    traversal = {source: None}  # enables path reconstruction
    visited.add(source)

    while queue:
        current_node = queue.popleft()  # while there are nodes to explore, the first node we added to the queue is
                                        # the first one to traverse

        for next_node in G[current_node]:
            cap = G[current_node][next_node]["capacity"] - G[current_node][next_node]["flow"]  # residual capacity: how much flow this edge can still sustain

            if cap > 0 and next_node not in visited:  # only visit nodes connected to edges with residual capacity
                visited.add(next_node)
                traversal[next_node] = current_node
                queue.append(next_node)

                if next_node == sink:
                    return traversal  # found augmenting path!

    return None  # no augmenting path exists


def edmonds_karp_maxflow(G, source, sink):
    """
    Ford–Fulkerson algorithm to (1) find max-flow in a network
    and (2) update corresponding flows on each edge.
    Uses breadth-first search traversal across connected nodes
    (i.e., Edmonds–Karp algorithm).
    Parameters
    ----------
    G : graph object; G[current_node][next_node] is a dictionary key with (capacity, flow, enzyme) value
    source : starting node (S) in network
    sink : ending node (T) in network
    Returns
    -------
    max-flow : maximum network flow (flux) value, and flow on each edge
    G_updated : graph object with updated flow values on each edge
    """
    max_flow = 0.0  # accumulate total flow from source to sink
    G_modified = copy.deepcopy(G)
    
    while True:
        traversal = bfs_augmenting_path(G_modified, source, sink)  
        if traversal is None:
            break  # no more augmenting paths → done

        # Walk traversal backward (from sink to source), to reconstruct augmenting path
        path = []  # accumulate edge pairs
        next_node = sink
        while traversal[next_node] is not None:
            current_node = traversal[next_node]
            path.append((current_node, next_node))
            next_node = current_node
        path.reverse()

        # Calculate bottleneck capacity on this path
        bottleneck = float("inf")
        for current_node, next_node in path:
            residual = G_modified[current_node][next_node]["capacity"] - G_modified[current_node][next_node]["flow"]  
            bottleneck = min(bottleneck, residual)

        # Augment flow along the path
        for current_node, next_node in path:
            G_modified[current_node][next_node]["flow"] += bottleneck  # update flows on graph object

        max_flow += bottleneck

    return max_flow, G_modified


def min_cut(G, source):
    """
    Identify the min-cut after max-flow computation.
    This is the path across which the total network capacity from S-T
    is minimized.
    Parameters
    ----------
    G : graph object; G[current_node][next_node] is a dictionary key with (capacity, flow) value
    source : starting node (S) in network
    Returns
    -------
    S : node set reachable from source
    T : node set not reachable from source
    edges
    """
    visited = set()
    queue = deque([source])
    visited.add(source)

    # BFS on residual network
    while queue:
        current_node = queue.popleft()
        for next_node in G[current_node]:
            residual = G[current_node][next_node]["capacity"] - G[current_node][next_node]["flow"]
            if residual > 0 and next_node not in visited:
                visited.add(next_node)
                queue.append(next_node)

    S = visited  # nodes that can be recached from the source node
    T = set(G.nodes()) - S  # nodes that cannot be reached from the source node

    # edges crossing from S to T; these are min-cut edges (no more flow can go through them)
    mincut_edges = [(current_node, next_node) for current_node in S for next_node in G[current_node] if next_node in T]

    rate_limiting_enzymes = [G[u][v]['enzyme'] for u, v in mincut_edges]

    return S, T, mincut_edges, rate_limiting_enzymes


def main():
    G = network_graph("glycolysis_network.csv", return_png=True, png_filename="glycolysis.png") 

    maxflow, G = edmonds_karp_maxflow(G, "glucose", "pyruvate")
    print("\n=== MAX FLOW ===")
    print("Maximum glycolytic flux:", maxflow)

    print("\n=== FLOW ON EACH EDGE ===")
    for u, v in G.edges():
        print(f"{u} -> {v} : flow = {G[u][v]['flow']} / {G[u][v]['capacity']}")

    print("\n=== MIN CUT ===")
    S, T, cut_edges, rate_limiting_enzymes = min_cut(G, "glucose")
    print("S (reachable):", S)
    print("T (unreachable):", T)
    print("Min-cut edges:", cut_edges)
    print("Rate-limiting enzymes:", rate_limiting_enzymes)


if __name__ == "__main__":
    main()
