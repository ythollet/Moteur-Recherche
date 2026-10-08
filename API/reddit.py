import ast
import html
import pandas as pd
import praw
import os

from Documment.class_reddit_document import RedditDocument


class Reddit:

    @staticmethod
    def main_fetch_data():
        """
        Récupère les posts Reddit et les sauvegarde en CSV sur le disque.
        """

        # Récupération de textes depuis Reddit
        reddit = praw.Reddit(
            client_id = os.getenv("CLIENT_ID"),
            client_secret = os.getenv("CLIENT_SECRET"),
            user_agent = os.getenv("USER_AGENT"),
        )

        # Choix du subreddit
        subr = reddit.subreddit("personalfinance")

        # On récupère les posts
        posts = list(subr.hot(limit = 10))

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
                auteur = post.author.name,
                type = 'Reddit',
                nb_comments = post.num_comments,
            )
            for post
            in posts
        ]

        # Conversion du texte Reddit en DataFrame
        df_reddit = pd.DataFrame(documents_reddit)

        # On sauvegarde les données en CSV sur le disque
        df_reddit.to_csv("RawData/reddit.csv", index = False, sep = "\t")


    @staticmethod
    def _load_data_reddit() -> pd.DataFrame:
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
