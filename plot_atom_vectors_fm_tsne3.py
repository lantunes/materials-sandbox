import argparse
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from grave import FactorizationMachine
from utils import color_by_label, build_label_color_map, build_marker_size_map


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a t-SNE plot for a trained GloVe model.')
    parser.add_argument('--model', '-m', action='store',
                        required=True,
                        help='The filename of the stored GloVe model.')
    parser.add_argument('--perplexity', '-p', action='store',
                        default=50, type=int,
                        help='The perplexity parameter for t-SNE.')
    parser.add_argument('--iterations', '-i', action='store',
                        default=500, type=int,
                        help='The number of iterations for t-SNE.')
    parser.add_argument('--learning-rate', '-r', action='store',
                        default=10, type=int,
                        help='The learning rate parameter for t-SNE.')

    args = parser.parse_args()

    model = FactorizationMachine.load_model(args.model)

    label_color_map = build_label_color_map()
    marker_size_map = build_marker_size_map()

    color_map = []
    labels = []
    sizes = []
    X = []
    for node in model.dictionary.keys():
        label = node[0].upper() + node[1:]
        color_map.append(color_by_label(label))
        labels.append(label)
        sizes.append(marker_size_map[label])
        X.append(model.W[model.dictionary[node]])

    tsne = TSNE(n_components=2, verbose=1,
                perplexity=args.perplexity, n_iter=args.iterations, learning_rate=args.learning_rate)
    result = tsne.fit_transform(X)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(result[:, 0], result[:, 1], c=color_map, s=sizes)

    for i, atom in enumerate(labels):
        reduced_embedding = result[i]
        c = label_color_map[atom]
        ax.annotate(atom, (reduced_embedding[0], reduced_embedding[1]), color=c)

    plt.show()
