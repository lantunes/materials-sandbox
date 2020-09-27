import pandas as pd
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.analysis.local_env import CrystalNN
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':

    """
    >>> df = pd.read_pickle("out/selenium_stable_bandgap.pkl")
    
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>
    
    >>> len(df)
    1830
    
    >>> df.columns
    Index(['structure', 'band_gap'], dtype='object')
    
    >>> type(df['structure'])
    <class 'pandas.core.series.Series'>
    
    >>> type(df['structure'][0])
    <class 'pymatgen.core.structure.Structure'>
    
    >>> print(df['structure'][0])
    Full Formula (Lu1 Tl1 Se2)
    Reduced Formula: LuTlSe2
    abc   :   8.125496   8.125496   8.125495
    angles:  29.329221  29.329221  29.329219
    Sites (4)
      #  SP           a         b         c    magmom
    ---  ----  --------  --------  --------  --------
      0  Lu    0         0         0                0
      1  Tl    0.5       0.5       0.5             -0
      2  Se    0.733155  0.733155  0.733155         0
      3  Se    0.266845  0.266845  0.266845         0
      
    >>> type(df['band_gap'])
    <class 'pandas.core.series.Series'>
    
    >>> type(df['band_gap'][0])
    <class 'numpy.float64'>
    
    >>> print(df['band_gap'][0])
    1.2344
    """
    # df = pd.read_pickle("out/selenium_stable_bandgap.pkl")
    df = pd.read_pickle("out/all_stable_bandgap.pkl")

    names = {}
    elements = {i: 0 for i in range(1, 119)}

    for i in range(len(df['structure'])):
        struct = df['structure'][i]

        # if struct.formula == "Li2 Zn2":
        #     struct = struct*2
        #     gr = StructureGraph.with_local_env_strategy(struct, CrystalNN())
        #     labels = {i:spec.name for i, spec in enumerate(struct.species)}
        #     nx.draw(gr.graph, pos=nx.shell_layout(gr.graph), with_labels=True, labels=labels)
        #     plt.show()
        #     break

        # if 'Li' in struct.symbol_set:
        #     print(struct.formula)

        for spec in struct.species:
            if not spec.name in names:
                names[spec.name] = 0
            names[spec.name] += 1

            elements[spec.number] += 1

    print(len(df))
    print(len(names))
    print(names)
    for i in sorted(elements):
        print(i, elements[i])
