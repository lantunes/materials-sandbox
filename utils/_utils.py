

def color_by_label(label):
    if label in ["H", "Li", "Na", "K", "Rb", "Cs"]:
        return "red"
    if label in ["Be", "Mg", "Ca", "Sr", "Ba"]:
        return "brown"
    if label in ["B", "Al", "Ga", "In", "Tl"]:
        return "steelblue"
    if label in ["C", "Si", "Ge", "Sn", "Pb"]:
        return "purple"
    if label in ["N", "P", "As", "Sb", "Bi"]:
        return "blue"
    if label in ["O", "S", "Se", "Te"]:
        return "yellow"
    if label in ["F", "Cl", "Br", "I"]:
        return "cyan"
    if label in ["He", "Ne", "Ar", "Kr", "Xe"]:
        return "olive"
    if label in ["Ni", "Pd", "Pt", "Cu", "Ag", "Au", "Zn", "Cd", "Hg", "Rh", "Ir"]:
        return "orange"
    if label in ["Ti", "Zr", "Hf", "V", "Nb", "Ta", "Cr", "Mo", "W"]:
        return "green"
    if label in ["Fe", "Mn", "Tc", "Ru", "Re", "Os", "Co"]:
        return "lime"
    return "lightgray"


def build_label_color_map():
    label_color_map = {}
    with open("resources/all_stable_bandgap_electronegativities.csv") as f:
        for line in f.readlines():
            atom, elec = line.strip().split(",")
            val = float(elec)
            color = "gray"
            if val >= 3.0:
                color = "red"
            elif 2.0 <= val < 3.0:
                color = "orange"
            elif 1.5 <= val < 2.0:
                color = "lightblue"
            elif val < 1.5:
                color = "blue"
            label_color_map[atom] = color
    return label_color_map


def build_marker_size_map():
    marker_size_map = {}
    with open("resources/all_stable_bandgap_atomic_radii.csv") as f:
        for line in f.readlines():
            atom, radius = line.strip().split(",")
            val = float(radius)
            size = 4
            if val >= 2.0:
                size = 32
            elif 1.5 <= val < 2.0:
                size = 16
            elif 1.0 <= val < 1.5:
                size = 8
            marker_size_map[atom] = 3*size
    return marker_size_map
