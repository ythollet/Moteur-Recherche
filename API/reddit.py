import pandas as pd
import praw
import os

from Documment.class_document import Document

class Reddit:

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

        subr = reddit.subreddit("vosfinances")

        posts = list(subr.hot(limit=taille_docs))

        documents_reddit = []
        for post in posts:

            document = Document(
                titre = post.title.replace("\n", " "),
                texte = post.selftext.replace("\n", " "),
                url = post.url,
                date = post.created_datetime,
                auteurs = post.author,
                origine = 'Reddit'
            )

            documents_reddit.append(document)

        # Conversion du texte Reddit en DataFrame
        df_reddit = pd.DataFrame(documents_reddit)

        df_reddit.to_csv("data/reddit.csv", index=False, sep="\t")
