import os
import json
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from shutil import copyfile
import csv
import re
from modules.data_extraction import *
from spacy.lang.en import English

print('Processing ...')
nlp = English()
print(os.getcwd())
inputpath = f"./data_chia"
outputpath = f"./data_bio"
trainpath = f"./trains"
testpath = f"./tests"


inputfiles = set()
for f in os.listdir(inputpath):
    if f.endswith('.ann'):
        inputfiles.add(f.split('.')[0].split('_')[0])

select_types = ['Condition', 'Drug', 'Procedure','Observation', 'Person', 'Mood']

brat_to_bio(inputfiles, inputpath, outputpath, select_types)

chia_datasets = split_train_test(inputfiles, train=0.8)


# Merge BIO format train, validation and test datasets
# chia_datasets = json.load(open("chia/chia_datasets.json", "r", encoding="utf-8"))
# merge the train dataset
with open("./data/train.txt", "w", encoding="utf-8") as f:
    for fid in chia_datasets["train"]:
        copyfile(f"{outputpath}/{fid}_exc.bio.txt", f"{trainpath}/{fid}_exc.bio.txt")
        copyfile(f"{outputpath}/{fid}_inc.bio.txt", f"{trainpath}/{fid}_inc.bio.txt")
        with open(f"{outputpath}/{fid}_exc.bio.txt", "r", encoding="utf-8") as fr:
            txt = fr.read().strip()
            if txt != '':
                f.write(txt)
                f.write("\n\n")
        with open(f"{outputpath}/{fid}_inc.bio.txt", "r", encoding="utf-8") as fr:
            txt = fr.read().strip()
            if txt != '':
                f.write(txt)
                f.write("\n\n")

# merge the validation dataset
with open("./data/dev.txt", "w", encoding="utf-8") as f:
    for fid in chia_datasets["dev"]:
        copyfile(f"{outputpath}/{fid}_exc.bio.txt", f"{trainpath}/{fid}_exc.bio.txt")
        copyfile(f"{outputpath}/{fid}_inc.bio.txt", f"{trainpath}/{fid}_inc.bio.txt")
        with open(f"{outputpath}/{fid}_exc.bio.txt", "r", encoding="utf-8") as fr:
            txt = fr.read().strip()
            if txt != '':
                f.write(txt)
                f.write("\n\n")
        with open(f"{outputpath}/{fid}_inc.bio.txt", "r", encoding="utf-8") as fr:
            txt = fr.read().strip()
            if txt != '':
                f.write(txt)
                f.write("\n\n")

# merge the test dataset
with open("./data/test.txt", "w", encoding="utf-8") as f:
    for fid in chia_datasets["test"]:
        copyfile(f"{outputpath}/{fid}_exc.bio.txt", f"{testpath}/{fid}_exc.bio.txt")
        copyfile(f"{outputpath}/{fid}_inc.bio.txt", f"{testpath}/{fid}_inc.bio.txt")
        with open(f"{outputpath}/{fid}_exc.bio.txt", "r", encoding="utf-8") as fr:
            txt = fr.read().strip()
            if txt != '':
                f.write(txt)
                f.write("\n\n")
        with open(f"{outputpath}/{fid}_inc.bio.txt", "r", encoding="utf-8") as fr:
            txt = fr.read().strip()
            if txt != '':
                f.write(txt)
                f.write("\n\n")

txt_to_df("./data/train.txt","./data/train2.csv")
txt_to_df("./data/test.txt","./data/test2.csv")
txt_to_df("./data/dev.txt","./data/dev2.csv")

print('Done !')