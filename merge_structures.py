import itertools
import structures as st

def remove_duplicates(original_list):
        original_list.sort()
        return list(original_list for original_list,_ in itertools.groupby(original_list))

def merge_similar_cliques(model, threshold = 0.9):
    print("merging similar cliques")
    #model.cliques = remove_duplicates(model.cliques)
    original_cliques = model.cliques.copy()
    biggest_overlap = 0
    for i in range(len(original_cliques)):
        biggest_overlap = 0
        for j in range(i+1, len(original_cliques)):
            clique_A_nodes = original_cliques[i].nodes
            clique_B_nodes = original_cliques[j].nodes
            intersection = list(set(clique_A_nodes) & set(clique_B_nodes))
            overlap = len(intersection) / len(clique_A_nodes) if len(clique_A_nodes) < len(clique_B_nodes) else len(intersection) / len(clique_B_nodes)
            #print(f"overlap: {overlap * 100}%")
            if overlap > biggest_overlap:
                biggest_overlap = overlap
                most_overlapping_clique = original_cliques[j]
        if biggest_overlap >= threshold and original_cliques[i] in model.cliques and most_overlapping_clique in model.cliques:
            print("merged cliques")
            #print(list(most_overlapping_clique.nodes) == list(original_cliques[i].nodes))
            merged_clique = st.Clique() 
            merged_clique.nodes = list(set(clique_A_nodes) | set(most_overlapping_clique.nodes))
            merged_clique.nx_graph = model.nx_graph.subgraph(merged_clique.nodes)
            merged_clique.number_of_edges = merged_clique.nx_graph.number_of_edges()
            model.cliques.remove(original_cliques[i])
            model.cliques.remove(most_overlapping_clique)
            #print(f"Removed: \n {original_cliques[i].nodes} \n {most_overlapping_clique.nodes}")
            model.cliques.append(merged_clique)
            #print(f"Added: {merged_clique.nodes}")

def merge_similar_structures(model, structure, threshold = 0.9):
    if structure == "biclique":
        print("merging similar bicliques")
        original_structure = model.bicliques.copy()
    if structure == "starclique":
        print("merging similar starcliques")
        original_structure = model.starcliques.copy()
    left_overlap = 0
    right_overlap = 0
    for i in range(len(original_structure)):
        for j in range(i+1, len(original_structure)):
            left_intersection = list(set(original_structure[i].left) & set(original_structure[j].left))
            right_intersection = list(set(original_structure[i].right) & set(original_structure[j].right))
            left_overlap = len(left_intersection) / len(original_structure[i].left) if len(original_structure[i].left) < len(original_structure[j].left) else len(left_intersection) / len(original_structure[j].left)
            right_overlap = len(right_intersection) / len(original_structure[i].right) if len(original_structure[i].right) < len(original_structure[j].right) else len(right_intersection) / len(original_structure[j].right)
            #print(f"left_overlap: {left_overlap * 100}%")
            #print(f"right_overlap: {right_overlap * 100}%")
            #print("----------------")
        if left_overlap > threshold and right_overlap > threshold and original_structure[i] in model.bicliques and original_structure[j] in model.bicliques:
            if structure == "biclique":
                print("merged bicliques")
                merged_biclique = st.Biclique()
                merged_biclique.nodes = list(set(original_structure[i].nodes) | set(original_structure[j].nodes))
                merged_biclique.left = list(set(original_structure[i].left) | set(original_structure[j].left))
                merged_biclique.right = list(set(original_structure[i].right) | set(original_structure[j].right))
                merged_biclique.nx_graph = model.nx_graph.subgraph(merged_biclique.nodes)
                merged_biclique.number_of_edges = merged_biclique.nx_graph.number_of_edges()
                #print(f"Removed: \n {original_structure[i].nodes} \n {original_structure[j].nodes}")
                model.bicliques.remove(original_structure[i])
                model.bicliques.remove(original_structure[j])
                #print(f"Added: {merged_biclique.nodes}")
                model.bicliques.append(merged_biclique)
            if structure == "starclique":
                print("merged starcliques")
                merged_starclique = st.Starclique()
                merged_starclique.nodes = list(set(original_structure[i].nodes) | set(original_structure[j].nodes))
                merged_starclique.left = list(set(original_structure[i].left) | set(original_structure[j].left))
                merged_starclique.right = list(set(original_structure[i].right) | set(original_structure[j].right))
                merged_starclique.nx_graph = model.nx_graph.subgraph(merged_starclique.nodes)
                merged_starclique.number_of_edges = merged_starclique.nx_graph.number_of_edges()
                #print(f"Removed: \n {original_structure[i].nodes} \n {original_structure[j].nodes}")
                model.starcliques.remove(original_structure[i])
                model.starcliques.remove(original_structure[j])
                #print(f"Added: {merged_starclique.nodes}")
                model.starcliques.append(merged_starclique)