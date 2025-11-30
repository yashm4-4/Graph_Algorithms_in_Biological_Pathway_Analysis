# Graph_Algorithms_in_Biological_Pathway_Analysis  
**Graph Algorithms in Biological Pathway Analysis (Glycolysis) — Micropresentation Project**

![Glycolisys](https://github.com/user-attachments/assets/f8ca85ab-8393-4f26-94ca-11e10945395a)

Image: https://www.ncbi.nlm.nih.gov/books/NBK482303/


In this project explores how classical network flow algorithms can be applied to metabolic pathways to reveal bottlenecks, pathway capacity, and efficient biochemical routes. We focus on two fundamental graph algorithms:

- Max-Flow

- Min-Cut

- Shortest Path Algorithms (BFS / Dijkstra)

Using a simplified metabolic network, we demonstrate how computational tools from theoretical computer science can be adapted to questions in molecular sciences and systems biology.


# Project Overview

Metabolic pathways can be viewed as directed graphs where nodes represent metabolites and edges represent biochemical reactions. Each reaction carries a certain “capacity” (e.g., maximum flux) or “cost” (e.g., energy requirement).

By applying network flow algorithms to these graphs, we can:

1. Identify rate-limiting steps using min-cut

2. Estimate maximum possible flux from substrate to product using max-flow

3. Compute the most efficient metabolic route using shortest-path methods

4. Interpret biological meaning in terms of bottlenecks, efficiency, and pathway structure

This project implements these algorithms on a toy metabolic network and provides visualizations and analysis connecting the results to biological context.

# Repository Structure


Graph_Algorithms_in_Biological_Pathway_Analysis/

├── notebook / flow_algorithms.py;  graph_visualization.py
   
├── README.md    

├── README_DATA.md

├── Rubric.md

├── requirements.txt   

├── Makefile

├── Presentation.pdf (5-minute slide presentation)

├── team_contributions.md               

├── Data / glycolysis_network.csv

└── Results / flow_results.txt; glycolysis_network.png

## How to use this repository?

> Step 1: clone the repo
```bash
git clone https://github.com/ktehmsen-berkeley/Graph_Algorithms_in_Biological_Pathway_Analysis.git
```

> Step 2: Install dependencies
```bash
pip install -r requirements.txt
```
This installs:

- networkx

- matplotlib

- pandas

- numpy

> Step 3: Run
```bash
python flow_algorithms.py
```
Expected output:

- Maximum Flux

- Min-Cut bottleneck

- Shortest Path route

> Step 4: Generate pathway visualization
```bash
python graph_visualization.py
```

# Results

## Glycolysis Network Visualization

<img width="3660" height="1929" alt="image" src="https://github.com/user-attachments/assets/1e452f67-1ea9-4548-a577-4632e02878ed" />

Glycolysis Network Flow Analysis

1) Maximum Flux (glucose → pyruvate)
   
   Max-flow value: 60

   Flow distribution by edge:
   
   glucose -> g6p: 60
   
   g6p -> f6p: 60
   
   f6p -> f16bp: 60
   
   f16bp -> g3p: 50
   
   f16bp -> dhap: 10
   
   g3p -> 13bpg: 60
   
   dhap -> g3p: 10
   
   13bpg -> 3pg: 60
   
   3pg -> 2pg: 60
   
   2pg -> pep: 60
   
   pep -> pyruvate: 60

2) Minimum Cut (Bottleneck Reactions)
   
   Min-cut value: 60
   
   Bottleneck edge(s):
   
   f6p -> f16bp

3) Shortest Path (Lowest-Cost Route)
   
   Path: glucose -> g6p -> f6p -> f16bp -> g3p -> 13bpg -> 3pg -> 2pg -> pep -> pyruvate
   
   Total path cost: 7


# Algorithm Summary

> ## Max-Flow / Min-Cut

Computes the maximum possible flux from a source metabolite to a product.

Identifies the minimum set of reactions whose removal blocks the pathway.

Biological interpretation: bottlenecks and rate-limiting reactions.

> ## Shortest Path (Dijkstra/BFS)

Finds the most efficient route between two metabolites.

Edge weights represent energy cost or number of reaction steps.

Biological interpretation: minimal-energy pathways or fastest signaling routes.

More details are provided inside the Jupyter notebook.


# Biological Relevance - Applications

Our analysis of network flow algorithms provides insight into:

1. Pathway capacity limits(max metabolic rate).

2. Essential reactions (min-cut).

3. Alternative Biochemical Paths (redundancy).

4. Energetic Efficiency (minimum distance).

Typically, metabolic models will be built using Flux Balance Analysis (FBA), however, flow algorithms provide a more intuitive structural interpretation and a clear visual representation.

# Conclusion

Applied to metabolic networks, classical graph algorithms provide insight into biological processes. Through directed, capacity-weighted graph modeling of glycolysis, we identified maximum flux, the primary rate-limiting reaction (PFK), and the least energy-consuming metabolic path from glucose to pyruvate. Although it is a simplification of complete Flux Balance Analysis, this technique provides a clear and visual way to observe pathway structure, bottlenecks, and energy efficiency trade-offs. The results obtained correlate well with current biochemistry knowledge. They demonstrate the usefulness of theoretical computer science-derived computational tools when evaluating real-world biological systems. This experiment reiterated the power of algorithmic thought to clarify intricate molecular mechanisms and introduced the potential for higher-level modeling of more extensive metabolic networks.



# Acknowledgments

- This project was developed as part of the Chem 274B – Algorithms & Data Structures in Scientific Computing course at UC Berkeley.

- All algorithms were implemented in Python using open-source libraries.


