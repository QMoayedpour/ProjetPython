# Exemple de module simple pour executer un module simplement depuis un terminal en spécifiant des arguments. On utilisera ce module pour importer les données
# Depuis un terminal simplement en spécifiant quelques arguments (taille de l'échantillon, keyword et fichier csv de sortie)
# Exemple d'utilisation (depuis un terminal): python GetCliniData.py --size 10 --keyword France --path My/File/Data.csv
# /!\ Attention, l'utilisation d'un keyword limite les résultats présentés par l'API, si la taille du dataset demandé est trop grande par rapport aux keyword indiqué, il risque d'y avoir un problème


import argparse

from utils.data_scrap_functions import *

from tqdm import tqdm

parser = argparse.ArgumentParser(description='Paramètre pour la récupération des données')

parser.add_argument('--size', type=int, help="Nombre d'essais cliniques à scrapper (en milliers)")

parser.add_argument('--keyword', type=str, help="[Optionnel] mot clé pour la recherche d'essais cliniques")

parser.add_argument('--path', type=str, help="Chemin d'accès où enregistrer (en CSV)")

args = parser.parse_args()

size = args.size

keyword = args.keyword

path = args.path

if keyword ==None:
    keyword =''

url = 'https://classic.clinicaltrials.gov/api/info/study_fields_list'

list_fields = get_list(url)

df = get_data_parralel(taille=size, list_fields=list_fields[:], keyword= keyword)

df.to_csv(path)