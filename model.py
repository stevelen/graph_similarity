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
        
