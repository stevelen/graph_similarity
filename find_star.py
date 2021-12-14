import networkx as nx
import matplotlib.pyplot as plt
import math

def generate_star_component_candidates(M, minimum_component_size = 10, components = []):
    stars = []
    star_spokes_original = []
    hubs = []
    for c in components:
        star, original_nodes, hub = find_star_from_component(c, M.G)
        if star != 0:
            stars.append(star)
            star_spokes_original.append(original_nodes)
            hubs.append(hub)
    return stars, star_spokes_original, hubs

def find_star_from_component(component, G):
    component_Graph = G.subgraph(component)
    top_nodes = sorted(component_Graph.degree, key=lambda x: x[1], reverse=True)
    
    if top_nodes[0][1] == top_nodes[1][1]:
        return 0, [], 0
    else:
        new_hub = top_nodes[0][0]
        subgraph = list(nx.descendants_at_distance(G, new_hub, 1))
        subgraph.append(new_hub)
        sub_G = G.subgraph(subgraph)
        nx.draw_circular(sub_G, with_labels = True)
        plt.show()   
        nodes_original = sub_G.nodes()
        n_spokes = sub_G.number_of_nodes() - 1
        fraction = 0.1
        candidates = sorted(list(filter(lambda x: n_spokes - 1 > x[1]-1 and x[1]-1 > 0.05* n_spokes, list(sub_G.degree()))), key = lambda x: x[1], reverse=True)
        temp = []
        for x in candidates:
            temp.append(x[0])
        candidates = temp
        print(f"candidates: {candidates}")
        cut_point = math.ceil(fraction * len(candidates))
        nodes_to_cut = candidates[:cut_point]
        print(len(nodes_to_cut))
        print(sub_G.number_of_nodes())
        while len(nodes_to_cut) > 0 and sub_G.number_of_nodes() >= 10:
            print("----------")
            print(f"nodes_to_cut: {nodes_to_cut}")
            print(f"nodes_original: {nodes_original}")
            
            nodes_to_keep = list(filter(lambda x: x not in nodes_to_cut, nodes_original))
            print(f"nodes_to_keep: {nodes_to_keep}")
            sub_G = G.subgraph(nodes_to_keep)
            nodes_original = sub_G.nodes()
            n_spokes = sub_G.number_of_nodes() - 1
            fraction = min(fraction + 0.01, 1.0)
            candidates = sorted(list(filter(lambda x: n_spokes - 1 > x[1]-1 and x[1]-1 > 0.05* n_spokes, list(sub_G.degree()))), key = lambda x: x[1], reverse=True)
            temp = []
            for x in candidates:
                temp.append(x[0])
            candidates = temp
            cut_point = math.ceil(fraction * len(candidates))
            nodes_to_cut = candidates[:cut_point]
            nx.draw_circular(sub_G, with_labels = True)
            plt.show() 
        if sub_G.number_of_nodes() < 10:
            return 0, [], 0
        else:
            nx.draw_circular(sub_G, with_labels = True)
            plt.show() 
            return_nodes = list(nodes_original)
            return_nodes.remove(new_hub)
            return sub_G, return_nodes, new_hub