import grave
from grave import FactorizationMachine
from math import isnan


if __name__ == '__main__':

    dim = 20
    context_window_size = 10
    feature = 1
    feature_combiner = grave.bitwise_or_feature_combiner
    combiner = "or"
    name = "all_stable_bandgap_dim%s.fm.ctx%s_%s_%s" % (dim, context_window_size, combiner, feature)

    feature_dict = {}
    with open("resources/all_stable_bandgap_electronegativities.csv") as f:
        for line in f.readlines():
            element, electronegativity = line.strip().split(",")
            val = float(electronegativity)
            if isnan(val):
                raise Exception("nan electronegativity for %s" % element)
            else:
                feature_dict[element] = [
                    feature if val >= 3.0 else 0,
                    feature if 2.0 <= val < 3.0 else 0,
                    feature if 1.5 <= val < 2.0 else 0,
                    feature if val < 1.5 else 0
                ]

    fm = FactorizationMachine(dim=dim, y_max=100, alpha=0.75, context_window_size=context_window_size,
                              feature_combiner=feature_combiner)
    X, Y = fm.build_training_data("out/all_stable_bandgap.node2vec.walks", feature_dict, workers=4)

    fm.save("%s.training.model" % name)
    FactorizationMachine.save_training_data(X, Y, fm.dictionary, "%s.training.data" % name, sparsify=True)
