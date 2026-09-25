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


def func_read_csv_reddit() -> pd.DataFrame:

    return pd.read_csv("data/df_reddit.csv", sep="\t")


def func_read_csv_arxiv() -> pd.DataFrame:

    return pd.read_csv("data/df_arxiv.csv", sep="\t")


def main():

    if not os.path.isfile("data/df_reddit.csv"):
        func_fetch_data_reddit()
    df_reddit = func_read_csv_reddit()
    # print(df_reddit)

    if not os.path.isfile("data/df_arxiv.csv"):
        func_fetch_data_arxiv()
    df_arxiv = func_read_csv_arxiv()
    # print(df_arxiv)
    pass


main()
