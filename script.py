# %%

import praw
import urllib.request
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


def func_get_data_reddit():

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

    # Cnversion du texte Reddit en DataFrame
    df_reddit = pd.DataFrame(textes_Reddit, columns = ['texte'])

    # On crée une colonne 'id'
    df_reddit = df_reddit.reset_index(names='id')

    # On spécifie l'origine des données (Reddit)
    df_reddit['origine'] = 'Reddit'

    return df_reddit


def func_get_data_arxiv():

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
    print("t")

    for result in client.results(search):
        print(f"Titre : {result.title}")
        print(f"Auteurs : {', '.join(a.name for a in result.authors)}")
        print(f"Date : {result.published.date()}")
        print(f"PDF : {result.pdf_url}")
        print(f"Résumé : {result.summary[:150]}...")
        print("-" * 40)


def main():

    df_reddit = func_get_data_reddit()
    print(df_reddit)


main()
# %%
