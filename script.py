# %%

import praw
import urllib.request
import io
import pdfplumber
import xmltodict
# import numpy as np
# import json
# import pickle
# import datetime
import pandas as pd
import arxiv
import os
from dotenv import load_dotenv

load_dotenv()


def func_fetch_data_reddit():

    taille_docs=10

    # Récupération de textes depuis Reddit
    reddit = praw.Reddit(
        client_id=os.getenv('CLIENT_ID'), 
        client_secret=os.getenv('CLIENT_SECRET'),
        user_agent=os.getenv('USER_AGENT')
    )

    subr = reddit.subreddit('vosfinances')

    posts = list(subr.hot(limit=taille_docs))

    textes_Reddit = []
    for post in posts:

        # Titre toujours présent
        texte = post.title.replace("\n", " ") + ". "

        if post.selftext:
            texte += post.selftext.replace("\n", " ")


        textes_Reddit.append(texte)

    # print("\n\n Nombre de posts Reddit collectés :", len(textes_Reddit))

    # Conversion du texte Reddit en DataFrame
    df_reddit = pd.DataFrame(textes_Reddit, columns = ['texte'])

    # On spécifie l'origine des données (Reddit)
    df_reddit['origine'] = 'Reddit'

    df_reddit.to_csv('data/df_reddit.csv', index_label='id', sep='\t')


def func_read_csv_reddit():

    return pd.read_csv('data/df_reddit.csv', sep='\t')


def func_fetch_data_arxiv():


    # Recherche par mots-clés ou catégorie (ex: Quantitative Finance / q-fin.PM)
    url = "https://export.arxiv.org/api/query?search_query=all:investment&start=0&max_results=" + str(10)

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': '*/*'})

    texte_all_pdfs = []

    # Téléchargement du PDF en mémoire
    with urllib.request.urlopen(req) as response:
        xml_data = response.read().decode('utf-8')

        dict_arxiv = xmltodict.parse(xml_data)

    entries = dict_arxiv['feed'].get('entry', [])
    if isinstance(entries, dict):
        entries = [entries]

    print("Nombre d'articles Arxiv trouvés :", len(entries))

    textes_Arxiv = []
    for entry in entries:
        texte = entry['summary'].replace('\n', ' ').strip()
        textes_Arxiv.append(texte)

    for texte in textes_Arxiv[:5]:
        print("\n\n\n---")
        print(texte)

    df_arxiv = pd.DataFrame(textes_Arxiv, columns = ['text'])

    df_arxiv['origine'] = 'Arxiv'

    df_arxiv.to_csv('data/df_arxiv.csv', index_label = 'id', sep='\t')


def func_read_csv_arxiv():

    return pd.read_csv('data/df_arxiv.csv', sep='\t')


def main():

    if not os.path.isfile('data/df_reddit.csv'):
        func_fetch_data_reddit()
    df_reddit = func_read_csv_reddit()
    # print(df_reddit)

    if not os.path.isfile('data/df_arxiv.csv'):
        func_fetch_data_arxiv()
    df_arxiv = func_read_csv_arxiv()
    # print(df_arxiv)


main()
# %%
