from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt


def afficher_colonnes_manquantes(df, seuil=0.95):
    """
    Affiche les colonnes d'un DataFrame ayant plus de seuil % de valeurs manquantes.

    Parameters:
    - df: Le DataFrame.
    - seuil: Le seuil (par défaut, 0.95 pour 95% de valeurs manquantes).
    """
    colonnes_manquantes = df.columns[df.isnull().mean() > seuil]
    
    if not colonnes_manquantes.empty:
        res = pd.DataFrame({
            'Colonne': colonnes_manquantes,
            'Nombre de valeurs manquantes': df[colonnes_manquantes].isnull().sum(),
            'Pourcentage de valeurs manquantes': df[colonnes_manquantes].isnull().mean() * 100
        }).reset_index(drop=True)
        
        print(tabulate(res, headers='keys', tablefmt='fancy_grid', showindex=False))
        print(f'Nombre de variables avec {seuil}% de valeurs manquantes :','\n', len(colonnes_manquantes))
    else:
        print("Aucune colonne avec plus de {:.0%} de valeurs manquantes.".format(seuil))


def plot_distribution_valeurs_manquantes(df):
    """
    Crée un graphique montrant la distribution des taux de valeurs manquantes.

    Parameters:
    - df: DataFrame a analyser
    """
    taux_valeurs_manquantes = df.isnull().mean().sort_values(ascending=False) * 100
    list_manq = taux_valeurs_manquantes.tolist()
    plt.figure(figsize=(12, 6))
    plt.plot(list_manq, marker='o', linestyle='-', color='skyblue')

    plt.title('Distribution des taux de valeurs manquantes')
    plt.xlabel('Nombre de variables')
    plt.ylabel('Taux de valeurs manquantes (%)')

    plt.show()