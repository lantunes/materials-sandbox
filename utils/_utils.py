

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


def build_label_color_map(resources_path="resources"):
    label_color_map = {}
    with open("%s/all_stable_bandgap_electronegativities.csv" % resources_path) as f:
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


def build_marker_size_map(resources_path="resources"):
    marker_size_map = {}
    with open("%s/all_stable_bandgap_atomic_radii.csv" % resources_path) as f:
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


def color_by_band_gap(bg):
    if bg < 0.1:
        return "#0515ff"
    if 0.1 <= bg < 1.0:
        return "#2e3bff"
    if 1.0 <= bg < 2.0:
        return "#4d58ff"
    if 2.0 <= bg < 3.0:
        return "#6670ff"
    if 3.0 <= bg < 4.0:
        return "#848cfa"
    if 4.0 <= bg <= 5.0:
        return "#a3a9ff"
    if bg > 5.0:
        return "#c2c6ff"


def get_label_by_band_gap(bg):
    if bg < 0.1:
        return "A"
    if 0.1 <= bg < 1.0:
        return "B"
    if 1.0 <= bg < 2.0:
        return "C"
    if 2.0 <= bg < 3.0:
        return "D"
    if 3.0 <= bg < 4.0:
        return "E"
    if 4.0 <= bg <= 5.0:
        return "F"
    if bg > 5.0:
        return "G"


def build_electronegativity_map(resources_path="resources"):
    m = {}
    with open("%s/all_stable_bandgap_electronegativities.csv" % resources_path) as f:
        for line in f.readlines():
            element, electronegativity = line.strip().split(",")
            m[element] = float(electronegativity)
    return m
