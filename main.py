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

    df_reddit = _load_data()


main()
