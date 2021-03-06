from grave import FactorizationMachine
from utils import RandomVectors


if __name__ == '__main__':

    fm = FactorizationMachine.load_model("../out/all_stable_bandgap_dim20.fm.ctx10_add_cont.model")
    atom_vectors = fm.W

    elems = list(fm.dictionary.keys())

    rv = RandomVectors(elems=elems, dim=20, mean=0, std=1)

    rv.save("../out/all_stable_bandgap_dim20.random.model")
