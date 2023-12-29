# Guide modélisation durée

Cette partie du projet se concentre sur la modélisation de la durée de l'essai clinique. <span style="color:red;">On ne se concentre que sur la durée de l'essai clinique, pas si il a échoué ou non</span>. Le dossier ``Succès Essai clinique`` quant à lui étudie réellement la probabilité de succès de l'essai clinique.

Dans cette partie, on entraîne un modèle de NLP pour pouvoir compter les mots d'intérêts dans les critères d'éligibilités d'un essai clinique et on regrèsse ensuite la durée d'un essai clinique sur différentes variables.

L'entrainement de modèles de NLP étant particulièrement longue et demandant beaucoup de données, il a donc été décidé de donner les directives pour pouvoir re-entrainer le modèle à partir du code en y chargeant les données d'entrainement.

# Données d'entrainements

Les données d'entrainements sont issues du dataset [CHIA](https://www.nature.com/articles/s41597-020-00620-0), qui ont été annotés à la main. Il est possible de les télécharger [ici](https://figshare.com/articles/dataset/Chia_Annotated_Datasets/11855817)

Une fois téléchargées, les données doivent être uploadées dans le dossier ``data_chia``.

Une fois télécharger, utiliser le terminal depuis le dossier Modelisation et faire tourner la commande:

```bash
python data_to_bio.py
```

Cela devrait ajouter toute les données d'entrainements dans les dossiers adéquats.

Une autre méthode est de simplement faire tourner le notebook ``Notebook_datapreparation.ipynb`` pour obtenir les données d'entraînements sous format CSV.

Le code pour extraire les données des fichier txt a été repris du git suivant: [clinical trials eligibility criteria ner](https://github.com/ctgatecci/Clinical-trial-eligibility-criteria-NER/blob/main/NER%20Preprocessing%20and%20Performance%20Analysis.ipynb)

Les données sont transcrites au format BIO:
* B représente le début d'un groupe de mot
* I représente un mot qui appartient à un groupe de mot
* O représente le label "par défaut"

# Entrainement du modèle

Pour entrainer le modèle, on "fine tune" un modèle BERT, l'entrainement peut être plutot long (environ 1h par epoch). Le paramètre "weight" permet de prendre en compte les poids des labels dans la fonction de perte (par exemple pour éviter que le modèle "oublie" les labels rares).

Le modèle pré-entrainé BERT utilisé est le modèle [BioBert](https://arxiv.org/abs/1901.08746), qui a été entraîné sur un grand corpûs de publications médicales.

Si le fichier ``train.csv`` est bien présent dans le dossier ``data``, il suffit de faire tourner toute les cellules du notebook pour entrainer le modèle.

Le modèle obtient les résultats suivants:


|      Label      | Precision | Recall | F1-Score | Support |
|-----------------|-----------|--------|----------|---------|
| B-Condition     |   0.84    |  0.82  |   0.83   |  2038   |
| B-Drug          |   0.88    |  0.81  |   0.84   |   774   |
| B-Mood          |   0.47    |  0.21  |   0.30   |    42   |
| B-Observation   |   0.54    |  0.28  |   0.37   |   211   |
| B-Person        |   0.82    |  0.74  |   0.78   |   172   |
| B-Procedure     |   0.70    |  0.73  |   0.71   |   590   |
| I-Condition     |   0.77    |  0.76  |   0.76   |  1588   |
| I-Drug          |   0.73    |  0.73  |   0.73   |   358   |
| I-Mood          |   0.64    |  0.27  |   0.38   |    26   |
| I-Observation   |   0.38    |  0.11  |   0.17   |   249   |
| I-Person        |   0.00    |  0.00  |   0.00   |    27   |
| I-Procedure     |   0.70    |  0.69  |   0.69   |   531   |
| O               |   0.91    |  0.94  |   0.93   | 12545   |

|    Metric       |   Value   |
|-----------------|-----------|
| Accuracy        |   0.87    |
| Macro Avg       |   0.64    |
| Weighted Avg    |   0.86    |

On voit que certains labels sont rares et le modèle converge alors mal. Il est envisagé de re-entrainer le modèle mais cela demande un certains temps et de la puissance de calcul.

L'important est que on obtienne un bon score de "precision" sur les labels qui commence par "B" car c'est avec cela qu'on va compter le nombre d'attributs par essais cliniques.



# Application du modèle

Le modèle est ensuite utilisé dans le notebook ``Notebook_Conversion.ipynb``. Une fois le modèle appliqué, on peut alors créer des variables supplémentaires dans le dataframe qui compte le nombre d'apparition de chaque type de critère. On se servira ensuite de ces variables pour étudier si elles ont un impact sur la durée d'un essai cliniques, c'est à dire si le fait d'avoir des critères d'éligibilités très précis risque de rallonger la durée de l'essai clinique.

Le notebook sert essentiellement à montrer le traitement des données pour l'application du modèle et les difficultés rencontrés, toute les étapes ont ainsi été présentés dans le notebook.


# Charger le modèle

Pour l'instant pour charger le modèle, il faut avoir une copie du modèle en local et d'ensuite le transférer dans le dossier ``model`` lorsque l'on clone le git et le nommer "model1". Le fichier est trop volumineux pour être upload sur un git.

# Regression et Survival Analysis

Le notebook ``Notebook_regression`` présente les regréssions et analyse de survie effectuées. Ces regressions n'ont pas pour but de prédire la durée d'un essai clinique mais d'étudier les différents facteurs qui influent sur sa durée. On applique nos modèles à deux jeux de données, un échantillon de données en phase 3 auquel on a utiliser le modèle de NER pour compter les différents critères importants de chaque essai clinique, et autre échantillon, plus grand, présentant pratiquement l'ensemble des données cliniques disponibles sur le site [clinical-trials](https://clinicaltrials.gov/)(~450 000 essais cliniques).

## Principaux résultats

* Pour les modèles étudiés, le nombre de critère spécifiques du profil du patient à bien un impact significatif et positif sur la durée d'un essai clinique.
* Le type de sponsor ne semble pas impacter la durée d'un essai clinique.
* Le fait d'accepter les patients en bonne santés réduit l'espérance de durée de l'essai clinique.

Il y a plusieurs raisons qui font qu'un essais clinique est terminé. Soit il est validé, soit il est annulé, soit il est terminé mais n'a pas été validé. On étudie alors les determinants de l'échecs d'un essai clinique dans la partie ``Survie Essai clinique``.