import pandas as pd
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.analysis.local_env import CrystalNN
import networkx as nx
from grave import Node2VecGraph


if __name__ == '__main__':
    df = pd.read_pickle("out/all_stable_bandgap.pkl")

    with open("all_stable_bandgap.node2vec.walks", "w") as output:

        for i in range(len(df['structure'])):
            struct = df['structure'][i]

            print(struct.formula)

            struct_graph = StructureGraph.with_local_env_strategy(struct, CrystalNN())
            labels = {i: spec.name for i, spec in enumerate(struct.species)}
            G = nx.Graph(struct_graph.graph)
            G = nx.relabel_nodes(G, labels)

            for source, target in G.edges():
                G[source][target]['weight'] = 1

            n2v_G = Node2VecGraph(G, False, 1, 1)

            n2v_G.preprocess_transition_probs()
            walks = n2v_G.simulate_walks(num_walks=10, walk_length=40)

            for walk in walks:
                line = " ".join(walk)
                output.write(line + "\n")

        output.flush()
