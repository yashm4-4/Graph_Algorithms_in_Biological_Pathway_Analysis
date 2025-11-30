# Data Reference: https://www.ncbi.nlm.nih.gov/books/NBK482303/

This folder contains a real biological dataset representing the glycolysis metabolic pathway, formatted as a directed graph suitable for flow-based algorithm analysis. The dataset is provided in:

```
glycolysis_network.csv

```
This file is a simplified but biologically accurate representation of the reaction structure found at `Data Reference: https://www.ncbi.nlm.nih.gov/books/NBK482303/`

# Data Purpose

The Dataset's goal is to demonstrate the applications of Network Flow Algorithms (Max-Flow/Min-Cut and Shortest Path) to actual metabolic pathways, such as Glycolysis which was chosen because it is one of the best-characterized pathways known, there is an identifiable Start (Glucose) and End (Pyruvate), and because of the nature in which it forks and converges lends itself well to Flow Algorithms. The data collected using this dataset also allows for meaningful insight into Pathway Bottlenecks and Pathway Optimal Routes without requiring the use of a complete Genome Scale Model.

# 2. File Contents

The CSV file contains the following columns:

Column Name	Meaning
source	Substrate metabolite for a reaction
target	Product metabolite
capacity	Approximate maximum flux (upper bound) for the reaction, based on typical FBA constraints
cost	Energy cost or gain (simplified): ATP-using steps have positive cost; ATP-producing steps have negative cost
reaction_id	Standard enzyme identifier (e.g., PFK, ALDO, PGK)
