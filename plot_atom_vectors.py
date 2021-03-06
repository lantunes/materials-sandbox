import argparse

from glove import Glove

import matplotlib.pyplot as plt

import networkx as nx


# def get_community_color(node):
#     if node in ["11", "5", "6", "7", "17"]:
#         return "lightblue"
#     if node in ["12", "22", "18", "1", "20", "2", "14", "8", "4", "13"]:
#         return "red"
#     if node in ["3", "10", "32", "29", "28", "26", "25"]:
#         return "lightgreen"
#     else:
#         return "purple"


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Inspect a trained GloVe model.')
    parser.add_argument('--model', '-m', action='store',
                        required=True,
                        help='The filename of the stored GloVe model.')

    args = parser.parse_args()

    glove = Glove.load(args.model)

    # color_map = []
    X = []
    Y = []
    for node in glove.dictionary.keys():
        # color_map.append(get_community_color(node))
        embedding = glove.word_vectors[glove.dictionary[node]]
        X.append(embedding[0])
        Y.append(embedding[1])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(X, Y)#, color=color_map)
    for vertex in glove.dictionary.keys():
        embedding = glove.word_vectors[glove.dictionary[vertex]]
        ax.annotate(vertex, (embedding[0], embedding[1]))
    plt.show()