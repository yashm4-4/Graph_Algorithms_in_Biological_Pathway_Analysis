# Graph_Algorithms_in_Biological_Pathway_Analysis  
**Graph Algorithms in Biological Pathway Analysis (Glycolysis) — Micropresentation Project**

Contributors:

David Houshangi

Kirk Ehmsen

Christian Fernandez

Yash Maheshvaran

This project explores how classical network flow algorithms can be applied to metabolic pathways to reveal bottlenecks, pathway capacity, and efficient biochemical routes. We focus on the fundamental graph algorithm:

- Ford-Fulkerson Algorithm for finding Max-Flow
    
    - Finding Augmention Paths via BFS

- Analyzing Residual graph to find Min-Cut Edges


Using a simplified metabolic network of glycolysis, we demonstrate how computational tools can be adapted to questions in molecular sciences and systems biology.


# Project Overview

Metabolic pathways can be viewed as directed graphs where nodes represent metabolites and edges represent biochemical reactions. Each reaction carries a certain “capacity” (e.g., maximum flux).

By applying network flow algorithms to these graphs, we can:

1. Estimate maximum possible flux from substrate to product using max-flow

2. Identify rate-limiting steps using min-cut

3. Interpret biological meaning in terms of bottlenecks, efficiency, and pathway structure


This project implements these algorithms on a toy metabolic network and provides visualizations and analysis connecting the results to biological context.

# Repository Structure


Graph_Algorithms_in_Biological_Pathway_Analysis/

├── PythonCode/ glycolysis_graph_analysis.py, glycolysis_network.csv


├── README.md    


├── requirements.txt   


├── Makefile


├── Presentation.pdf (5-minute slide presentation)


├── team_contributions.md               


└── Results / glycolysis.png, glycolysis_maxflow.png, glycolysis_noflow.png

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
python glycolysis_graph_analysis.py
```
Expected output:

- Maximum Flux

- Min-Cut bottleneck

# Results

> ## Glycolysis Graph

<img width="1170" height="3569" alt="glycolysis" src="https://github.com/user-attachments/assets/fddc29bc-368a-44ba-9d79-683347071733" />

  
<img width="1170" height="3569" alt="glycolysis_noflow" src="https://github.com/user-attachments/assets/e0512066-01c5-4fe1-aca2-66970982beb8" />


> ## Max-Flow / Min-Cut

- Computes the maximum possible flux from a source metabolite to a product.

- Identifies the minimum set of reactions whose removal blocks the pathway.

- Biological interpretation: bottlenecks and rate-limiting reactions.
  

<img width="1170" height="3569" alt="glycolysis_maxflow" src="https://github.com/user-attachments/assets/76d9ff5e-8626-45c0-9999-5c4e71c6f660" />



# Biological Relevance - Applications

Our analysis of network flow algorithms provides insight into:

1. Pathway capacity limits(max metabolic rate).

2. Essential reactions (min-cut).

3. Specific Example in Biology: Glycolysis

# Conclusion

Applied to metabolic networks, classical graph algorithms provide insight into biological processes. Through directed, capacity-weighted graph modeling of glycolysis, we identified maximum flux of metabolites, the bottleneck reaction (f6p --> f16bp), and the primary rate-limiting enzyme (PFK). Although it is a simplification of complete Flux Balance Analysis, this technique provides a clear and visual way to observe pathway structure, bottlenecks, and energy efficiency trade-offs. The results obtained correlate well with current biochemistry knowledge. They demonstrate the usefulness of theoretical computer science-derived computational tools when evaluating real-world biological systems. This experiment reiterated the power of algorithmic thought to clarify intricate molecular mechanisms and introduced the potential for higher-level modeling of more extensive metabolic networks.


# Acknowledgments

- This project was developed as part of the Chem 274B – Algorithms & Data Structures in Scientific Computing course at UC Berkeley.

- All algorithms were implemented in Python using open-source libraries.


