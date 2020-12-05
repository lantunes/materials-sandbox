import pandas as pd
import numpy as np
from utils import build_transition_metal_minus_list
from pymatgen import Composition, Element


if __name__ == '__main__':
    df = pd.read_pickle("out/all_selenium_2020-11-05.pkl")

    names = {}
    elements = {i: 0 for i in range(1, 119)}

    counts = {1: 0, 2: 0, 3: 0, 4: 0, 5:0}
    tot_num_atoms = []
    num_atoms_dist = {"1<=x<10": 0, "10<=x<20": 0, "20<=x<40": 0, "x>=40": 0}

    transition_metals = build_transition_metal_minus_list()
    binary_incl = [
        Composition({Element("Ti"): 1, Element("Se"): 2}),
        Composition({Element("Hf"): 1, Element("Se"): 2}),
        Composition({Element("Cu"): 2, Element("Se"): 1}),
        Composition({Element("Ag"): 2, Element("Se"): 1})
    ]

    contains_only_se = lambda s: len(s.symbol_set) == 1

    """
    "...we can also include any compound that can be formed by adding those binary formula units to another formula unit 
    already in our list. For example: SnSe2 is already in our list, so Cu2SnSe3 can be included too, because its 
    formula unit is SnSe2 + Cu2Se"
    """
    incl_set = set()
    for i in range(len(df['structure'])):
        struct = df['structure'][i]
        for b in binary_incl:
            if not any([symbol in transition_metals for symbol in struct.symbol_set]) and not contains_only_se(struct):
                incl_set.add((struct.composition.reduced_composition + b).reduced_formula)

    contains_more_electronegative = lambda s: any([a in ["O", "S", "F", "Cl", "Br"] for a in s.symbol_set])

    with open("all_se_no_tm_incl_binary_no_oxides_no_elem_se.csv", "wt") as f:
        f.write("pretty_formula,unit_cell_formula,num_atoms_in_unit_cell\n")

        for i in range(len(df['structure'])):
            struct = df['structure'][i]

            incl = False
            if struct.composition.reduced_formula in ["TiSe2", "HfSe2", "Cu2Se", "Ag2Se"]:
                incl = True
                print("*** %s, %s" % (struct.composition.reduced_formula, struct.composition.formula))

            if struct.composition.reduced_formula in incl_set:
                incl = True
                print("### %s, %s" % (struct.composition.reduced_formula, struct.composition.formula))

            if any([symbol in transition_metals for symbol in struct.symbol_set]) and not incl:
                continue

            if contains_more_electronegative(struct) or contains_only_se(struct):
                continue

            print("%s, %s" % (struct.composition.formula, struct.composition.reduced_formula))

            pretty_formula = struct.composition.reduced_formula
            unit_cell_formula = struct.composition.formula
            num_atoms_in_unit_cell = struct.num_sites

            f.write("%s,%s,%s\n" %(pretty_formula, unit_cell_formula, num_atoms_in_unit_cell))

            t = len(struct.types_of_species)
            if t < 5:
                counts[t] += 1
            else:
                counts[5] += 1

            tot_num_atoms.append(num_atoms_in_unit_cell)

            if 1 <= num_atoms_in_unit_cell < 10:
                num_atoms_dist["1<=x<10"] += 1
            elif 10 <= num_atoms_in_unit_cell < 20:
                num_atoms_dist["10<=x<20"] += 1
            elif 20 <= num_atoms_in_unit_cell < 40:
                num_atoms_dist["20<=x<40"] += 1
            else:
                num_atoms_dist["x>=40"] += 1

    print(counts)
    print(len(tot_num_atoms))
    print(num_atoms_dist)
    print(np.mean(tot_num_atoms))
