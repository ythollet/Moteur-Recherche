import pandas as pd
import praw
import os

def func_fetch_data_reddit():
    """
    Récupère les données depuis Reddit
    """

    # Nombre de documents a récupérer
    taille_docs = 10

    # Récupération de textes depuis Reddit
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT"),
    )

    subr = reddit.subreddit("vosfinances")

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
    df_reddit = pd.DataFrame(textes_Reddit, columns=["text"])

    # On spécifie l'origine des données (Reddit)
    df_reddit["origine"] = "Reddit"

    df_reddit.to_csv("data/df_reddit.csv", index_label="id", sep="\t")
