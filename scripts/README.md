

### PCA on the Mean Atom Vector for a Compound

With atom vectors in hand, one way to represent a compound (such as Bi<sub>2</sub>Se<sub>3</sub>, for example) is to 
take the mean of the atom vectors for that compound, i.e. `mean {Bi_v, Bi_v, Se_v, Se_v, Se_v}` where `Bi_v` and `Se_v` 
represent the atom vectors for Bi and Se, respectively.

It is interesting to ask if there is a relationship between this kind of representation for a compound and its band 
gap value. The following command will compute the mean atom vectors for each of the ~33,000 compounds in the 
`out/all_stable_bandgap.pkl` dataset, perform PCA on them, and plot the first two components against eachother:
```
python pca_mean_atom_vectors.py
```

The following plots are the result:

<img alt="" src="../resources/pca_mean_atom_vectors.png" width="800">

Each point represents a compound, colored according to its band gap value, with darker points representing a lower 
value. The plot on the right is the same as the one on the left, except that the compounds where the band gap is 
exactly 0 have been excluded, as about half of the compounds have a band gap value of 0.

For the plots above, the GraVe embeddings that incorporate a continuous electronegativity feature were used to 
represent an atom in a compound.

For comparison, random vectors were assigned to the elements of the dataset, and the same procedure was carried out:
```
python pca_mean_random_vectors.py
```

<img alt="" src="../resources/pca_mean_random_vectors.png" width="800">
