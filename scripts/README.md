

### PCA on the Mean Atom Vector for a Compound

With atom vectors in hand, one way to represent a compound (such as Bi<sub>2</sub>Se<sub>3</sub>, for example) is to 
take the mean of the atom vectors for that compound, i.e. `mean {Bi_v, Bi_v, Se_v, Se_v, Se_v}` where `Bi_v` and `Se_v` 
represent the atom vectors for Bi and Se, respectively.

It is interesting to ask if there is a relationship between this kind of representation for a compound and its band 
gap value. The following command will compute the mean atom vectors for each of the ~33,000 compounds in the 
`out/all_stable_bandgap.pkl` dataset, perform PCA on them, and plot the first two components against eachother:
```
python pca_mean_grave_vectors.py
```

The following plots are the result:

<img alt="" src="../resources/pca_mean_grave_vectors.png">

Each point represents a compound, colored according to its band gap value, with darker points representing a lower 
value. The plot on the right is the same as the one on the left, except that the compounds where the band gap is 
exactly 0 have been excluded, as about half of the compounds have a band gap value of 0.

For the plots above, the GraVe embeddings that incorporate a continuous electronegativity feature were used to 
represent an atom in a compound.

For comparison, random vectors were assigned to the elements of the dataset, and the same procedure was carried out:
```
python pca_mean_random_vectors.py
```

<img alt="" src="../resources/pca_mean_random_vectors.png">

### Regression with the Mean Atom Vector for a Compound to Predict Band Gap Energies

Mean atom vectors were computed for each of the ~33,000 compounds in the `out/all_stable_bandgap.pkl` dataset, and a
Random Forest Regression model was trained on these mean atom vectors and their corresponding band gaps. The results 
are displayed in the following table:

Atom Vectors             |  Random Forest, R<sup>2</sup>   | MLP, R<sup>2</sup> |
-------------------------|--------------------------------:|-------------------:|   
GraVe<i><sup>1</sup></i> | 0.693 ± 0.0148 (0.559 ± 0.0216) | 0.630 ± 0.0183     |
GloVe                    | 0.705 ± 0.0122 (0.577 ± 0.0208) | 0.590 ± 0.0176     |
Random                   | 0.697 ± 0.0118 (0.561 ± 0.0186) | 0.700 ± 0.0141     |                         
One-hot                  | 0.849 ± 0.0148 (0.775 ± 0.0270) | 0.883 ± 0.0158     |

<i>The Random Forest Regression model utilized 100 estimators. 
The MLP consisted of 1 hidden layer with 100 neurons, and was trained with the ADAM optimizer.
Score values represent the mean 10-fold cross-validation result.
The values in parentheses are the scores for a dataset in which the examples with a band gap of 0 were removed.</i>

<i><sup>1</sup> embeddings jointly trained with a single, continuous electronegativity feature</i> 
