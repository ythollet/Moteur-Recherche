import os
from ensurepip import __main__

import pandas as pd
from dotenv import load_dotenv

# Librairies projet
from API.reddit import Reddit
from API.arxiv import Arxiv
from Corpus.corpus import Corpus

# Charge les variables du fichier .env nécessaires aux accès aux API.
load_dotenv()





def main():

    corpus = Corpus(
        nom = "corpus_finance"
    )

    corpus.load()

    # On affiche les stats et récupère
    # - le dictionnaire contenant pour chaque documents, sa liste de mots
    # - le DataFrame contenant le nombre d'occurences de chaque mots dans le corpus
    dict_documents, df_freq = corpus.stats()

    # On récupère le dictionnaire contenant les infos de chaque mots
    dict_mots = corpus.get_dict_mots_from_df_freq(
        in_df_freq = df_freq,
    )

    # On calcule la matrice TF
    matrix_tf = corpus.build_matrix_tf(
        in_dict_mots = dict_mots,
        in_dict_documents = dict_documents
    )

    matrix_tf







if __name__ == '__main__':
    main()
