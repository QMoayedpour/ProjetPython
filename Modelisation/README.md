# Guide modélisation

Cette partie du projet se concentre sur la modélisation. 

L'entrainement de modèles de NLP étant particulièrement longue et demande beaucoup de données. Il a donc été décidé de donner les directives pour pouvoir re-entrainé le modèle à partir du code en y chargant les données d'entrainements.

# Données d'entrainements

Les données d'entrainements sont issues du dataset [CHIA](https://www.nature.com/articles/s41597-020-00620-0), qui ont été annotés à la main. Il est possible de les télécharger [ici](https://figshare.com/articles/dataset/Chia_Annotated_Datasets/11855817)

Une fois télécharger, les données doivent être uploadé dans le dossier ``data_chia``.

Le code pour extraire les données des fichier txt a été repris du git suivant: [clinical trials eligibility criteria ner](https://github.com/ctgatecci/Clinical-trial-eligibility-criteria-NER/blob/main/NER%20Preprocessing%20and%20Performance%20Analysis.ipynb)

# Entrainement du modèle

Pour entrainer le modèle. On "fine tune" un modèle BERT, l'entrainement peut être plutot long (environ 1h par epoch). Le paramètre "weight" permet de prendre en compte les poids des labels dans la fonction de pertes (par exemple pour éviter que le modèle "oublie" les labels rare).

# Charger le modèle

Pour l'instant pour charger le modèle, il faut avoir une copie du modèle en local et d'ensuite le transférer dans le dossier ```model`` lorsque l'on clone le git et le nommer "model1". Le fichier est trop volumineux pour être upload sur un git.


