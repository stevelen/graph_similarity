import networkx as nx

class Model:
    
    nx_graph = None
    bicliques = []
    cliques = []
    stars = []
    starcliques = []
    structures = []
    
    def __str__(self):
        return f"Graph model: \n number of stars: {len(self.stars)} \n number of cliques: {len(self.cliques)} \n number of bicliques: {len(self.bicliques)} \n number of starcliques: {len(self.starcliques)} \n number of all structures: {len(self.structures)} "
    
    def __init__(self, nx_graph, bicliques, cliques, stars, starcliques, structures):
        self.nx_graph = nx_graph
        self.bicliques = bicliques
        self.cliques = cliques
        self.stars = stars
        self.starcliques = starcliques
        self.structures = structures