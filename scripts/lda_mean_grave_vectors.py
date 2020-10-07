import matplotlib.pyplot as plt
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from mpl_toolkits.mplot3d import Axes3D
from grave import FactorizationMachine
from utils import color_by_band_gap, get_label_by_band_gap
import pandas as pd

"""
Here, we use LDA for dimensionality reduction, reducing the size of the GraVe embedding from 20 to 3.
"""


if __name__ == '__main__':
    fm = FactorizationMachine.load_model("../out/all_stable_bandgap_dim20.fm.ctx10_add_cont.model")
    embeddings = fm.W

    df = pd.read_pickle("../out/all_stable_bandgap.pkl")

    color_map = []
    X = []
    Y = []
    for i in range(len(df['structure'])):
        struct = df['structure'][i]
        band_gap = df['band_gap'][i]

        # if band_gap == 0.0: continue

        color_map.append(color_by_band_gap(band_gap))
        vectors = []
        for element in struct.species:
            vectors.append(np.array(embeddings[fm.dictionary[element.name]]))
        X.append(np.mean(vectors, axis=0))
        Y.append(get_label_by_band_gap(band_gap))

    result = LinearDiscriminantAnalysis(n_components=3).fit_transform(X, Y)

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(result[:, 0], result[:, 1], result[:, 2], c=color_map)
    plt.show()
