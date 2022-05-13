import networkx as nx
import matplotlib.pyplot as plt
import math
import structures as st

def generate_star_component_candidates(M, components = []):
    for c in components:
        star_nx_graph, star_nodes, star_hub = find_star_from_component(c, M.nx_graph)
        if star_nx_graph != 0:
            star = st.Star()
            star.nodes = star_nodes
            star.hub = star_hub
            star.nx_graph = star_nx_graph
            star.number_of_edges = star_nx_graph.number_of_edges()
            M.stars.append(star)

def find_star_from_component(component, G):
    component_Graph = G.subgraph(component)
    top_nodes = sorted(component_Graph.degree, key=lambda x: x[1], reverse=True)
    
    if top_nodes[0][1] == top_nodes[1][1]:
        return 0, [], 0
    else:
        hub = top_nodes[0][0]
        subgraph = list(nx.descendants_at_distance(component_Graph, hub, 1)) 
        subgraph.append(hub)
        sub_G = G.subgraph(subgraph)
        nodes = sub_G.nodes()
        n_spokes = sub_G.number_of_nodes() - 1
        fraction = 0.1
        candidates = sorted(list(filter(lambda x: n_spokes - 1 > x[1]-1 and x[1]-1 > 0.05* n_spokes, list(sub_G.degree()))), key = lambda x: x[1], reverse=True)
        temp = []
        for x in candidates:
            temp.append(x[0])
        candidates = temp
        cut_point = math.ceil(fraction * len(candidates))
        nodes_to_cut = candidates[:cut_point]
        while len(nodes_to_cut) > 0 and sub_G.number_of_nodes() >= 10:
            
            nodes_to_keep = list(filter(lambda x: x not in nodes_to_cut, nodes))
            sub_G = G.subgraph(nodes_to_keep)
            nodes = sub_G.nodes()
            n_spokes = sub_G.number_of_nodes() - 1
            fraction = min(fraction + 0.01, 1.0)
            candidates = sorted(list(filter(lambda x: n_spokes - 1 > x[1]-1 and x[1]-1 > 0.05* n_spokes, list(sub_G.degree()))), key = lambda x: x[1], reverse=True)
            temp = []
            for x in candidates:
                temp.append(x[0])
            candidates = temp
            cut_point = math.ceil(fraction * len(candidates))
            nodes_to_cut = candidates[:cut_point]
        if sub_G.number_of_nodes() < 10:
            return 0, [], 0
        else:
            return_nodes = list(nodes)
            return_nodes.remove(hub)
            return sub_G, list(sub_G.nodes), hub