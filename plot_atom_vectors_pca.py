import argparse
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from glove import Glove


def color_by_label(label):
    if label in ["H", "Li", "Na", "K", "Rb", "Cs"]:
        return "red"
    if label in ["Be", "Mg", "Ca", "Sr", "Ba"]:
        return "brown"
    if label in ["B", "Al", "Ga", "In", "Tl"]:
        return "steelblue"
    if label in ["C", "Si", "Ge", "Sn", "Pb"]:
        return "purple"
    if label in ["N", "P", "As", "Sb", "Bi"]:
        return "blue"
    if label in ["O", "S", "Se", "Te"]:
        return "yellow"
    if label in ["F", "Cl", "Br", "I"]:
        return "cyan"
    if label in ["He", "Ne", "Ar", "Kr", "Xe"]:
        return "olive"
    if label in ["Ni", "Pd", "Pt", "Cu", "Ag", "Au", "Zn", "Cd", "Hg", "Rh", "Ir"]:
        return "orange"
    if label in ["Ti", "Zr", "Hf", "V", "Nb", "Ta", "Cr", "Mo", "W"]:
        return "green"
    if label in ["Fe", "Mn", "Tc", "Ru", "Re", "Os", "Co"]:
        return "lime"
    return "lightgray"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a t-SNE plot for a trained GloVe model.')
    parser.add_argument('--model', '-m', action='store',
                        required=True,
                        help='The filename of the stored GloVe model.')

    args = parser.parse_args()

    model = Glove.load(args.model)

    color_map = []
    labels = []
    X = []
    for node in model.dictionary.keys():
        label = node[0].upper() + node[1:]
        color_map.append(color_by_label(label))
        labels.append(label)
        X.append(model.word_vectors[model.dictionary[node]])

    pca = PCA(n_components=2)
    result = pca.fit_transform(X)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(result[:, 0], result[:, 1], c=color_map)
    for i, res in enumerate(result):
        ax.annotate(labels[i], (res[0], res[1]))
    plt.show()