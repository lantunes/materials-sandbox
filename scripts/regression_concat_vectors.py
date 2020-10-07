import numpy as np
import pandas as pd
from grave import FactorizationMachine
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_validate
from utils import build_electronegativity_map


def get_electronegativity_embedding(embeddings, atom, electronegativities):
    electronegativity = electronegativities[atom]
    if electronegativity >= 3.0:
        return embeddings[89]
    elif 2.0 <= electronegativity < 3.0:
        return embeddings[90]
    elif 1.5 <= electronegativity < 2.0:
        return embeddings[91]
    else:
        return embeddings[92]


if __name__ == '__main__':
    model = FactorizationMachine.load_model("../out/all_stable_bandgap_dim20.fm.ctx10_or_1.model")
    embeddings = model.W

    df = pd.read_pickle("../out/all_stable_bandgap.pkl")

    # regression, args = LinearRegression, {}
    regression, args = RandomForestRegressor, {"n_estimators": 100, "n_jobs": 4}
    # regression, args = MLPRegressor, {"hidden_layer_sizes": (100,), "max_iter": 500}

    # pool = np.mean
    pool = np.max

    # BOREP
    borep = True
    dim = 40
    borep_dim = 200
    W = np.random.uniform(low=-1 / np.sqrt(dim), high=1 / np.sqrt(dim), size=(borep_dim, dim))

    electronegativities = build_electronegativity_map("../resources")

    X = []
    y = []
    for i in range(len(df['structure'])):
        struct = df['structure'][i]
        band_gap = df['band_gap'][i]

        # if band_gap == 0.0: continue

        vectors = []
        for element in struct.species:
            electronegativity_embedding = get_electronegativity_embedding(embeddings, element.name, electronegativities)
            atom_embedding = embeddings[model.dictionary[element.name]]
            vector = np.concatenate([atom_embedding, electronegativity_embedding])
            if borep:
                vector = np.dot(W, vector)
            vectors.append(vector)
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
