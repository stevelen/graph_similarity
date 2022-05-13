import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import structures as st

def generate_clique_component_candidates(M, components = []):
    for c in components:
        clique_graph, clique_nodes = find_clique_from_component(c, M.nx_graph)
        if clique_graph != 0:
            clique = st.Clique()
            clique.nodes = clique_nodes
            clique.nx_graph = clique_graph
            clique.number_of_edges = clique_graph.number_of_edges()
            M.cliques.append(clique)


def find_clique_from_component(component, G, min_connectivity_fraction = 0.5):

    component_Graph = G.subgraph(component)

    largest_clique = nx.algorithms.approximation.max_clique(component_Graph)
    nodes_original = list(largest_clique)
    component_Graph = G.subgraph(nodes_original)

    while True:
        cutoff = min_connectivity_fraction * len(nodes_original)
        neighbors_list = []
        for x in nodes_original:
            neighbors_list = neighbors_list + [n for n in G[x]]
        neighbor_map = list(Counter(neighbors_list).items())
        nodes_to_add = sorted(list(filter(lambda x: x[1] >= cutoff and x[0] not in nodes_original, neighbor_map)), key = lambda x: G.degree[x[0]], reverse=True)
        if len(nodes_to_add) > 0:
            node_to_add = nodes_to_add[0][0]
        else:
            break
        nodes_original.append(node_to_add)
        component_Graph = G.subgraph(nodes_original)

    if component_Graph.number_of_nodes() < 10:
            return 0, []
    else:
        return_nodes = list(nodes_original)
        return component_Graph, list(component_Graph.nodes)