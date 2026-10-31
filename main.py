import os
from ensurepip import __main__

import numpy as np
import pandas as pd
from dotenv import load_dotenv

# Librairies projet
from API.reddit import Reddit
from API.arxiv import Arxiv
from Corpus.corpus import Corpus
from utils.utils import nettoyer_texte

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

    # On calucle la matrice TF-IDF
    matrix_tf_idf, idf_mots = corpus.build_matrix_tf_idf(
        in_dict_mots = dict_mots,
        in_dict_documents = dict_documents
    )

    # texte = input("Saisissez votre recherche : ")
    texte = "i like money"

    text_vectorized = corpus.vectorize_texte(
        in_text = texte,
        in_dict_mots = dict_mots,
        in_idf_mots = idf_mots,
    )

    list_cos = corpus.get_list_distances_recherche_documents(
        in_vector_recherche = text_vectorized,
        in_matrix_tf_idf = matrix_tf_idf
    )

    corpus.show_best_results(
        in_list_cos = list_cos
    )








if __name__ == '__main__':
    main()
