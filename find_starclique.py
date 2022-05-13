import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import structures as st

def generate_starclique_component_candidates(M, components = []):
    for c in components:
        starclique_nx_graph, starclique_nodes, left, right = find_starclique_from_component(c, M.nx_graph)
        if starclique_nx_graph != 0:
            starclique = st.Starclique()
            starclique.nodes = starclique_nodes
            starclique.left = left
            starclique.right = right
            starclique.nx_graph = starclique_nx_graph
            starclique.number_of_edges = starclique_nx_graph.number_of_edges()
            M.starcliques.append(starclique)

def find_starclique_from_component(component, G):

    max_intra_connectivity = 0.05
    min_intra_connectivity = 0.5
    min_inter_connectivity = 0.5
    component_Graph = G.subgraph(component)

    largest_clique = nx.algorithms.approximation.max_clique(component_Graph)
    left = list(largest_clique)
    component_Graph = G.subgraph(left)

    neighbors_list = []
    for x in left:
        neighbors_list = neighbors_list + [n for n in G[x]]
    neighbor_map = list(Counter(neighbors_list).items())
    right_candidates = list(filter(lambda x: x[1] >= min_inter_connectivity * len(left) and x[0] not in left, neighbor_map))
    right_candidates = list(x[0] for x in right_candidates)
    right_Graph = G.subgraph(right_candidates)
    if right_candidates == []:
        return 0, 0, [], []
    right = nx.maximal_independent_set(right_Graph, seed=1234)
    right = sorted(right, key=lambda x: G.degree[x], reverse=True)

    iter_counter = 0
    while True:

        neighbors_list = []
        for x in right:
            neighbors_list = neighbors_list + [n for n in G[x]]
        neighbor_map = list(Counter(neighbors_list).items())

        added_left = list(filter(lambda x: x[0] not in left and x[0] not in right and x[1] >= min_inter_connectivity * len(right) and len(list(set([n for n in G[x[0]]]) & set(left))) >= min_intra_connectivity * len(left), neighbor_map))
        if len(added_left) > 0:
            added_left_sorted_list = []
            for x in sorted(added_left, key=lambda x: x[1], reverse=True):
                added_left_sorted_list.append(x[0])   
            left.append(added_left_sorted_list[0])
        
        neighbors_list = []
        for x in left:
            neighbors_list = neighbors_list + [n for n in G[x]]
        neighbor_map = list(Counter(neighbors_list).items())

        added_right = list(filter(lambda x: x[0] not in left and x[0] not in right and x[1] >= min_inter_connectivity * len(left) and len(list(set([n for n in G[x[0]]]) & set(right))) <= max_intra_connectivity * len(right), neighbor_map))
        if len(added_right) > 0:
            added_right_sorted_list = []
            for x in sorted(added_right, key=lambda x: x[1], reverse=True):
                added_right_sorted_list.append(x[0])   
            right.append(added_right_sorted_list[0])
        if len(added_left) == 0 and len(added_right) == 0:
            break
        iter_counter+=1
    
    left_right_union = list(set(left) | set(right))
    component_Graph = G.subgraph(left_right_union)

    isolates = []
    for node in left_right_union:
        if component_Graph.degree[node] == 0:
            isolates.append(node)
    left = list(set(left).difference(set(isolates)))
    right = list(set(right).difference(set(isolates)))
    left_right_union = list(set(left) | set(right))
    component_Graph = G.subgraph(left_right_union)

    if component_Graph.number_of_nodes() < 10 or len(left) < 3 or len(right) < 3 :
        return 0, 0, [], []
    else:
        return component_Graph, list(component_Graph.nodes), left, right
        