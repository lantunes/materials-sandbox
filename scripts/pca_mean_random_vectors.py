import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
from utils import RandomVectors, color_by_band_gap


if __name__ == '__main__':
    rv = RandomVectors.load("../out/all_stable_bandgap_dim20.random.model")

    atom_vectors = rv.vectors

    df = pd.read_pickle("../out/all_stable_bandgap.pkl")

    X = []
    color_map = []
    band_gaps = []
    for i in range(len(df['structure'])):
        struct = df['structure'][i]
        band_gap = df['band_gap'][i]

        # if band_gap == 0.0: continue

        vectors = []
        for element in struct.species:
            vectors.append(np.array(atom_vectors[rv.dictionary[element.name]]))
        X.append(np.mean(vectors, axis=0))
        color_map.append(color_by_band_gap(band_gap))
        band_gaps.append(band_gap)

    pca = PCA(n_components=2)
    result = pca.fit_transform(X)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(result[:, 0], result[:, 1], c=color_map)

    plt.show()
