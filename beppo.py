import time
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
import sys

show_plots = False

def beppo(graph):
    model = ml.Model(graph, [], [], [], [], [])
    structure_vocab = ["star", "clique", "biclique", "starclique"]
    components = dc.decomposition(graph)
    for structure in structure_vocab:
        if structure == "star":
            fs.generate_star_component_candidates(model, components)
        if structure == "clique":
            fc.generate_clique_component_candidates(model, components)
        if structure == "biclique":
            fb.generate_biclique_component_candidates(model, components)
        if structure == "starclique":
            fsc.generate_starclique_component_candidates(model, components)

    merger.merge_similar_cliques(model)
    merger.merge_similar_structures(model, "biclique")
    merger.merge_similar_structures(model, "starclique")

    for star in model.stars:
        model.structures.append(star)
    for clique in model.cliques:
        model.structures.append(clique)
    for biclique in model.bicliques:
        model.structures.append(biclique)
    for starclique in model.starcliques:
        model.structures.append(starclique)

    model = cfc.choose_stuctures(model)
    print(model)
    if show_plots:
        for structure in model.structures:
            print(type(structure))
            nx.draw_circular(structure.nx_graph, with_labels = True)
            plt.show()

    return model
    

def main():
    global show_plots
    if(len(sys.argv) > 1):
            show_plots = sys.argv[1]
    
    G = nx.erdos_renyi_graph(400, 0.1, int(time.time()), False)
    beppo(G)

    
if __name__=="__main__":
    main()
