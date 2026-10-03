import ast
import os
import urllib
from typing import Optional

import xmltodict
import pandas as pd

from Documment.arxiv_document import ArxivDocument

class Arxiv:

    @staticmethod
    def get_authors_from_entry(
        in_entry: dict
    ) -> list[str]:

        auteurs = in_entry["author"]

        if isinstance(auteurs, list):
            return [e['name'] for e in auteurs]

        elif isinstance(auteurs, dict):
            return [auteurs["name"]]

        else:
            print("Erreur de récupération du nom de l'auteur")
            return []



    @staticmethod
    def main_fetch_data():

        query = (
            'all:%22personal%20finance%22%20OR%20'
            'all:%22retail%20investor%22%20OR%20'
            'all:%22individual%20investor%22%20OR%20'
            'all:%22household%20finance%22'
        )

        url = (
            f"https://export.arxiv.org/api/query?"
            f"search_query={query}"
            f"&start=0"
            f"&max_results=10"
        )


        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Moteur-Recherche/1.0"
            }
        )

        # Téléchargement du PDF en mémoire
        with urllib.request.urlopen(req) as response:
            xml_data = response.read().decode("utf-8")

            dict_arxiv = xmltodict.parse(xml_data)

        entries = dict_arxiv["feed"]["entry"]
        if isinstance(entries, dict):
            entries = [entries]

        print("Nombre d'articles Arxiv trouvés :", len(entries))

        documents_arxiv = []

        for entry in entries:

            texte = entry["summary"].replace("\n", " ").strip()

            document = ArxivDocument(
                list_auteurs= Arxiv.get_authors_from_entry(entry),
                texte = entry['summary'].replace("\n", " ").strip(),
                url = entry["id"],
                origine = 'Arxiv',
                date = entry["published"],
                titre = entry["title"]
            )

            documents_arxiv.append(document)

        df_arxiv = pd.DataFrame(documents_arxiv)

        df_arxiv.to_csv("RawData/arxiv.csv", index=False, sep="\t")

    @staticmethod
    def load_data_arxiv() -> pd.DataFrame:

        # Si les données Arxiv ne sont pas dispo en local
        if not os.path.isfile("RawData/arxiv.csv"):

            # On requête l'API Arxiv pour les récupérer
            Arxiv.main_fetch_data()

        df = pd.read_csv(
            "RawData/arxiv.csv",
            sep = "\t",
            converters = {"list_auteurs": ast.literal_eval}
        )

        return df
