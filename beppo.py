import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import config
import find_star as fs
import find_clique as fc
import find_biclique as fb
import find_starclique as fsc
import model as ml
import merge_structures as merger
import choose_from_candidates as cfc
import decomposition as dc
import time


def beppo(graph):
    model = ml.Model(graph, [], [], [], [], [])
    structure_vocab = ["star", "clique", "biclique", "starclique"]
    #model.nx_graph = graph
    #nx.draw_circular(graph, with_labels = True)
    #plt.show()
    components = dc.decomposition(graph)
    #components = []
    #components.append([32, 2, 36, 40, 42, 43, 12, 13, 49, 20, 22, 24, 26, 29, 30, 38])
    #print(components)
    #fs.generate_star_component_candidates(model, components)
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

    #print(model)
    model = cfc.choose_stuctures(model)
    print(model)
    #for structure in model.structures:
        #print(type(structure))
        #nx.draw_circular(structure.nx_graph, with_labels = True)
        #plt.show()

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
    
    #G = nx.erdos_renyi_graph(500, 0.03, 8788235817235, False)
    #G = nx.erdos_renyi_graph(100, 0.3, 8788235817235, False)
    G = nx.erdos_renyi_graph(50, 0.4, 8788235817235, False)
    #nx.draw_circular(G, with_labels = True)
    #plt.show()
    #print(decomposition(G))
    #fsc.find_starclique_from_component([7, 13, 16, 17, 27, 35, 39, 40, 47, 49, 59, 60, 61, 70, 71, 75, 81, 94, 95, 86], G)
    beppo(G)
    #G = nx.barabasi_albert_graph(100, 50, seed = 12345)

    

    
    
if __name__=="__main__":
    main()
