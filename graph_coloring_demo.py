"""
Graph Coloring Demonstration
============================
Covers: Chromatic Number, Chromatic Index, Chromatic Polynomial.

Real-life model: exam timetabling.
  - Vertices = subjects (A..F)
  - Edge     = two subjects share at least one student (cannot be in same slot)
  - Colors   = exam time slots

Run:  python graph_coloring_demo.py
Needs: networkx, sympy, matplotlib
"""
import itertools
import networkx as nx
import sympy as sp
import matplotlib
matplotlib.use("Agg")          # remove this line if you want a pop-up window
import matplotlib.pyplot as plt

PALETTE = ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4",
           "#42d4f4", "#f032e6", "#bfef45", "#9a6324", "#808000"]
k = sp.Symbol("k")


# ---------------------------------------------------------------- 1. GRAPH
def build_graph():
    G = nx.Graph()
    G.add_edges_from([("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"),
                      ("C", "D"), ("D", "E"), ("D", "F"), ("E", "F")])
    return G


# ------------------------------------------------- 2. CHROMATIC NUMBER chi(G)
def welsh_powell(G):
    """Greedy heuristic: colour vertices in decreasing order of degree."""
    colour = {}
    for v in sorted(G.nodes, key=lambda x: -G.degree(x)):
        used = {colour[u] for u in G[v] if u in colour}
        c = 0
        while c in used:
            c += 1
        colour[v] = c
    return colour


def is_k_colourable(G, k_colours):
    """Exact backtracking test: can G be properly coloured with k colours?"""
    nodes = sorted(G.nodes, key=lambda x: -G.degree(x))
    colour = {}

    def solve(i):
        if i == len(nodes):
            return True
        v = nodes[i]
        for c in range(k_colours):
            if all(colour.get(u) != c for u in G[v]):
                colour[v] = c
                if solve(i + 1):
                    return True
                del colour[v]
        return False

    return (dict(colour) if solve(0) else None)


def chromatic_number(G):
    """Smallest k for which a proper colouring exists (exact)."""
    for kk in range(1, G.number_of_nodes() + 1):
        col = is_k_colourable(G, kk)
        if col is not None:
            return kk, col


# ------------------------------------------------- 3. CHROMATIC INDEX chi'(G)
def chromatic_index(G):
    """Edge colouring = vertex colouring of the line graph L(G)."""
    L = nx.line_graph(G)
    kk, col = chromatic_number(L)
    return kk, col, L


# --------------------------------------------- 4. CHROMATIC POLYNOMIAL P(G,k)
def chromatic_polynomial(G):
    """Deletion-contraction:  P(G) = P(G - e) - P(G / e).
    Base case: graph with no edges on n vertices -> k^n."""
    if G.number_of_edges() == 0:
        return k ** G.number_of_nodes()
    u, v = next(iter(G.edges))
    G_del = G.copy()
    G_del.remove_edge(u, v)
    G_con = nx.contracted_nodes(G, u, v, self_loops=False)
    return sp.expand(chromatic_polynomial(G_del) - chromatic_polynomial(G_con))


def brute_force_count(G, kk):
    """Count proper colourings with kk colours directly (to verify P(G,k))."""
    nodes = list(G.nodes)
    count = 0
    for assign in itertools.product(range(kk), repeat=len(nodes)):
        c = dict(zip(nodes, assign))
        if all(c[a] != c[b] for a, b in G.edges):
            count += 1
    return count


# ------------------------------------------------------------ 5. VISUALS
def draw_vertex_colouring(G, col, pos, ax, title):
    ax.set_title(title, fontsize=11)
    nx.draw(G, pos, ax=ax, with_labels=True, font_weight="bold",
            node_color=[PALETTE[col[v]] for v in G.nodes],
            node_size=900, edge_color="#555", width=2, font_color="white")


def draw_edge_colouring(G, ecol, pos, ax, title):
    ax.set_title(title, fontsize=11)
    edge_colours = []
    for e in G.edges:
        c = ecol[e] if e in ecol else ecol[(e[1], e[0])]
        edge_colours.append(PALETTE[c])
    nx.draw(G, pos, ax=ax, with_labels=True, font_weight="bold",
            node_color="#dddddd", node_size=900, edge_color=edge_colours,
            width=4)


def draw_polynomial_chart(poly, G, ax):
    xs = list(range(0, 6))
    ys = [int(poly.subs(k, x)) for x in xs]
    ax.bar(xs, ys, color="#4363d8")
    for x, y in zip(xs, ys):
        ax.text(x, y, str(y), ha="center", va="bottom", fontsize=9)
    ax.set_xlabel("number of colours (time slots) k")
    ax.set_ylabel("P(G, k) = valid timetables")
    ax.set_title("Chromatic polynomial: number of valid colourings")


# ------------------------------------------------------------------ MAIN
def main():
    G = build_graph()
    pos = nx.spring_layout(G, seed=7)
    n, m = G.number_of_nodes(), G.number_of_edges()
    max_deg = max(d for _, d in G.degree)

    print("=" * 60)
    print("GRAPH:  vertices =", sorted(G.nodes))
    print("        edges    =", sorted(G.edges))
    print(f"        n = {n}, m = {m}, max degree = {max_deg}")

    # --- Chromatic number
    wp = welsh_powell(G)
    chi, exact = chromatic_number(G)
    clique = max(len(c) for c in nx.find_cliques(G))
    print("\n--- CHROMATIC NUMBER ---")
    print("Welsh-Powell greedy uses", max(wp.values()) + 1, "colours:", wp)
    print("Exact chi(G) =", chi, "->", exact)
    print(f"Check: clique number {clique} <= chi <= max degree + 1 = {max_deg + 1}")

    # --- Chromatic index
    chi_e, ecol, L = chromatic_index(G)
    print("\n--- CHROMATIC INDEX ---")
    print(f"Max degree Delta = {max_deg}; Vizing: {max_deg} <= chi' <= {max_deg + 1}")
    print("Exact chi'(G) =", chi_e)
    for e, c in sorted(ecol.items()):
        print(f"  edge {e} -> colour {c}")

    # --- Chromatic polynomial
    poly = chromatic_polynomial(G)
    print("\n--- CHROMATIC POLYNOMIAL ---")
    print("P(G,k) expanded :", poly)
    print("P(G,k) factored :", sp.factor(poly))
    print(f"{'k':>3} {'P(G,k)':>10} {'brute force':>13}")
    for kk in range(0, 6):
        print(f"{kk:>3} {int(poly.subs(k, kk)):>10} {brute_force_count(G, kk):>13}")
    smallest = min(x for x in range(1, 10) if poly.subs(k, x) > 0)
    print("Smallest k with P(G,k) > 0 =", smallest, "(equals chi(G))")

    # --- Figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    draw_vertex_colouring(G, wp, pos, axes[0][0],
                          f"1) Welsh-Powell vertex colouring "
                          f"({max(wp.values()) + 1} colours)")
    draw_vertex_colouring(G, exact, pos, axes[0][1],
                          f"2) Exact vertex colouring: chi(G) = {chi}")
    draw_edge_colouring(G, ecol, pos, axes[1][0],
                        f"3) Edge colouring: chi'(G) = {chi_e}")
    draw_polynomial_chart(poly, G, axes[1][1])
    fig.suptitle("Graph Coloring: Exam Timetable Model", fontsize=14,
                 fontweight="bold")
    plt.tight_layout()
    fig.savefig("graph_coloring_output.png", dpi=150)
    print("\nSaved figure -> graph_coloring_output.png")
    # plt.show()   # uncomment for an interactive window


if __name__ == "__main__":
    main()
