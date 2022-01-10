import itertools
import model as ml
import networkx as nx


def remove_duplicates(original_list):
        original_list.sort()
        return list(original_list for original_list,_ in itertools.groupby(original_list))

def merge_similar_cliques(model, threshold = 0.9):
    print("merging similar cliques")
    model.cliques = remove_duplicates(model.cliques)
    original_cliques = model.cliques.copy()
    biggest_overlap = 0
    for i in range(len(original_cliques)):
        biggest_overlap = 0
        for j in range(i+1, len(original_cliques)):
            clique_A_nodes = original_cliques[i]
            clique_B_nodes = original_cliques[j]
            intersection = list(set(clique_A_nodes) & set(clique_B_nodes))
            overlap = len(intersection) / len(clique_A_nodes) if len(clique_A_nodes) > len(clique_B_nodes) else len(intersection) / len(clique_B_nodes)
            #print(f"overlap: {overlap * 100}%")
            if overlap > biggest_overlap:
                biggest_overlap = overlap
                most_overlapping_clique = original_cliques[j]
        if biggest_overlap >= threshold and original_cliques[i] in model.cliques and most_overlapping_clique in model.cliques:
            print("merged something")
            #print(list(most_overlapping_clique.nodes) == list(original_cliques[i].nodes))
            merged_clique = list(set(clique_A_nodes) | set(most_overlapping_clique))
            model.cliques.remove(original_cliques[i])
            model.cliques.remove(most_overlapping_clique)
            print(f"Removed: \n {original_cliques[i]} \n {most_overlapping_clique}")
            model.cliques.append(model.nx_graph.subgraph(merged_clique))
            print(f"Added: {merged_clique}")

def merge_similar_structures(model, structure, threshold = 0.9):
    if structure == "biclique":
        print("merging similar bicliques")
        original_structure = model.bicliques.copy()
    if structure == "starclique":
        print("merging similar starcliques")
        original_structure = model.starcliques.copy()
    for i in range(len(original_structure)):
        for j in range(i+1, len(original_structure)):
            left_intersection = list(set(original_structure[i].left) & set(original_structure[j].left))
            right_intersection = list(set(original_structure[i].right) & set(original_structure[j].right))
            left_overlap = len(left_intersection) / len(original_structure[i].left) if len(original_structure[i].left) > len(original_structure[j].left) else len(left_intersection) / len(original_structure[j].left)
            right_overlap = len(right_intersection) / len(original_structure[i].right) if len(original_structure[i].right) > len(original_structure[j].right) else len(right_intersection) / len(original_structure[j].right)
            #print(f"left_overlap: {left_overlap * 100}%")
            #print(f"right_overlap: {right_overlap * 100}%")
            #print("----------------")
        if left_overlap > threshold and right_overlap > threshold and original_structure[i] in model.bicliques and original_structure[j] in model.bicliques:
            print("merged something")
            if structure == "biclique":
                merged_biclique = ml.Biclique()
                merged_biclique.nodes = list(set(original_structure[i].nodes) | set(original_structure[j].nodes))
                merged_biclique.left = list(set(original_structure[i].left) | set(original_structure[j].left))
                merged_biclique.right = list(set(original_structure[i].right) | set(original_structure[j].right))
                print(f"Removed: \n {original_structure[i].nodes} \n {original_structure[j].nodes}")
                model.bicliques.remove(original_structure[i])
                model.bicliques.remove(original_structure[j])
                print(f"Added: {merged_biclique.nodes}")
                model.bicliques.append(merged_biclique)
            if structure == "starclique":
                merged_starclique = ml.Starclique()
                merged_starclique.nodes = list(set(original_structure[i].nodes) | set(original_structure[j].nodes))
                merged_starclique.left = list(set(original_structure[i].left) | set(original_structure[j].left))
                merged_starclique.right = list(set(original_structure[i].right) | set(original_structure[j].right))
                print(f"Removed: \n {original_structure[i].nodes} \n {original_structure[j].nodes}")
                model.starcliques.remove(original_structure[i])
                model.starcliques.remove(original_structure[j])
                print(f"Added: {merged_starclique.nodes}")
                model.starcliques.append(merged_starclique)