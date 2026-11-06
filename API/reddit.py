import ast
import html
import pandas as pd
import praw
import os
from datetime import datetime, timezone
from pathlib import Path

from Documment.class_reddit_document import RedditDocument


class Reddit:

    @staticmethod
    def main_fetch_data():
        """
        Récupère les posts Reddit et les sauvegarde en CSV sur le disque.

        :raises ValueError: Si aucun texte exploitable n'est récupéré.
        """

        subreddits = ("personalfinance", "financialindependence", "Bogleheads")

        # Récupération de textes depuis Reddit
        reddit = praw.Reddit(
            client_id = os.getenv("CLIENT_ID"),
            client_secret = os.getenv("CLIENT_SECRET"),
            user_agent = os.getenv("USER_AGENT"),
        )

        # Récupère les publications populaires de chaque communauté.
        posts = []
        for nom_subreddit in subreddits:
            subr = reddit.subreddit(nom_subreddit)
            for post in subr.hot(limit = None):
                texte = Reddit._clean_str(in_str = post.selftext)
                # Même seuil que le corpus : écarte aussi les textes supprimés.
                if len(texte) < 100:
                    continue
                posts.append(post)

        # On stocke les posts sous forme de RedditDocument, dans une liste
        documents_reddit = [
            RedditDocument(
                titre = Reddit._clean_str(
                    in_str = post.title
                ),
                texte = Reddit._clean_str(
                    in_str = post.selftext
                ),
                url = post.url,
                date = post.created_datetime,
                auteur = post.author.name if post.author is not None else "",
                type = 'Reddit',
                nb_comments = post.num_comments,
            )
            for post
            in posts
        ]

        # Une collecte vide ne doit pas écraser les données déjà disponibles.
        if not documents_reddit:
            raise ValueError("Aucun texte Reddit exploitable n'a été récupéré.")

        # Conversion du texte Reddit en DataFrame
        df_reddit = pd.DataFrame(documents_reddit)

        # On sauvegarde les données en CSV sur le disque
        Path("RawData").mkdir(exist_ok = True)
        df_reddit.to_csv("RawData/reddit.csv", index = False, sep = "\t")
        print(f"Nombre de publications Reddit retenues : {len(df_reddit)}")


    @staticmethod
    def load_data_reddit() -> pd.DataFrame:
        """
        Charge le CSV Reddit si dispo en local, sinon effectue un appel API
        pour récupérer les données.

        :return: DataFrame des publications Reddit.
        """

        # Si les données Reddit ne sont pas dispo en local
        if not os.path.isfile("RawData/reddit.csv"):

            # On requête l'API Reddit pour les récupérer
            Reddit.main_fetch_data()

        # On sauvegarde les données en CSV sur le disque
        df = pd.read_csv(
            "RawData/reddit.csv",
            sep = "\t",
            converters = {"list_auteurs": ast.literal_eval}
        )

        return df


    @staticmethod
    def _clean_str(
        in_str: str
    ) -> str:
        """ Supprime les espaces insécables

        :param in_str: Texte à nettoyer.
        :return: Texte nettoyé.
        """

        # Décodage des entités HTML et normalisation des espaces.
        return " ".join(html.unescape(in_str).split())
