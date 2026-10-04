# Graph Coloring Demonstration

A Python program that computes and visualizes three core graph coloring quantities:

- **Chromatic number χ(G)**: the minimum number of colors for a proper vertex coloring
- **Chromatic index χ′(G)**: the minimum number of colors for a proper edge coloring
- **Chromatic polynomial P(G, k)**: the number of proper colorings using k colors

## Real-life model: exam timetabling

Each vertex is an exam subject, and an edge joins two subjects that share at least one student. Colors are time slots.

| Quantity | Meaning in this model |
|---|---|
| χ(G) | Minimum number of exam slots with no clashes |
| χ′(G) | Minimum number of rounds for pairwise coordination meetings |
| P(G, k) | Number of valid timetables with k slots |

## Algorithms

- **Welsh-Powell**: greedy vertex coloring (upper bound)
- **Backtracking**: exact chromatic number
- **Line graph**: chromatic index computed as χ′(G) = χ(L(G))
- **Deletion-contraction**: chromatic polynomial, P(G) = P(G − e) − P(G / e)
- **Brute-force counting**: independent check of the polynomial

## Results for the sample graph

| Quantity | Result |
|---|---|
| Chromatic number | 3 |
| Chromatic index | 4 |
| Chromatic polynomial | k(k−1)²(k−2)³ |
| P(G, 3), P(G, 4), P(G, 5) | 12, 288, 2160 |

The program prints these values and saves a figure (`graph_coloring_output.png`) showing the colored graphs and a chart of P(G, k).

## Requirements

- Python 3
- networkx, sympy, matplotlib

```bash
pip install networkx sympy matplotlib
```

## Usage

```bash
python graph_coloring_demo.py
```

To use your own graph, edit the edge list in `build_graph()`. The exact algorithms are exponential, so keep graphs small (about 10 vertices or fewer).

## Output

<img width="842" height="616" alt="image" src="https://github.com/user-attachments/assets/f38c2d2b-48b9-449b-adb2-727cdac46588" />


## Concepts covered

Clique and degree bounds on χ(G), Brooks' theorem, Vizing's theorem (Δ ≤ χ′ ≤ Δ+1), line graphs, deletion-contraction, and the link between P(G, k) and χ(G).

## Author

[Your Full Name], [Your Registration Number]
