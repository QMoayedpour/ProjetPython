import pandas as pd
import requests
#import urllib
import re
from tqdm import trange
import time


def get_list(url):

    """
    Fonction pour récupérer la liste de variables des essais cliniques.
    inputs: url de l'API clinicaltrials 'https://classic.clinicaltrials.gov/api/info/study_fields_list'

    Returns:
        list: liste des variables accessibles depuis l'API clinical trials
    """
    resp = requests.get(url)
    texte = resp.text

    list_fields = re.findall('<Field Name=".*?"/>\n',texte)
    list_fields = [x[13:-4] for x in list_fields]
    return list_fields



def treat_list(x):
    """
    Fonction à appliquer au dataframe scrappé pour le "nettoyer"

    Args:
        x (list ou None): variable du dataframe

    Returns:
        str or None: variable 'néttoyée'
    """
    if type(x)==list:
        if len(x)>0:
            return x[0]
    else:
        return x



def get_data(taille=10,list_fields=['NCTId','StartDate','LastUpdatePostDate'],keyword=''):
    """
    Fonction de récupération des données d'essais cliniques à partir de l'API du site clinical Trials. 
    Inputs: 
    --Taille: Taille de l'échantillon à récupérer (en milliers) (int)
    --list_fields: Variables à récupérer (list)
    --keyword: mots clés pour la recherche d'essais cliniques (str)
    """
    full_df=pd.DataFrame() #On crée un dataframe vide
    http_time=0
    pandas_time=0
    itter=len(list_fields)//20 +1
    for j in trange(taille):
        df=pd.DataFrame()
        for i in range(itter):     #Itter sert à savoir combien de fois dois ittérer la boucle, étant donné que on ne peut récupérer les variables que 20 par 20  

            url_temp=f'https://classic.clinicaltrials.gov/api/query/study_fields?expr={keyword}&fields='
            fields='%2C'.join(list_fields[i*20:(i+1)*20]) #On join dans un string les variables à récupérer pour les intégrer dans l'url

            url_temp+=fields
            url_temp+=f'&min_rnk={j*1000+1}&max_rnk={(j+1)*1000}&fmt=json' #On intègre aussi le rank des données à récupérer

            st = time.time()

            req_temp = requests.get(url_temp)
            data_temp =req_temp.json()['StudyFieldsResponse']['StudyFields']

            et = time.time()

            http_time+= et - st

            st = time.time()

            df_temp = pd.DataFrame(data_temp).drop('Rank', axis=1)
            df=pd.concat([df, df_temp], axis=1) #On fusionne le dataframe temporelle avec le grand dataframe HORIZONTALEMENT car les 2 dataframe présentent les mêmes essais cliniques mais des variables différentes

            et = time.time()

            pandas_time+= et - st

        st = time.time()

        full_df=pd.concat([full_df,df],axis=0) #On fusionne maintenant verticalement les dataframe

        et = time.time()

        pandas_time+= et - st

    full_df = full_df.reset_index()
    full_df = full_df.drop('index',axis=1)
    full_df=full_df.applymap(treat_list)

    print("Temps requete API:" , '-'*20, http_time, '\n\n', 'Temps Pandas:', '-'*20, pandas_time)
    return full_df

