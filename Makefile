# Makefile for
# Graph_Algorithms_in_Biological_Pathway_Analysis

VENV_DIR = .venv

.PHONY: env run clean

env:
\tpython -m venv $(VENV_DIR)
\t$(VENV_DIR)/bin/pip install --upgrade pip
\t$(VENV_DIR)/bin/pip install -r requirements.txt

run:
\tpython flow_algorithms.py

clean:
\tfind . -name "__pycache__" -type d -exec rm -rf {} +
\tfind . -name ".ipynb_checkpoints" -type d -exec rm -rf {} +
