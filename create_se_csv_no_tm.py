import pandas as pd
import numpy as np
from utils import build_transition_metal_minus_list

if __name__ == '__main__':
    df = pd.read_pickle("out/all_selenium_2020-11-05.pkl")

    names = {}
    elements = {i: 0 for i in range(1, 119)}

    counts = {1: 0, 2: 0, 3: 0, 4: 0, 5:0}
    tot_num_atoms = []
    num_atoms_dist = {"1<=x<10": 0, "10<=x<20": 0, "20<=x<40": 0, "x>=40": 0}

    tm = build_transition_metal_minus_list()

    with open("all_se_no_tm.csv", "wt") as f:
        f.write("pretty_formula,unit_cell_formula,num_atoms_in_unit_cell\n")

        for i in range(len(df['structure'])):
            struct = df['structure'][i]

            if any([symbol in tm for symbol in struct.symbol_set]):
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
