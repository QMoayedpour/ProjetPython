#Exemple de module simple pour executer un module simplement depuis un terminal en spécifiant des arguments. On utilisera ce module pour importer les données
#Depuis un terminal simplement en spécifiant quelques arguments (taille de l'échantillon, keyword et fichier csv de sortie)


import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))


#python GetCliniData.py 1 2 3 4 5 --sum