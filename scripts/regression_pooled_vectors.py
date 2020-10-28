import numpy as np
import pandas as pd
from utils import RandomVectors, OneHotVectors, OrbitalDescriptors
from grave import FactorizationMachine
from sklearn.linear_model import LinearRegression
from glove import Glove
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_validate

if __name__ == '__main__':

    # model = FactorizationMachine.load_model("../out/all_stable_bandgap_dim20.fm.ctx10_add_cont.model")
    # embeddings = model.W
    # converter = lambda x: x

    model = RandomVectors.load("../out/all_stable_bandgap_dim20.random.model")
    embeddings = model.vectors
    converter = lambda x: x

    # model = OrbitalDescriptors(valence=True)
    # embeddings = model.vectors
    # converter = lambda x: x

    # model = Glove.load("../out/all_stable_bandgap_dim20.glove.model")
    # embeddings = model.word_vectors
    # converter = lambda x: x.lower()

    # model = OneHotVectors.load("../out/all_stable_bandgap_dim20.one_hot.model")
    # embeddings = model.vectors
    # converter = lambda x: x

    df = pd.read_pickle("../out/all_stable_bandgap.pkl")

    # regression, args = LinearRegression, {}
    regression, args = RandomForestRegressor, {"n_estimators": 100, "n_jobs": 4}
    # regression, args = MLPRegressor, {"hidden_layer_sizes": (100,), "max_iter": 500}

    # pool = np.mean
    pool = np.max

    exclude_zero = False
    # exclude_zero = True

    X = []
    y = []
    for i in range(len(df['structure'])):
        struct = df['structure'][i]
        band_gap = df['band_gap'][i]

        if band_gap == 0.0 and exclude_zero:
            continue

        vectors = []
        for element in struct.species:
            vectors.append(np.array(embeddings[model.dictionary[converter(element.name)]]))
        X.append(pool(vectors, axis=0))
        y.append(band_gap)

    cv_results = cross_validate(regression(**args), X, y, cv=10, return_estimator=True,
                                scoring=('r2', 'neg_root_mean_squared_error', 'neg_mean_absolute_error'))
    # the r2 score is the coefficient of determination, R^2, of the prediction
    print(cv_results['test_r2'])
    print(cv_results['test_neg_root_mean_squared_error'])
    print(cv_results['test_neg_mean_absolute_error'])

    print("mean fold r2 score: %s" % np.mean(cv_results['test_r2']))
    print("std fold r2 score: %s" % np.std(cv_results['test_r2']))
    print("mean fold neg_root_mean_squared_error score: %s" % np.mean(cv_results['test_neg_root_mean_squared_error']))
    print("std fold neg_root_mean_squared_error score: %s" % np.std(cv_results['test_neg_root_mean_squared_error']))
    print("mean fold neg_mean_absolute_error score: %s" % np.mean(cv_results['test_neg_mean_absolute_error']))
    print("std fold neg_mean_absolute_error score: %s" % np.std(cv_results['test_neg_mean_absolute_error']))

    # there is a trained estimator for each fold
    # estimator = cv_results['estimator'][0]

    estimator = regression(**args).fit(X, y)

    print("'Cd1 Ag2 I4', actual band gap: 2.0050000000000003")
    cd = np.array(embeddings[model.dictionary[converter("Cd")]])
    ag = np.array(embeddings[model.dictionary[converter("Ag")]])
    i = np.array(embeddings[model.dictionary[converter("I")]])
    print(estimator.predict(np.mean([cd, ag, ag, i, i, i, i], axis=0).reshape(1, -1)))

    print("'La1 Co1 Si3', actual band gap: 0.0")
    la = np.array(embeddings[model.dictionary[converter("La")]])
    co = np.array(embeddings[model.dictionary[converter("Co")]])
    si = np.array(embeddings[model.dictionary[converter("Si")]])
    print(estimator.predict(np.mean([la, co, si, si, si], axis=0).reshape(1, -1)))

    print("'Li2 Hf1 N2', actual band gap: 1.9339000000000004")
    li = np.array(embeddings[model.dictionary[converter("Li")]])
    hf = np.array(embeddings[model.dictionary[converter("Hf")]])
    n = np.array(embeddings[model.dictionary[converter("N")]])
    print(estimator.predict(np.mean([li, li, hf, n, n], axis=0).reshape(1, -1)))

    print("'Y2 Ni2 Ge4', actual band gap: 0.0")
    y_ = np.array(embeddings[model.dictionary[converter("Y")]])
    ni = np.array(embeddings[model.dictionary[converter("Ni")]])
    ge = np.array(embeddings[model.dictionary[converter("Ge")]])
    print(estimator.predict(np.mean([y_, y_, ni, ni, ge, ge, ge, ge], axis=0).reshape(1, -1)))
