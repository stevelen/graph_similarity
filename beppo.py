import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import config
import find_star as fs
import find_clique as fc
import find_biclique as fb
import find_starclique as fsc
import math
import model as ml
import structures as st
import merge_structures as merger
import choose_from_candidates as cfc
from networkx.algorithms.components.connected import connected_components


def decomposition(G, minimum_component_size = 10, neighborhood_size = 1):
    components = []
    slashed = []
    G_copy = G.copy()

    #connected_components = sorted(nx.connected_components(G_copy), key=len, reverse=True)
    #largest_connected_component = list(connected_components[0])
    largest_connected_component = max(nx.connected_components(G_copy), key=len)
    lccG = G_copy.subgraph(largest_connected_component)
    #print(lccG.degree)
    largest_degree = sorted(lccG.degree, key=lambda x: x[1], reverse=True)[0][1]
    if config.DEBUG:
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
        #connected_components = sorted(nx.connected_components(G_copy), key=len, reverse=True)
        #largest_connected_component = list(connected_components[0])
        largest_connected_component = max(nx.connected_components(G_copy), key=len)
        lccG = G_copy.subgraph(largest_connected_component)
        largest_degree = sorted(lccG.degree, key=lambda x: x[1], reverse=True)[0][1]
        if config.DEBUG:
            print(f"Uj hub: {new_hub}")
            print(f"Az uj hub szomszedsaga: {hub_neighbors}")
            print(f"Eddig talalt komponensek: {components}")
            print(f"Legnagyobb osszefuggo komponens: {largest_connected_component}")
            nx.draw_circular(G_copy, with_labels = True)
            plt.show()   
            print("----- Iteracio vege -----")

    if config.DEBUG:
        print(f"Vegso komponensek listaja: {components}")
    return components

def beppo(graph, structure_vocab):
    model = ml.Model(graph, [], [], [], [], [])
    #model.nx_graph = graph
    nx.draw_circular(graph, with_labels = True)
    plt.show()
    components = decomposition(graph)
    print(components)
    for structure in structure_vocab:
        if structure == "star":
            fs.generate_star_component_candidates(model, components)
        if structure == "clique":
            fc.generate_clique_component_candidates(model, components)
        if structure == "biclique":
            fb.generate_biclique_component_candidates(model, components)
        if structure == "starclique":
            fsc.generate_starclique_component_candidates(model, components)
    
    #print(model)
    merger.merge_similar_cliques(model)
    merger.merge_similar_structures(model, "biclique")
    merger.merge_similar_structures(model, "starclique")
    #print(model)

    for star in model.stars:
        model.structures.append(star)
    for clique in model.cliques:
        model.structures.append(clique)
    for biclique in model.bicliques:
        model.structures.append(biclique)
    for starclique in model.starcliques:
        model.structures.append(starclique)

    print(model)
    model = cfc.choose_stuctures(model)
    print(model)
    #for structure in model.structures:
    #    nx.draw_circular(structure.nx_graph, with_labels = True)
    #    plt.show()
    return model
    

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
    #G = nx.from_numpy_matrix(A)
    struct_vocab = ["star", "clique", "biclique", "starclique"]
    G = nx.erdos_renyi_graph(1000, 0.05, 8788235817235, False)
    #G = nx.erdos_renyi_graph(100, 0.4, 8788235817235, False)
    #G = nx.erdos_renyi_graph(50, 0.2, 8788235817235, False)
    #nx.draw_circular(G, with_labels = True)
    #plt.show()
    #print(decomposition(G))
    #fsc.find_starclique_from_component([7, 13, 16, 17, 27, 35, 39, 40, 47, 49, 59, 60, 61, 70, 71, 75, 81, 94, 95, 86], G)
    beppo(G, struct_vocab)
    
if __name__=="__main__":
    main()
