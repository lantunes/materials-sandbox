import numpy as np
import pandas as pd
from utils import RandomVectors, OneHotVectors
from grave import FactorizationMachine
from sklearn.linear_model import LinearRegression
from glove import Glove
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_validate

"""
BOREP: Bag of Random Embedding Projections

Instead of pooling the atom vectors themselves, we'll initialize a projection matrix to compute the compound embedding:

h = f(W*e)

where h is the compound embedding, f is a pooling function, W is the projection matrix, and e is the atom vector.

See: Wieting, J., & Kiela, D. (2019). No training required: Exploring random encoders for sentence classification. 
     arXiv preprint arXiv:1901.10444.
"""

if __name__ == '__main__':

    # model = FactorizationMachine.load_model("../out/all_stable_bandgap_dim20.fm.ctx10_add_cont.model")
    # embeddings = model.W
    # converter = lambda x: x
    # dim = 20

    # model = RandomVectors.load("../out/all_stable_bandgap_dim20.random.model")
    # embeddings = model.vectors
    # converter = lambda x: x
    # dim = 20

    # model = Glove.load("../out/all_stable_bandgap_dim20.glove.model")
    # embeddings = model.word_vectors
    # converter = lambda x: x.lower()
    # dim = 20

    model = OneHotVectors.load("../out/all_stable_bandgap_dim20.one_hot.model")
    embeddings = model.vectors
    converter = lambda x: x
    dim = 89

    df = pd.read_pickle("../out/all_stable_bandgap.pkl")

    # regression, args = LinearRegression, {}
    regression, args = RandomForestRegressor, {"n_estimators": 100, "n_jobs": 4}
    # regression, args = MLPRegressor, {"hidden_layer_sizes": (100,), "max_iter": 500}

    # pool = np.mean
    pool = np.max

    borep_dim = 200

    W = np.random.uniform(low=-1/np.sqrt(dim), high=1/np.sqrt(dim), size=(borep_dim, dim))

    X = []
    y = []
    for i in range(len(df['structure'])):
        struct = df['structure'][i]
        band_gap = df['band_gap'][i]

        # if band_gap == 0.0: continue

        vectors = []
        for element in struct.species:
            atom_vector = np.array(embeddings[model.dictionary[converter(element.name)]])
            vectors.append(np.dot(W, atom_vector))
        X.append(pool(vectors, axis=0))
        y.append(band_gap)

    cv_results = cross_validate(regression(**args), X, y, cv=10, return_estimator=True,
                                scoring=('r2', 'neg_root_mean_squared_error'))
    # the r2 score is the coefficient of determination, R^2, of the prediction
    print(cv_results['test_r2'])
    print(cv_results['test_neg_root_mean_squared_error'])

    print("mean fold r2 score: %s" % np.mean(cv_results['test_r2']))
    print("std fold r2 score: %s" % np.std(cv_results['test_r2']))
    print("mean fold neg_root_mean_squared_error score: %s" % np.mean(cv_results['test_neg_root_mean_squared_error']))
    print("std fold neg_root_mean_squared_error score: %s" % np.std(cv_results['test_neg_root_mean_squared_error']))
