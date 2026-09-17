# %%

import praw
import urllib.request
import pdfplumber
# import xmltodict
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

    print("\n\n Nombre de posts Reddit collectés :", len(textes_Reddit))

    # Conversion du texte Reddit en DataFrame
    df_reddit = pd.DataFrame(textes_Reddit, columns = ['texte'])

    # On spécifie l'origine des données (Reddit)
    df_reddit['origine'] = 'Reddit'

    df_reddit.to_csv('data/df_reddit.csv', index_label='id', sep='\t')


def func_read_csv_reddit():

    return pd.read_csv('data/df_reddit.csv', sep='\t')


def func_fetch_data_arxiv():

    # Initialisation du client
    client = arxiv.Client(
        page_size=10,
        delay_seconds=3.0,  # Respecte la politique de rate limit d'arXiv
        num_retries=3
    )

    # Recherche par mots-clés ou catégorie (ex: Computer Vision / cs.CV)
    search = arxiv.Search(
        query="cat:cs.CV AND deep learning",
        max_results=5,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    textes = []

    for result in client.results(search):

        # Téléchargement du PDF
        pdf_path = result.download_pdf(dirpath="papers")

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                textes.append(page.extract_text or '')

    df_arxiv = pd.DataFrame(textes, columns = ['text'])

    df_arxiv['origine'] = 'Arxiv'

    df_arxiv.to_csv('data/df_arxiv.csv', index_label = 'id', sep='\t')

def func_read_csv_arxiv():

    return pd.read_csv('data/df_arxiv.csv', sep='\t')


def main():

    if os.path.isfile('data/df_data_reddit.csv'):
        func_fetch_data_reddit()
    df_reddit = func_read_csv_reddit()

    func_fetch_data_arxiv()
    df_arxiv = func_read_csv_arxiv()


main()
# %%
