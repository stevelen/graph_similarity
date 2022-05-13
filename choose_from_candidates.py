import model as ml
import structures as st

def choose_stuctures(model):
    final_model = ml.Model(model.nx_graph, [], [], [], [], [])
    model.structures = sorted(model.structures, key=lambda x: (len(x.nodes), x.number_of_edges), reverse=True)
    nodes_already_used = []
    
    for structure in model.structures:
        if len(list(set(nodes_already_used) & set(structure.nodes))) > len(structure.nodes) * 0.6:
            pass
        else:
            if isinstance(structure, st.Biclique):
                final_model.bicliques.append(structure)
            if isinstance(structure, st.Clique):
                final_model.cliques.append(structure)
            if isinstance(structure, st.Starclique):
                final_model.starcliques.append(structure)
            if isinstance(structure, st.Star):
                final_model.stars.append(structure)
            final_model.structures.append(structure)
            nodes_already_used.extend(structure.nodes)
        
    left_out_nodes = list(set(list(model.nx_graph.nodes)) - set(nodes_already_used)) + list(set(nodes_already_used) - set(list(model.nx_graph.nodes)))
    
    for structure in model.structures:
        if len(list(set(left_out_nodes) & set(structure.nodes))) > len(structure.nodes) * 0.8:
            if isinstance(structure, st.Biclique):
                final_model.bicliques.append(structure)
            if isinstance(structure, st.Clique):
                final_model.cliques.append(structure)
            if isinstance(structure, st.Starclique):
                final_model.starcliques.append(structure)
            if isinstance(structure, st.Star):
                final_model.stars.append(structure)
            final_model.structures.append(structure)
            left_out_nodes = [x for x in left_out_nodes if x not in structure.nodes]
            print("extra structure added")
            print(left_out_nodes)
    print(f" number of left out nodes: {len(list(set(list(model.nx_graph.nodes)) - set(nodes_already_used)) + list(set(nodes_already_used) - set(list(model.nx_graph.nodes))))}")
    return final_model
            