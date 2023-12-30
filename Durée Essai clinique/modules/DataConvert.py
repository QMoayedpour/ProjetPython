import re
import numpy as np
import pandas as pd
from tqdm import tqdm, trange
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .NER_functions import Bert_Model, data_treatment

def extract_inclusion_criteria(eligibility_criteria):
    if type(eligibility_criteria)!=str:
        return None
    match = re.search(r'Inclusion Criteria:(.*?)Exclusion Criteria:', eligibility_criteria, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    else:
        return None

def split_text_by_words(text, max_words=80):
    words = text.split()
    segments = []
    current_segment = []
    word_count = 0

    for word in words:
        if word_count  + 1 <= max_words:
            current_segment.append(word)
            word_count +=  1
        else:
            segments.append(' '.join(current_segment))
            current_segment = [word]
            word_count = len(word)

    segments.append(' '.join(current_segment))
    return segments

def count_attributes(pred, list_keys):
    dict_clini = {} # dict_clini est un dictionnaire qui repertorie le nombre de mots d'intérêts par catégorie.
    # On initialise le dictionnaire
    for elem in list_keys:
        dict_clini[elem]=0



    for i in pred:
        if i[1][0]=="B":
            if i[0][:2]!="##":
                dict_clini[i[1][2:]]+=1 #On rajoute 1 à la clé du compteur
    return dict_clini

    
class Data_Convertor(object):
    def __init__(self, path_df='../data/MyData.csv', path_model='./model/model1',):
        self.df = pd.read_csv(path_df).head(300)
        self.path_model = path_model
        self.cleaned = False
        
    def load(self, tags):
        print('Chargement du modèle ...', '\r')
        self.model = Bert_Model()
        self.model.load_model(self.path_model)
        self.model.getTag(tags)
        print('Modèle chargé !')
    def clean_data(self, col='EligibilityCriteria'):
        self.df = data_treatment(self.df)
        self.df['InclusionCriteria'] = self.df[col].apply(extract_inclusion_criteria)        
        self.cleaned = True

    def extract_predictions(self, phase='Phase 3'):
        if not self.cleaned:
            raise ValueError('Clean ur data first !')
        df_temp = self.df[(self.df['Phase']==phase) & (self.df['EligibilityCriteria']!="None") & (self.df['EligibilityCriteria']!="")][['NCTId','InclusionCriteria']]
        df_temp['InclusionCriteria'] = df_temp['InclusionCriteria'].fillna('').apply(split_text_by_words)
        if len(df_temp)==0:
            raise ValueError(f'DataFrame vide pour la condition {phase}')
        expanded_df = df_temp.explode('InclusionCriteria')
        expanded_df = expanded_df.fillna('')
        expanded_df = expanded_df[expanded_df['InclusionCriteria']!='']
        expanded_df.reset_index(drop=True, inplace=True)
        
        list_to_treat = expanded_df['InclusionCriteria'].tolist()
        preds = self.model.batch_predict(list_to_treat)
        del df_temp
        df_wait= pd.DataFrame() #Un autre dataframe temporaire
        df_wait['NCTId'] = expanded_df['NCTId']
        df_wait['Liste'] = preds

        df_merged = df_wait.groupby('NCTId')['Liste'].agg(sum).reset_index()
        df_merged = df_merged.fillna('')
        del df_wait
        list_preds = df_merged['Liste'].tolist()

        list_keys = [element[2:] for element in self.model.tag_values if element.startswith("B")]
        preds_dict_list = [count_attributes(elem, list_keys) for elem in list_preds]
        df_merged['raw_count'] = preds_dict_list
        self.df_predict = pd.merge(df_merged, self.df, how='inner', on='NCTId') 
        self.preds= preds

        # On réparti maintenant les observations dans des colonnes annexes (afin de pouvoir utiliser les variables facilement ensuite)

        colonnes_separees = self.df_predict['raw_count'].apply(pd.Series)
        colonnes_separees.rename(columns={'Condition': 'Conditions'}, inplace=True)
        self.df_predict = pd.concat([self.df_predict, colonnes_separees], axis=1)

    def save_preds(self, path='./data.csv'):
        self.df_predict.to_csv(path)
