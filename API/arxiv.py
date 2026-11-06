import ast
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any
import xmltodict
import pandas as pd

from Documment.class_arxiv_document import ArxivDocument


class Arxiv:
    """Regroupe la collecte et le chargement des articles Arxiv."""

    @staticmethod
    def fetch_data():
        """
        Récupère les articles, initialise des objets ArxivDocument, convertit en
        DataFrame et les sauvegarde en CSV sur le disque

        :raises ValueError: Si aucun article n'est trouvé.
        """

        # Expressions liées aux finances des particuliers.
        expressions = (
            "personal finance", "retail investor", "individual investor",
            "household finance", "financial literacy", "retirement saving",
            "retirement planning", "consumer debt", "household debt",
            "mortgage borrowing", "portfolio choice",
        )

        # Relie les expressions par un OU logique.
        # Le préfixe all recherche dans l'ensemble des champs de l'article
        # (titre, résumé, auteur).
        query = ' OR '.join(
            f'all:"{expression}"'
                for expression in expressions
        )

        # On construit l'URL
        # urlencode encode les espaces et les guillemets pour construire l'URL.
        parametres = urllib.parse.urlencode({
            "search_query": query,
            "start": 0,
            "max_results": 1000,
            "sortBy": "relevance",
            "sortOrder": "descending",
        })
        url = f"https://export.arxiv.org/api/query?{parametres}"

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
        articles = dict_arxiv["feed"].get("entry", [])
        if isinstance(articles, dict):
            articles = [articles]

        print("Nombre d'articles Arxiv trouvés :", len(articles))

        if not articles:
            raise ValueError("Aucun article Arxiv trouvé ; le CSV est conservé.")

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
        Path("RawData").mkdir(exist_ok = True)
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
