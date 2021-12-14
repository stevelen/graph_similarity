import networkx as nx
import matplotlib.pyplot as plt
import math
from collections import Counter


def find_clique_from_component(component, G, min_connectivity_fraction = 0.5):

    component_Graph = G.subgraph(component)
    print(f"component length:{len(component)}")
    nx.draw_circular(component_Graph, with_labels = True)
    plt.show()

    largest_clique = nx.algorithms.approximation.max_clique(component_Graph)
    print(f"max clique: {largest_clique}")
    nodes_original = list(largest_clique)
    print(nodes_original)
    print(f"clique length: {len(nodes_original)}")
    component_Graph = G.subgraph(nodes_original)
    nx.draw_circular(component_Graph, with_labels = True)
    plt.show()

    while True:
        cutoff = min_connectivity_fraction * len(nodes_original)
        neighbors_list = []
        for x in nodes_original:
            neighbors_list = neighbors_list + [n for n in G[x]]
        print(neighbors_list)
        neighbor_map = list(Counter(neighbors_list).items())
        nodes_to_add = sorted(list(filter(lambda x: x[1] >= cutoff and x[0] not in nodes_original, neighbor_map)), key = lambda x: G.degree[x[0]], reverse=True)
        print(nodes_to_add)
        if len(nodes_to_add) > 0:
            node_to_add = nodes_to_add[0][0]
        else:
            break
        print(f"node added: {node_to_add}")
        nodes_original.append(node_to_add)
        component_Graph = G.subgraph(nodes_original)
        nx.draw_circular(component_Graph, with_labels = True)
        plt.show()

    print(nodes_original)

    if component_Graph.number_of_nodes() < 10:
            return 0, []
    else:
        nx.draw_circular(component_Graph, with_labels = True)
        plt.show() 
        return_nodes = list(nodes_original)
        return component_Graph, return_nodes