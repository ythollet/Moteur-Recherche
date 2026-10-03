import ast
import html

import pandas as pd
import praw
import os

from Documment.document import Document
from Documment.reddit_document import RedditDocument


class Reddit:

    @staticmethod
    def _clean_str(
        in_str: str
    ) -> str:

        # Décodage des entités HTML et normalisation des espaces.
        return " ".join(html.unescape(in_str).split())



    @staticmethod
    def main_fetch_data():
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

        subr = reddit.subreddit("personalfinance")

        posts = list(subr.hot(limit=taille_docs))

        documents_reddit = []
        for post in posts:

            document = RedditDocument(
                titre = Reddit._clean_str(
                    in_str = post.title
                ),
                texte = Reddit._clean_str(
                    in_str = post.selftext
                ),
                url = post.url,
                date = post.created_datetime,
                auteur = post.author.name,
                origine = 'Reddit',
                nb_comments = post.num_comments,
            )

            documents_reddit.append(document)

        # Conversion du texte Reddit en DataFrame
        df_reddit = pd.DataFrame(documents_reddit)

        df_reddit.to_csv("RawData/reddit.csv", index=False, sep="\t")

    @staticmethod
    def _load_data_reddit() -> pd.DataFrame:

        # Si les données Reddit ne sont pas dispo en local
        if not os.path.isfile("RawData/reddit.csv"):
            # On requête l'API Reddit pour les récupérer
            Reddit.main_fetch_data()

        df = pd.read_csv(
            "RawData/reddit.csv",
            sep="\t",
            converters={"list_auteurs": ast.literal_eval}
        )

        return df
