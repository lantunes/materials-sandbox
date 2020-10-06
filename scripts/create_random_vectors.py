from grave import FactorizationMachine
import numpy as np
from utils import RandomVectors


if __name__ == '__main__':

    fm = FactorizationMachine.load_model("../out/all_stable_bandgap_dim20.fm.ctx10_add_cont.model")
    atom_vectors = fm.W

    mean = np.mean(atom_vectors, axis=0)
    std = np.std(atom_vectors, axis=0)
    elems = list(fm.dictionary.keys())

    rv = RandomVectors(elems=elems, dim=20, mean=mean, std=std)

    rv.save("../out/all_stable_bandgap_dim20.random.model")
