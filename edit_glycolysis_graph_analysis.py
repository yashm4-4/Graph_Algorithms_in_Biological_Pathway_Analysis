import networkx as nx
import pandas as pd
from collections import deque
import copy
import matplotlib.pyplot as plt

def network_graph(csv_path, return_png = False, png_filename = None, title = None, edge_labels = False):
    """
    Build a directed graph from the CSV file
    """
    df = pd.read_csv(csv_path)
    G = nx.DiGraph()

    for _, reaction in df.iterrows():  #add nodes and edges
        G.add_edge(
            reaction["source"],
            reaction["target"],
            enzyme=reaction["enzyme"],
            capacity=float(reaction["capacity"]),
            flow=0.0   # initialize flow as 0 on all edges
        )

    if return_png == True:
        pos = nx.kamada_kawai_layout(G, scale=8.0)
        plt.figure(figsize=(4, 12))
        plt.title(title)
        nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=800, arrows=True, arrowsize=20)
        if edge_labels == True:
            edge_labels = {(u, v): f"{G[u][v]['flow']}/{G[u][v]['capacity']}\n{G[u][v]['enzyme']}" for u, v in G.edges()}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="black", font_size=8)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="black")
        plt.tight_layout()
        plt.savefig(png_filename, format="png", dpi=300,bbox_inches='tight')

    return G


def plot_graph(G, png_filename = None, title = None, edge_labels = False):
    pos = nx.kamada_kawai_layout(G, scale=8.0)
    plt.figure(figsize=(4, 12))
    plt.title(title)
    nx.draw(G, pos, with_labels=True, node_color="yellow", node_size=800, arrows=True, arrowsize=20)
    if edge_labels == True:
        edge_labels = {(u, v): f"{G[u][v]['flow']}/{G[u][v]['capacity']}\n{G[u][v]['enzyme']}" for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="black", font_size=8)
    plt.tight_layout()
    plt.savefig(png_filename, format="png", dpi=300, bbox_inches='tight')
    

def bfs_augmenting_path(G, source, sink):
    """
    Find an augmenting path using breadth-first search
    Record traversed nodes
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
                    return traversal  # augmenting path found

    return None  # no augmenting path exists


def ff_max(G, source, sink):
    """
    Ford Fulkerson to find max flow in a network
    and  accordingly update the corresponding flows on each edge
    """
    max_flow = 0.0  # accumulate total flow from source to sink
    G_modified = copy.deepcopy(G)
    
    while True:
        augmenting_path = bfs_augmenting_path(G_modified, source, sink)  
        if augmenting_path is None:
            break  # no more augmenting paths

        # Walk backward through the augmenting path - from the sink to the source - to reconstruct the augmenting path
        path = []  # accumulate edge pairs
        start_node = sink
        while augmenting_path[start_node] is not None:
            current_node = augmenting_path[start_node]
            path.append((current_node, start_node))
            start_node = current_node
        path.reverse()  # augmenting path, from source to sink

        # calculate bottleneck capacity on this path
        bottleneck = float("inf")
        for current_node, start_node in path:
            residual = G_modified[current_node][start_node]["capacity"] - G_modified[current_node][start_node]["flow"]  
            bottleneck = min(bottleneck, residual)

        # augment flow along the path
        for current_node, start_node in path:
            G_modified[current_node][start_node]["flow"] += bottleneck  # update flows on graph object

        max_flow += bottleneck

    return max_flow, G_modified


def min_cut(G, source):
    """
    Min cut after max-flow computation - path where total network capacity is minimzed
    """
    visited = set()
    queue = deque([source])
    visited.add(source)

    # BFS
    while queue:
        current_node = queue.popleft()
        for next_node in G[current_node]:
            residual = G[current_node][next_node]["capacity"] - G[current_node][next_node]["flow"]
            if residual > 0 and next_node not in visited:
                visited.add(next_node)
                queue.append(next_node)

    reach = visited  # nodes that can be reached from the source node
    no_reach = set(G.nodes()) - reach  # nodes that cannot be reached from the source node

    # edges crossing from reach to no_reach; these are min-cut edges aka no more flow can go through them
    mincut_edges = [(current_node, next_node) for current_node in reach for next_node in G[current_node] if next_node in no_reach]

    rate_limiting_enzymes = [G[u][v]['enzyme'] for u, v in mincut_edges]

    return reach, no_reach, mincut_edges, rate_limiting_enzymes


def main():
    G = network_graph("glycolysis_network.csv", return_png=True, png_filename="glycolysis.png",
                      title="Glycolysis") 
    G = network_graph("glycolysis_network.csv", return_png=True, png_filename="glycolysis_noflow.png", 
                      title="Glycolysis, Reaction Capacities (No Flow)", edge_labels=True) 

    maxflow, G = ff_max(G, "glucose", "pyruvate")

    plot_graph(G, png_filename="glycolysis_maxflow.png", title="Glycolysis, Reaction Capacities (Max Flow)", edge_labels=True)

    print("\nMaximum flux:", maxflow)

    print("\nFlow on each edge:")
    for u, v in G.edges():
        print(f"  {u} -> {v}, {G[u][v]['flow']} / {G[u][v]['capacity']}")

    print("\nMin cut (bottleneck) reactions:")
    reach, no_reach, cut_edges, rate_limiting_enzymes = min_cut(G, "glucose")
    print("Pre-bottleneck node(s):", reach)
    print("Post-bottleneck node(s):", no_reach)
    print("Min cut (bottleneck) reaction(s):", cut_edges)
    print("Rate-limiting enzyme(s):", rate_limiting_enzymes)

if __name__ == "__main__":
    main()
