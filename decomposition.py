import networkx as nx
import matplotlib.pyplot as plt
import config

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