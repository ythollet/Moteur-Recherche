import ast

import pandas as pd
import os
from dotenv import load_dotenv

# Librairies projet
from API.reddit import Reddit
from API.arxiv import Arxiv
from Author.author import Author
from Documment.document import Document

load_dotenv() 

def _load_data_reddit() -> pd.DataFrame:

    # Si les données Reddit ne sont pas dispo en local
    if not os.path.isfile("data/reddit.csv"):

        # On requête l'API Reddit pour les récupérer
        Reddit.main_fetch_data()

    return pd.read_csv("data/reddit.csv", sep="\t")


def _load_data_arxiv() -> pd.DataFrame:

    # Si les données Arxiv ne sont pas dispo en local
    if not os.path.isfile("data/arxiv.csv"):

        # On requête l'API Arxiv pour les récupérer
        Arxiv.main_fetch_data()

    df = pd.read_csv(
        "data/arxiv.csv",
        sep = "\t",
        converters = {"auteurs": ast.literal_eval})

    return df


def _load_data() -> pd.DataFrame:

    df_reddit = _load_data_reddit()
    df_arxiv = _load_data_arxiv()

    df = pd.concat(
        [df_reddit, df_arxiv],
        ignore_index = True
    ).reset_index(names = 'id')

    return df
    


def main():

    # Chargement des données Reddit et Arxiv en DataFrame
    df = _load_data()



    # 3.1
    print(f'Nombre de documents : {len(df)}\n') 

    # id des lignes à supprimer du DataFrame
    list_id_row_to_drop = []

    # 3.2 
    for row in df.itertuples():

        if pd.isna(row.texte):
            list_id_row_to_drop.append(row.id)
            continue

        print(f'Document {row.id}')
        print(f'Mots : {len(row.texte.split())}')
        print(f'Phrases : {len(row.texte.split("."))}\n')

        # Si le document contient moins de 100 caractères
        if len(row.texte) < 100:

            # On l'ajoute à la liste des éléments à supprimer
            list_id_row_to_drop.append(row.id)

    # On supprimme toutes les lignes contenant moins de 100 caractères
    df.drop(index = list_id_row_to_drop, inplace = True)

    all_docs = ' '.join(df['texte'])

    dict_documents = {
        row.Index: Document(
            titre = row.titre,
            list_auteurs= row.list_auteurs,
            texte = row.texte,
            origine = row.origine,
            url = row.url,
            date = row.date
        )
        for row
        in df.itertuples()
    }


    dict_authors: dict[str, Author] = {}

    # Pour chaque document
    for document in dict_documents.values():

        # Pour chaque autheur de la liste
        for author in document.list_auteurs:

            # Si l'auteur est déja dans le dictionnaire
            if author in dict_authors.keys():

                dict_authors[author].add_document(
                    in_document = document
                )

            # Si l'auteur n'est pas dans le dictionnaire
            else:

                dict_authors[author] = Author(
                    name = author,
                    nb_docs = 1,
                    productions = [document],
                )




if __name__ == '__main__':
    main()
