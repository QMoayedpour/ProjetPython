# Guide modélisation

Cette partie du projet se concentre sur la modélisation. 

L'entrainement de modèles de NLP étant particulièrement longue et demandant beaucoup de données, il a donc été décidé de donner les directives pour pouvoir re-entrainer le modèle à partir du code en y chargeant les données d'entrainement.

# Données d'entrainements

Les données d'entrainements sont issues du dataset [CHIA](https://www.nature.com/articles/s41597-020-00620-0), qui ont été annotés à la main. Il est possible de les télécharger [ici](https://figshare.com/articles/dataset/Chia_Annotated_Datasets/11855817)

Une fois téléchargées, les données doivent être uploadées dans le dossier ``data_chia``.

Il faut ensuite créer un dossier ``trains`` et un fichier ``tests``. C'est dans ce fichier que seront répartis les essais cliniques sous format B-I-O

La dernière étape est de simplement faire tourner le notebook ``Notebook_datapreparation.ipynb`` pour obtenir les données d'entraînements sous format CSV.

Le code pour extraire les données des fichier txt a été repris du git suivant: [clinical trials eligibility criteria ner](https://github.com/ctgatecci/Clinical-trial-eligibility-criteria-NER/blob/main/NER%20Preprocessing%20and%20Performance%20Analysis.ipynb)

# Entrainement du modèle

Pour entrainer le modèle, on "fine tune" un modèle BERT, l'entrainement peut être plutot long (environ 1h par epoch). Le paramètre "weight" permet de prendre en compte les poids des labels dans la fonction de perte (par exemple pour éviter que le modèle "oublie" les labels rares).

Si le fichier ``train.csv`` est bien présent dans le dossier ``data``, il suffit de faire tourner toute les cellules du notebook pour entrainer le modèle.

Le modèle obtient les résultats suivants:


|      Label      | Precision | Recall | F1-Score | Support |
|-----------------|-----------|--------|----------|---------|
| B-Condition     |   0.79    |  0.81  |   0.80   |  1729   |
| B-Drug          |   0.84    |  0.84  |   0.84   |   713   |
| B-Mood          |   0.27    |  0.14  |   0.19   |    42   |
| B-Observation   |   0.49    |  0.19  |   0.27   |   210   |
| B-Person        |   0.73    |  0.68  |   0.70   |   169   |
| B-Procedure     |   0.68    |  0.68  |   0.68   |   507   |
| I-Condition     |   0.75    |  0.75  |   0.75   |  1457   |
| I-Drug          |   0.66    |  0.75  |   0.70   |   335   |
| I-Mood          |   0.27    |  0.15  |   0.20   |    26   |
| I-Observation   |   0.27    |  0.14  |   0.19   |   242   |
| I-Person        |   0.00    |  0.00  |   0.00   |    27   |
| I-Procedure     |   0.74    |  0.65  |   0.69   |   501   |
| O               |   0.92    |  0.94  |   0.93   | 12157   |

|    Metric       |   Value   |
|-----------------|-----------|
| Accuracy        |   0.86    |
| Macro Avg       |   0.57    |
| Weighted Avg    |   0.85    |

On voit que certains labels sont rares et le modèle converge alors mal. Il est envisagé de re-entrainer le modèle mais cela demande un certains temps et de la puissance de calcul.

L'important est que on obtienne un bon score de "precision" sur les labels qui commence par "B" car c'est avec cela qu'on va compter le nombre d'attributs par essais cliniques.



# Application du modèle

Le modèle est ensuite utilisé dans le notebook ``Notebook_modelisation.ipynb``. Une fois le modèle appliqué, on peut alors créer des variables supplémentaires dans le dataframe qui compte le nombre d'apparition de chaque type de critère. On se servira ensuite de ces variables pour étudier si elles ont un impact sur la durée d'un essai cliniques, c'est à dire si le fait d'avoir des critères d'éligibilités très précis risque de rallonger la durée de l'essai clinique.


# Charger le modèle

Pour l'instant pour charger le modèle, il faut avoir une copie du modèle en local et d'ensuite le transférer dans le dossier ``model`` lorsque l'on clone le git et le nommer "model1". Le fichier est trop volumineux pour être upload sur un git.
