# Guide modélisation succès

Cette partie du projet se concentre sur la modélisation du succès de
l'essai clinique. On prend pour donnée la durée de vie de l'essai, par
une variable utilisée dans le modèle de durée de vie
['TimePassed']{style="color:red;"}. Le dossier `Durée Essai clinique`
quant à lui se concentre sur des modèles de durée.

Dans cette partie, on cherche à déterminer les facteurs non médicaux qui
conduisent à la réussite d'un essai clinique en phase III, c'est à dire
le passage à la phase supérieure. On ne travaille que sur les essais qui
ont dépassé la phase III, soldé par le succès ou l'échec, c'est-à-dire
l'abandon (pas la suspension).

# Données d'entrainements

Les données sont dans le dossier "succès essai clinique", du nom de
`ctg-studies`. Elles ont été téléchargées sur ClinicalTrials.gov, avec
les critères qui conviennent. Toutefois, un script dans la branche
"data-exploration" permet aussi de scrapper ces données. Ce script étant
long à mettre en oeuvre, nous mettons à disposition du lecteur les
données, téléchargées grâce au package git-lfs (large files storage),
qui permet de push des fichiers volumineux (supérieurs à 100MB).

Une fois téléchargées en local, les données doivent être uploadées dans
le dossier `Succès Essai Clinique`.

On ajoute aussi des données issues de Clinical Trials sur les études
précédentes et en cours des Sponsors de chaque étude de notre dataset.

Enfin, on utilise le modèle de complexité des critères d'éligibilité
développé dans la partie Modélisation, dans la colonne
"Eligibility_Criteria".

# Entrainement du modèle

Etant donné la distribution très inégale des deux classes, succès et
échec, variable dépendante de notre étude, on se propose d'intégrer des
pondérations pour les classes à notre modèle. Nous avons étudié les
implications d'un tel choix en amont à la lecture de cet article :
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9542776/#M0011.

## Principaux résultats

-   Pour les modèles étudiés, le nombre de critère spécifiques du profil
    du patient à bien un impact significatif et négatif sur le succès
    d'un essai clinique.
-   Le type de sponsor ne semble pas impacter beaucoup le succès d'un
    essai clinique, pour ce qui est de la typologie public/privé; ce qui
    est aussi le caas des sponsors les plus prolifiques.
-   La présence d'un placebo dans l'étude a un impact négatif
    significatif.
-   Comme attendu, le choix d'un sujet "populaire" a un impact positif.
