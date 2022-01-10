import networkx as nx

class Model:
    
    nx_graph = None
    bicliques = []
    #biclique_lefts = []
    #biclique_rights = []
    cliques = []
    stars = []
    #star_spokes = []
    #star_hubs = []
    starcliques = []
    #starclique_lefts = []
    #starclique_rights = []
    structures = []

    def __str__(self):
        return f"Graph model: \n number of stars: {len(self.stars)} \n number of cliques: {len(self.cliques)} \n number of bicliques: {len(self.bicliques)} \n number of starcliques: {len(self.starcliques)} "

class Biclique:

    nodes = []
    left = []
    right = []

    def __str__(self):
        return f"Biclique: \n number of nodes: {len(self.nodes)} \n number of left nodes: {len(self.left)} \n number of right nodes: {len(self.right)}"


class Starclique:

    nodes = []
    left = []
    right = []

    def __str__(self):
        return f"Starclique: \n number of nodes: {len(self.nodes)} \n number of left nodes: {len(self.left)} \n number of right nodes: {len(self.right)}"
