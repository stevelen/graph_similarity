from math import floor
import mdl

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

def compute_clique_description_length(model, clique):
    max_n_edges = int(mdl.choose(len(clique.nodes), 2))
    cost_sparse_or_dense = 1
    cost_n_edges = mdl.log2_zero(mdl.log2_zero(floor(max_n_edges/2))) + mdl.log2_zero(min(clique.number_of_edges, max_n_edges - clique.number_of_edges))
    rest = cost_sparse_or_dense + cost_n_edges
    cost_n_nodes = mdl.unviversal_integer(len(clique.nodes))
    cost_node_ids = mdl.log2_choose(model.nx_graph.number_of_nodes(), len(clique.nodes))
    return cost_n_nodes + rest + cost_node_ids

