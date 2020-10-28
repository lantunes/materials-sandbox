import pymatgen
import numpy as np
import re

try:
    import cPickle as pickle
except ImportError:
    import pickle


ATOMS = ["Ag","I","Cd","La","Si","Co","Ge","Y","Ni","N","Li","Hf","Te","Th","Cu","Pt","Ga","Pr","Al","K","Se","Pd","Cs",
         "F","As","Rb","Tm","Sb","Lu","Mo","Nd","Hg","Pm","Yb","Sn","Zr","O","S","Na","Nb","P","Xe","Er","Fe","In","Pb",
         "Zn","Dy","Mn","Ti","Au","Ir","Cl","Mg","V","Ca","H","Tl","B","Ba","Sc","Ru","Gd","U","Bi","Br","Ta","Ce","Os",
         "Rh","Be","Re","Tb","Sm","Eu","C","Ho","Cr","Pu","Sr","Tc","Ac","Np","W","Pa","Kr","Ne","He","Ar"]

IDX = {"1s": 0, "2s": 2, "2p": 4, "3s": 10, "3p": 12, "3d": 18, "4s": 28, "4p": 30, "4d": 36, "5s": 46, "5p": 48,
       "4f": 54, "5d": 68, "5f": 78, "6s": 92, "6p": 94, "6d": 100, "7s": 110, "7p": 112}

DENSE_IDX = {"1s": 0, "2s": 1, "2p": 2, "3s": 5, "3p": 6, "3d": 9, "4s": 14, "4p": 15, "4d": 18, "5s": 23, "5p": 24,
       "4f": 27, "5d": 34, "5f": 39, "6s": 46, "6p": 47, "6d": 50, "7s": 55, "7p": 56}

RE = re.compile("([1-7])([spdf])([0-9]+)")


class OrbitalDescriptors:
    def __init__(self, elems=ATOMS, valence=False, dense=False):
        """
        elems: a list of strings with the names of the elements to be assigned an orbital vector
        """
        self.vectors = np.zeros(shape=(len(elems), 118 if not dense else 59))

        self.dictionary = {}
        for i, elem in enumerate(elems):
            self.dictionary[elem] = i
            if not valence:
                electrons = pymatgen.Element(elem).full_electronic_structure
                for level, orb, occup in electrons:
                    self._populate(i, level, orb, occup) if not dense else self._populate_dense(i, level, orb, occup)
            else:
                tokens = pymatgen.Element(elem).electronic_structure.split(".")
                for token in tokens:
                    found = RE.findall(token)
                    if found:
                        level, orb, occup = found[0]
                        self._populate(i, int(level), orb, int(occup)) if not dense else self._populate_dense(i, int(level), orb, int(occup))

    def _populate(self, i, level, orb, occup):
        idx = IDX["%s%s" % (level, orb)]
        for o in range(occup):
            self.vectors[i][idx + o] = 1.0

    def _populate_dense(self, i, level, orb, occup):
        idx = DENSE_IDX["%s%s" % (level, orb)]
        if orb == "s":
            stop = 1
        elif orb == "p":
            stop = 3
        elif orb == "d":
            stop = 5
        elif orb == "f":
            stop = 7
        else:
            raise Exception("unsupported orbital type: %s" % orb)
        for o in range(occup):
            self.vectors[i][idx + (o % stop)] += 0.5

    def save(self, filename):
        with open(filename, 'wb') as f:
            data = (self.elems, self.vectors, self.dictionary)
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            elems, vectors, dictionary = pickle.load(f)
            od = OrbitalDescriptors(elems=elems)
            od.vectors = vectors
            od.dictionary = dictionary
            return od
