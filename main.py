# import numpy as np
# import json
# import pickle
# import datetime
import pandas as pd
import arxiv
import os
from dotenv import load_dotenv

# Librairies projet
from API.reddit import func_fetch_data_reddit
from API.arxiv import func_fetch_data_arxiv

load_dotenv() 

def _load_data_reddit() -> pd.DataFrame:

    # Si les données Reddit ne sont pas dispo en local
    if not os.path.isfile("data/df_reddit.csv"):

        # On requête l'API Reddit pour les récupérer
        func_fetch_data_reddit()

    return pd.read_csv("data/df_reddit.csv", sep="\t")


def _load_data_arxiv() -> pd.DataFrame:

    # Si les données Arxiv ne sont pas dispo en local
    if not os.path.isfile("data/df_arxiv.csv"):

        # On requête l'API Arxiv pour les récupérer
        func_fetch_data_arxiv()
    
    return pd.read_csv("data/df_arxiv.csv", sep="\t")


def _load_data() -> pd.DataFrame:

    df_reddit = _load_data_reddit()
    df_arxiv = _load_data_arxiv()

    return pd.concat([df_reddit, df_arxiv])
    


def main():

    df = _load_data()

    # 3.1
    print(f'Nombre de documents : {len(df)}\n') 

    # id des lignes à supprimer du DataFrame
    list_id_row_to_drop = []

    # 3.2 
    for row in df.itertuples():
        print(f'Document {row.id}')
        print(f'Mots : {len(row.text.split())}')
        print(f'Phrases : {len(row.text.split('.'))}\n')

        # Si le document contient moins de 100 caractères
        if len(row.text) < 100:

            # On l'ajoute à la liste des éléments à supprimer
            list_id_row_to_drop.append(row.id)

        # On supprimme toutes les lignes contenant moins de 100 caractères
        df.drop(index = list_id_row_to_drop)

    all_docs = ' '.join(df['text'])
    pass

    
if __name__ == '__main__':
    main()
