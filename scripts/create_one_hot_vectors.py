from grave import FactorizationMachine
from utils import OneHotVectors


if __name__ == '__main__':

    fm = FactorizationMachine.load_model("../out/all_stable_bandgap_dim20.fm.ctx10_add_cont.model")
    atom_vectors = fm.W

    elems = list(fm.dictionary.keys())

    ohv = OneHotVectors(elems=elems)

    ohv.save("all_stable_bandgap_dim20.one_hot.model")
