from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
import numpy as np
from lifelines import KaplanMeierFitter


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


def data_treatment(df, filter=True):
    """Fonction pour traiter les dataframe

    Args:
        df (Dataframe): Dataframe de données clinical trials
        filter (bool, optional): Supprimer ou non les valeurs non pertinentes. Defaults to True.

    Returns:
        Dataframe: dataframe traité
    """
    df['StartDate'] = pd.to_datetime(df['StartDate'], format='%B %d, %Y', errors='coerce')
    df['CompletionDate'] = pd.to_datetime(df['CompletionDate'], format='%B %d, %Y', errors='coerce')
    # Créer une nouvelle colonne avec la différence en jours
    df['TimePassed'] = (df['CompletionDate'] - df['StartDate']).dt.days
    df['TimePassed'] = df['TimePassed'].fillna(0)
    df['Bin']=df['TimePassed'].apply(lambda x: 1 if x>5 else 0)
    if filter:
        df = df[df['Bin']==1].reset_index(drop=True) #On supprime les valeurs trop petites/protocoles non terminés (ou n'ayant pas de date de fin prévue)
        df = df[df['TimePassed']<1000].reset_index(drop=True) #On supprime aussi les valeurs trop élevés considérés comme des outliers (Seuil objectif)
       
    return df



def plot_survie(T, df, phase='Phase 3', comparaison="ALL"):
    """Fonction pour afficher la distribution kaplan meier de survie de l'échantillon. Cette methode n'est PAS paramétrique, on modelise simplement la probabilité 
    instantané de sortie selon le groupe. Rien n'est controllé (il peut par exemple y avoir des biais). Cette approche permet simplement d'avoir une intuition mais 
    ne peut pas être directement interprété.

    Args:
        T (series): serie des temps passés avant la completion date par essai clinique
        df (dataframe): dataframe lié à la série T
        phase (str, optional): phase à étudier. Defaults to 'Phase 3'.
        comparaison (str, optional): phase à comparer. "ALL" par défault.

    Raises:
        ValueError: Si la phase rentré n'est pas valide
    """
    ax = plt.subplot(111)
    m = (df["Phase"] == phase)
    kmf = KaplanMeierFitter()
    kmf.fit(durations = T[m], label = "Phase 3")
    kmf.plot_survival_function(ax = ax)
    if comparaison=="ALL":
        kmf.fit(T[~m], label = "Autre")  
    else:
        if comparaison not in df['Phase'].unique():
            list_poss = ", ".join(df['Phase'].dropna().unique())
            raise ValueError(f"'{comparaison}' n'est pas une valeur valide, veuillez choisir parmis les valeurs suivantes:",list_poss)     
        j = (df["Phase"] == comparaison)
        kmf.fit(T[j], label = comparaison) 

    kmf.plot_survival_function(ax = ax, at_risk_counts = True)
    plt.title("Survival of different gender group")