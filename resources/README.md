
The file `all_stable_bandgap_electronegativities.csv` was created based on the atoms occurring in the walks corpus
`all_stable_bandgap.node2vec.walks`. The electronegativity for an atom was obtained from `electronegativities2.csv`
if a value for that atom exists in the file, otherwise it was obtained from `electronegativities.csv`.

The data in the file `electronegativities.csv` was obtained from: 
https://en.wikipedia.org/wiki/Electronegativities_of_the_elements_(data_page)#Electronegativity_(Pauling_scale)

The data in the file `electronegativities2.csv` was obtained from: 
https://en.wikipedia.org/wiki/Electronegativities_of_the_elements_(data_page)#Electronegativity_(Allen_scale)

The data in `all_stable_bandgap_atomic_radii.csv` was created from the pymatgen values associated with the 
corresponding Element class, using the "Atomic radius" value, and the "Atomic radius calculated" value if the former
had a value of "no data".
