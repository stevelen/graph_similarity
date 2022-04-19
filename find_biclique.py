import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import structures as st

def generate_biclique_component_candidates(M, components = []):
    for c in components:
        biclique_nx_graph, biclique_nodes, left, right = find_biclique_from_component(c, M.nx_graph)
        if biclique_nx_graph != 0:
            biclique = st.Biclique()
            biclique.nodes = biclique_nodes
            biclique.left = left
            biclique.right = right
            biclique.nx_graph = biclique_nx_graph
            biclique.number_of_edges = biclique_nx_graph.number_of_edges()
            M.bicliques.append(biclique)

def find_biclique_from_component(component, G):

    #print("Teljes gráf")
    #nx.draw_circular(G, with_labels = True)
    #plt.show()
    max_intra_connectivity = 0.05
    min_inter_connectivity = 0.5
    component_Graph = G.subgraph(component)
    #print("paraméterben kapott komponens gráf")
    #nx.draw_circular(component_Graph, with_labels = True)
    #plt.show()

    right = nx.maximal_independent_set(component_Graph, seed=7463)
    right = sorted(right, key=lambda x: G.degree[x], reverse=True)
    #print(f"véletlenszerűen választott maximális független csúcshalmaz: {right}")
    right = right[0:min(len(right), 5)]
    component_Graph = G.subgraph(right)
    #print("gráf a csúcshalmaz első 5 eleméből (right)")
    #nx.draw_circular(component_Graph, with_labels = True)
    #plt.show()
    #print(f"kiinduló right: {right}")

    neighbors_list = []
    for x in right:
        neighbors_list = neighbors_list + [n for n in G[x]]
    neighbor_map = list(Counter(neighbors_list).items())
    left_candidates = list(filter(lambda x: x[1] >= min_inter_connectivity * len(right) and x[0] not in right, neighbor_map))
    left_candidates = (x[0] for x in left_candidates)
    left_Graph = G.subgraph(left_candidates)
    left = nx.maximal_independent_set(left_Graph, seed=1234)
    left = sorted(left, key=lambda x: G.degree[x], reverse=True)
    
    neighbors_list = []
    for x in left:
        neighbors_list = neighbors_list + [n for n in G[x]]
    neighbor_map = list(Counter(neighbors_list).items())
    left_to_add = list(filter(lambda x: x[1] <= max_intra_connectivity * len(left) and x in left_candidates, neighbor_map))
    left_to_add = list(x[0] for x in left_to_add)
    if len(left_to_add) > 0:
        left.append(left_to_add)
    #print(f"kiinduló left: {left}")

    if len(left) < 3 or len(right) < 5:
        return 0, 0, [], []
        #return 0
    
    iter_counter = 0
    while True:

        neighbors_list = []
        for x in right:
            neighbors_list = neighbors_list + [n for n in G[x]]
        neighbor_map = list(Counter(neighbors_list).items())
        added_left = list(filter(lambda x: x[0] not in left and x[0] not in right and x[1] >= min_inter_connectivity * len(right) and len(list(set([n for n in G[x[0]]]) & set(left))) <= max_intra_connectivity * len(left), neighbor_map))
        if len(added_left) > 0:
            added_left_sorted_list = []
            for x in sorted(added_left, key=lambda x: x[1], reverse=True):
                added_left_sorted_list.append(x[0])   
            left.append(added_left_sorted_list[0])
            #print(f"{iter_counter}. iterációban új csúcs leftben: {added_left_sorted_list[0]}")
        #else:
            #print(f"{iter_counter}. iterációban nincs új csúcs leftben")


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
            #print(f"{iter_counter}. iterációban új csúcs rightban: {added_right_sorted_list[0]}")
        #else:
            #print(f"{iter_counter}. iterációban nincs új csúcs rightban")
        if len(added_left) == 0 and len(added_right) == 0:
            break
        iter_counter+=1
    #print(f"végső right: {right}")
    #print(f"végső left: {left}")
    left_right_union = list(set(left) | set(right))
    #print(f"left-right unió: {left_right_union}")
    component_Graph = G.subgraph(left_right_union)
    #print("left-right unió gráf")
    #nx.draw_circular(component_Graph, with_labels = True)
    #plt.show()
    isolates = []
    for node in left_right_union:
        if component_Graph.degree[node] == 0:
            isolates.append(node)
    left = list(set(left).difference(set(isolates)))
    right = list(set(right).difference(set(isolates)))
    left_right_union = list(set(left) | set(right))
    component_Graph = G.subgraph(left_right_union)
    #print("végső gráf (biklikk)")
    #nx.draw_circular(component_Graph, with_labels = True)
    #plt.show()

    if component_Graph.number_of_nodes() < 10 :
        #print("empty")
        return 0, 0, [], []
        #return 0
    else:
        return component_Graph, list(component_Graph.nodes), left, right
        #return list(component_Graph.nodes)