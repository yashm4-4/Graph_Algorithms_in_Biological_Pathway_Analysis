# Data Reference: https://www.ncbi.nlm.nih.gov/books/NBK482303/

This folder contains a real biological dataset representing the glycolysis metabolic pathway, formatted as a directed graph suitable for flow-based algorithm analysis. The dataset is provided in:

```
glycolysis_network.csv

```
This file is a simplified but biologically accurate representation of the reaction structure found at `Data Reference: https://www.ncbi.nlm.nih.gov/books/NBK482303/`

# Data Purpose

The Dataset's goal is to demonstrate the applications of Network Flow Algorithms (Max-Flow/Min-Cut and Shortest Path) to actual metabolic pathways, such as Glycolysis which was chosen because it is one of the best-characterized pathways known, there is an identifiable Start (Glucose) and End (Pyruvate), and because of the nature in which it forks and converges lends itself well to Flow Algorithms. The data collected using this dataset also allows for meaningful insight into Pathway Bottlenecks and Pathway Optimal Routes without requiring the use of a complete Genome Scale Model.

# Data Contents

The CSV file contains the following columns:

Column Name	Meaning
source	Substrate metabolite for a reaction
target	Product metabolite
capacity	Approximate maximum flux (upper bound) for the reaction, based on typical FBA constraints
cost	Energy cost or gain (simplified): ATP-using steps have positive cost; ATP-producing steps have negative cost
reaction_id	Standard enzyme identifier (e.g., PFK, ALDO, PGK)


  source   |  target     |  capacity  |  cost  |  reaction_id
  ---------|-------------|------------|--------|--------------         
  glucose  |   g6p       |    100     |    2   |    HEX1
  g6p      |   f6p       |    80      |    1   |    PGI
  f6p      |   f16bp     |    60      |    2   |    PFK
  f16bp    |   g3p       |    50      |    1   |    ALDO
  f16bp    |   dhap      |    50      |    1   |    ALDO
  dhap     |   g3p       |    40      |    1   |    TPI
  g3p      |   13bpg     |    70      |    1   |    GAPD
  13bpg    |   3pg       |    70      |   -1   |    PGK
  3pg      |   2pg       |    90      |    1   |    PGM
  2pg      |   pep       |    85      |    1   |    ENO
  pep      |   pyruvate  |   100      |   -1   |    PYK

**These values allow the pathway to be represented as a directed weighted graph, where “capacity” is used for max-flow/min-cut and “cost” is used for shortest-path algorithms.**


# Overview of Glycolysis

The biochemical reactions of glycolysis convert glucose directly into pyruvate. The biological characteristics of glycolysis that are important to our research include:

1) Glycolytic pathway ATP costs (ATP Investment):
   
- Hexokinase and Phosphofructokinase are enzymes that consume ATP; therefore, they have the greatest ATP costs of the glycolytic pathway.
  
2) Branching Point
   
- Fructose-1,6-bisphosphate can be converted into two different products (G3P or DHAP).
  
3) Energy Payoff Phase (Phase)
   
- Phosphoglycerate Kinase and Pyruvate Kinase produce ATP; therefore, they have low or negative ATP costs.
  
4) Convergence Point:
   
- The branches of the glycolytic pathway merge at similar points to produce pyruvate.

The analysis of this model of glycolysis clearly shows that glycolysis can be used to demonstrate bottlenecks and optimal routes.

# How This Dataset Is Used in the Project

The notebook performs:

## Max-Flow Analysis

- Computes the maximum possible flux from glucose to pyruvate

- Identifies the reaction that limits throughput (the bottleneck)

## Minimum Cut

- Detects essential reactions whose removal disrupts glycolysis

## Shortest Path Analysis

- Finds the lowest-energy metabolic route

- Shows how the cell might minimize ATP usage or maximize ATP yield

This demonstrates the practical usefulness of classical graph algorithms in biological pathway analysis.
