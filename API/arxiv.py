import urllib
from typing import Optional

import xmltodict
import pandas as pd

from Documment.class_document import Document

class Arxiv:

    @staticmethod
    def get_authors_from_entry(
        in_entry: dict
    ) -> Optional[list[str]]:

        auteurs = in_entry.get("author")

        if isinstance(auteurs, list):
            return [e['name'] for e in auteurs]

        elif isinstance(in_entry, dict):
            return [auteurs.get("name")]

        else:
            raise ValueError("Erreur de récupération du nom de l'auteur")



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

        entries = dict_arxiv["feed"].get("entry", [])
        if isinstance(entries, dict):
            entries = [entries]

        print("Nombre d'articles Arxiv trouvés :", len(entries))

        documents_arxiv = []
        for entry in entries:
            texte = entry["summary"].replace("\n", " ").strip()

            document = Document(
                auteurs = Arxiv.get_authors_from_entry(entry),
                texte = entry.get('summary').replace("\n", " ").strip(),
                url = entry.get("id"),
                origine = 'Arxiv',
                date = entry.get("published"),
                titre = entry.get("title")
            )
            documents_arxiv.append(document)

        df_arxiv = pd.DataFrame(documents_arxiv)

        df_arxiv.to_csv("data/arxiv.csv", index=False, sep="\t")