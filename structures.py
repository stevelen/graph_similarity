class Biclique:

    nx_graph = None
    nodes = []
    left = []
    right = []
    number_of_edges = 0

    def __str__(self):
        return f"Biclique: \n nx_graph: {self.nx_graph} \n number of nodes: {len(self.nodes)} \n number of left nodes: {len(self.left)} \n number of right nodes: {len(self.right)} \n number of edges: {self.number_of_edges}"


class Starclique:

    nx_graph = None
    nodes = []
    left = []
    right = []
    number_of_edges = 0

    def __str__(self):
        return f"Starclique: \n nx_graph: {self.nx_graph} \n number of nodes: {len(self.nodes)} \n number of left nodes: {len(self.left)} \n number of right nodes : {len(self.right)} \n number of edges: {self.number_of_edges}"

class Star:

    nx_graph = None
    nodes = []
    hub = 0
    number_of_edges = 0
    def __str__(self):
        return f"Star: \n nx_graph: {self.nx_graph} \n number of nodes: {len(self.nodes)} \n hub node: {self.hub} \n number of edges: {self.number_of_edges}"

class Clique:

    nx_graph = None
    nodes = []
    number_of_edges = 0
    def __str__(self):
        return f"Clique: \n nx_graph: {self.nx_graph} \n number of nodes: {len(self.nodes)} \n number of edges: {self.number_of_edges}"

