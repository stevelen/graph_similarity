import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import config
import find_star as fs
import find_clique as fc
import find_biclique as fb
import find_starclique as fsc
import math
from networkx.algorithms.components.connected import connected_components


def decomposition(G, minimum_component_size = 1, neighborhood_size = 1):
    components = []
    slashed = []
    G_copy = G.copy()

    connected_components = sorted(nx.connected_components(G_copy), key=len, reverse=True)
    largest_connected_component = list(connected_components[0])
    lccG = G_copy.subgraph(largest_connected_component)
    largest_degree = sorted(lccG.degree, key=lambda x: x[1], reverse=True)[0][1]
    if config.DEBUG:
        print(f"Osszefuggo komponensek: {connected_components}")
        print(f"Legnagyobb osszefuggo komponens: {largest_connected_component}")
        nx.draw_circular(G, with_labels = True)
        plt.show()
        print("----- While ciklus -----")



    while len(largest_connected_component) >= minimum_component_size and largest_degree >= minimum_component_size:
        new_hub = sorted(lccG.degree, key=lambda x: x[1], reverse=True)[0][0]
        slashed.append(new_hub)
        hub_neighbors = list(nx.descendants_at_distance(G_copy, new_hub, neighborhood_size))
        hub_neighbors.append(new_hub)
        components.append(hub_neighbors)
        ebunch = list(G.edges(new_hub))
        G_copy.remove_edges_from(ebunch)
        connected_components = sorted(nx.connected_components(G_copy), key=len, reverse=True)
        largest_connected_component = list(connected_components[0])
        lccG = G_copy.subgraph(largest_connected_component)
        largest_degree = sorted(lccG.degree, key=lambda x: x[1], reverse=True)[0][1]
        if config.DEBUG:
            print(f"Uj hub: {new_hub}")
            print(f"Az uj hub szomszedsaga: {hub_neighbors}")
            print(f"Eddig talalt komponensek: {components}")
            print(f"Osszefuggo komponensek: {connected_components}")
            print(f"Legnagyobb osszefuggo komponens: {largest_connected_component}")
            nx.draw_circular(G_copy, with_labels = True)
            plt.show()   
            print("----- Iteracio vege -----")

    if config.DEBUG:
        print(f"Vegso komponensek listaja: {components}")
    return components

def main():

    A = np.array([
        [0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 0, 0, 0, 0, 0, 0]])
    G = nx.from_numpy_matrix(A)
    #G = nx.erdos_renyi_graph(350, 0.12, 8788235817235, False)
    G = nx.erdos_renyi_graph(100, 0.12, 8788235817235, False)
    #nx.draw_circular(G, with_labels = True)
    #plt.show()
    #print(decomposition(G))
    fsc.find_starclique_from_component([7, 13, 16, 17, 27, 35, 39, 40, 47, 49, 59, 60, 61, 70, 71, 75, 81, 94, 95, 86], G)
    #fsc.find_starclique_from_component([129, 259, 260, 262, 135, 137, 269, 270, 143, 17, 274, 149, 22, 27, 155, 156, 160, 290, 292, 295, 40, 298, 43, 300, 175, 49, 305, 185, 314, 315, 189, 62, 191, 
#317, 194, 197, 199, 327, 202, 75, 77, 78, 79, 207, 211, 339, 341, 217, 218, 220, 222, 97, 228, 101, 102, 103, 105, 111, 120, 250, 123, 252, 333], G)
  
if __name__=="__main__":
    main()
