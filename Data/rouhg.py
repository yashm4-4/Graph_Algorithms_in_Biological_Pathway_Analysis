import networkx as nx
import pandas as pd
from collections import deque

def build_graph(csv_path):
    """
    Build a directed graph from the metabolic CSV file.
    Ignores cost, includes only capacities.
    For glycolysis (unidirectional pathway), no backward edges needed.
    """
    df = pd.read_csv(csv_path)
    G = nx.DiGraph()

    for _, r in df.iterrows():
        G.add_edge(
            r["source"],
            r["target"],
            capacity=float(r["capacity"]),
            flow=0.0   # initialize flow on every edge
        )

    return G


def bfs_find_path(G, source, sink):
    """
    BFS on the *residual graph* to find an augmenting path.
    Returns parent dictionary mapping each node to its predecessor.
    """
    visited = set()
    queue = deque([source])
    parent = {source: None}
    visited.add(source)

    while queue:
        u = queue.popleft()

        for v in G[u]:
            cap = G[u][v]["capacity"] - G[u][v]["flow"]  # residual capacity

            if cap > 0 and v not in visited:
                visited.add(v)
                parent[v] = u
                queue.append(v)

                if v == sink:
                    return parent  # found augmenting path!

    return None  # no augmenting path exists


def edmonds_karp_maxflow(G, source, sink):
    """
    Manual implementation of Ford–Fulkerson using BFS (Edmonds–Karp).
    Returns max-flow value and the final flow on each edge.
    """
    max_flow = 0.0

    while True:
        parent = bfs_find_path(G, source, sink)
        if parent is None:
            break  # no more augmenting paths → done

        # Reconstruct the augmenting path
        path = []
        v = sink
        while parent[v] is not None:
            u = parent[v]
            path.append((u, v))
            v = u
        path.reverse()

        # Find bottleneck capacity on this path
        bottleneck = float("inf")
        for u, v in path:
            residual = G[u][v]["capacity"] - G[u][v]["flow"]
            bottleneck = min(bottleneck, residual)

        # Augment flow along the path
        for u, v in path:
            G[u][v]["flow"] += bottleneck

        max_flow += bottleneck

    return max_flow, G


def extract_min_cut(G, source):
    """
    After max-flow completes, the min-cut is found by:
    - BFS in the residual graph from source
    - Nodes reachable = S
    - Edges S → T in original graph = min-cut edges
    """
    visited = set()
    queue = deque([source])
    visited.add(source)

    # BFS on residual network
    while queue:
        u = queue.popleft()
        for v in G[u]:
            residual = G[u][v]["capacity"] - G[u][v]["flow"]
            if residual > 0 and v not in visited:
                visited.add(v)
                queue.append(v)

    S = visited
    T = set(G.nodes()) - S

    # edges crossing from S to T
    cut_edges = [(u, v) for u in S for v in G[u] if v in T]

    return S, T, cut_edges


def main():
    G = build_graph("glycolysis_network.csv")

    maxflow, G = edmonds_karp_maxflow(G, "glucose", "pyruvate")
    print("\n=== MAX FLOW ===")
    print("Maximum glycolytic flux:", maxflow)

    print("\n=== FLOW ON EACH EDGE ===")
    for u, v in G.edges():
        print(f"{u} -> {v} : flow = {G[u][v]['flow']} / {G[u][v]['capacity']}")

    print("\n=== MIN CUT ===")
    S, T, cut_edges = extract_min_cut(G, "glucose")
    print("S (reachable):", S)
    print("T (unreachable):", T)
    print("Min-cut edges:", cut_edges)


if __name__ == "__main__":
    main()
