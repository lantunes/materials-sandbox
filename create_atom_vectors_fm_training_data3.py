import grave
from grave import FactorizationMachine


if __name__ == '__main__':

    dim = 20
    context_window_size = 10
    feature_combiner = grave.addition_feature_combiner
    combiner = "add"
    name = "all_stable_bandgap_dim%s.fm.ctx%s_%s_cont_rad" % (dim, context_window_size, combiner)

    radii = {}
    with open("resources/all_stable_bandgap_atomic_radii.csv") as af:
        for line in af.readlines():
            element, radius = line.strip().split(",")
            val = float(radius)
            radii[element] = val

    feature_dict = {}
    with open("resources/all_stable_bandgap_electronegativities.csv") as f:
        for line in f.readlines():
            element, electronegativity = line.strip().split(",")
            val = float(electronegativity)
            feature_dict[element] = [float(electronegativity), radii[element]]

    fm = FactorizationMachine(dim=dim, y_max=100, alpha=0.75, context_window_size=context_window_size,
                              feature_combiner=feature_combiner)
    X, Y = fm.build_training_data("out/all_stable_bandgap.node2vec.walks", feature_dict, workers=4)

    fm.save("%s.training.model" % name)
    FactorizationMachine.save_training_data(X, Y, fm.dictionary, "%s.training.data" % name, sparsify=True)
