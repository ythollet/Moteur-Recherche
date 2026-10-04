import ast
import os
import urllib
from typing import Any
import xmltodict
import pandas as pd

from Documment.arxiv_document import ArxivDocument


class Arxiv:
    """Regroupe la collecte et le chargement des articles Arxiv."""

    @staticmethod
    def fetch_data():
        """
        Récupère les articles, initialise des objets ArxivDocument, convertit en
        DataFrame et les sauvegarde en CSV sur le disque
        """

        # Les expressions sont encodées pour l'URL et reliées par un OU logique.
        # Le préfixe all recherche dans l'ensemble des champs de l'article
        # (titre, résumé, auteur).
        query = (
            'all:%22personal%20finance%22%20OR%20'
            'all:%22retail%20investor%22%20OR%20'
            'all:%22individual%20investor%22%20OR%20'
            'all:%22household%20finance%22'
        )

        # On construit l'URL
        url = (
            f"https://export.arxiv.org/api/query?"
            f"search_query={query}"
            f"&start=0"
            f"&max_results=10"
        )

        # On crée la requête
        req = urllib.request.Request(
            url,
            headers = {
                "User-Agent": "Moteur-Recherche/1.0"
            }
        )

        # On execute la requete
        with urllib.request.urlopen(req) as response:

            # On stocke le résultat XML
            xml_data = response.read().decode("utf-8")

            # On convertit le XML en dictionnaire Python
            dict_arxiv = xmltodict.parse(xml_data)

        # xmltodict renvoie un dictionnaire pour une entrée unique : on
        # convertit en liste pour consevrer le même format
        articles = dict_arxiv["feed"]["article"]
        if isinstance(articles, dict):
            articles = [articles]

        print("Nombre d'articles Arxiv trouvés :", len(articles))

        # On stocke les documents dans une liste
        documents_arxiv = []

        # pour chaque article
        for article in articles:

            # On init un objet ArxivDocument
            document = ArxivDocument(
                list_auteurs = Arxiv._get_authors_from_entry(article),
                texte = article['summary'].replace("\n", " ").strip(),
                url = article["id"],
                type = 'Arxiv',
                date = article["published"],
                titre = article["title"]
            )

            # On ajoute le document a la liste
            documents_arxiv.append(document)

        # Conversion: liste d'objets -> DataFrame
        df_arxiv = pd.DataFrame(documents_arxiv)

        # On exporte le DataFrame en CSV
        df_arxiv.to_csv("RawData/arxiv.csv", index = False, sep = "\t")

    @staticmethod
    def _get_authors_from_entry(
        in_article: dict[str, Any]
    ) -> list[str]:
        """
        Extrait les noms des auteurs d'un article Arxiv.

        Le champ « author » est un dictionnaire pour un auteur unique et une
        liste de dictionnaires pour plusieurs auteurs.

        :param in_article: dictionnaire contenant les infos de l'article.
        :return: liste des noms d'auteurs de l'article.
        """

        # On stocke les auteurs
        auteurs = in_article["author"]

        # Si on a plusieurs auteurs
        if isinstance(auteurs, list):

            # On renvoie la liste des auteurs
            return [e['name'] for e in auteurs]

        # Si on a un seul auteur
        elif isinstance(auteurs, dict):

            # On renvoie l'auteur sous forme de liste
            return [auteurs["name"]]

        # Si le format est inattendu
        else:
            print("Erreur de récupération du nom de l'auteur")
            return []

    @staticmethod
    def load_data_arxiv() -> pd.DataFrame:
        """
        Charge les données Arxiv locales, en les collectant si le CSV est absent.

        :return: DataFrame contenant les données des articles Arxiv.
        """

        # Si les données Arxiv ne sont pas dispo en local
        if not os.path.isfile("RawData/arxiv.csv"):

            # On requête l'API Arxiv pour les récupérer
            Arxiv.fetch_data()

        # On charge les données Arxiv
        df = pd.read_csv(
            "RawData/arxiv.csv",
            sep = "\t",
            converters = {"list_auteurs": ast.literal_eval}
        )

        return df
