import numpy as np
import pandas as pd
from scipy.sparse import lil_matrix
from tqdm.auto import tqdm

from Corpus.corpus import Corpus
from utils.utils import nettoyer_texte


class SearchEngine:

    corpus: Corpus
    """ Contient la base documentaire """

    matrix_tf_idf: lil_matrix
    """ Matrice TF-IDF du corpus """

    dict_mots: dict
    """ Dictionnaire contenant les infos sur chaque mot """

    dict_documents: dict
    """ Dictionnaire contenant les infos sur les documents du corpus """

    idf_mots: np.ndarray
    """ Contient les coefficients IDF de chaque mot"""


    def __init__(
        self,
        in_corpus: Corpus
    ):

        self.corpus = in_corpus

        # On charge le corpus
        self.corpus.load()

        # On affiche les stats et récupère
        # - le dictionnaire contenant pour chaque documents, sa liste de mots
        # - le DataFrame contenant le nombre d'occurences de chaque mots dans le corpus
        self.dict_documents, df_freq = self.corpus.stats()

        # On récupère le dictionnaire contenant les infos de chaque mots
        self.dict_mots = self.corpus.get_dict_mots_from_df_freq(
            in_df_freq = df_freq,
        )

        # On calucle la matrice TF-IDF
        self.build_matrix_tf_idf(
        )


    def build_matrix_tf(
        self
    ) -> lil_matrix:

        # On vérifie que le nombre de mot est renseigné
        if not self.corpus.nb_mots:
            raise ValueError('Nombre de mots inconnus')

        # On initailise la matrice TF
        matrix_tf = lil_matrix(
            (self.corpus.nb_docs, self.corpus.nb_mots),
            dtype = float
        )

        # Pour chaque document
        for num_doc, list_mots_document in tqdm(
            self.dict_documents.items(),
            desc = "Construction de la matrice TF",
            unit = "document"
        ):

            # Pour chaque mot du document
            for mot_document in list_mots_document:

                # On récupère l'id du mot
                num_mot = self.dict_mots[mot_document]['id_mot']

                # On compte le nombre de fois que le mot apparait dans le doc
                matrix_tf[num_doc, num_mot] += 1

        return matrix_tf


    def build_matrix_tf_idf(self):

        # On cosntruit la matrice TF
        matrix_tf = self.build_matrix_tf()

        # On initialise les coefficients IDF des mots
        self.idf_mots = np.zeros(len(self.dict_mots))

        # On calcule l'IDF de chaque mot
        for mot, stats_mot in self.dict_mots.items():

            # On récupère l'id du mot
            num_mot = stats_mot['id_mot']

            # Calcule le score IDF du mot
            idf_mot = np.log(self.corpus.nb_docs / stats_mot['nb_documents'])

            # On stocke l'IDF du mot dans une liste
            self.idf_mots[num_mot] = idf_mot

        # On construit la matrice TF-IDF en multipliant la matrice TF par les
        # coefficients IDF
        self.matrix_tf_idf = matrix_tf.multiply(self.idf_mots).tolil()




    def search(
        self,
        in_text: str,
        in_nb_docs_to_return = 5,
        in_source: str | None = None
    ) -> pd.DataFrame:

        """Recherche les meilleurs documents, avec un filtre facultatif.

        :param in_text: Mots-clés de la requête.
        :param in_nb_docs_to_return: Nombre maximal de documents à retourner.
        :param in_source: Source retenue, ou None pour toutes les sources.
        :return: Tableau des documents classés par similarité.
        :raises ValueError: Si la source est inconnue.
        """
        if in_source not in (None, "Reddit", "Arxiv"):
            raise ValueError("Source inconnue : choisissez Reddit ou Arxiv.")

        # On convertit le texte en vecteur
        text_vectorized = self.vectorize_texte(
            in_text = in_text,
        )

        # On calcule les distances (cosinus) entre le vecteur recherche et les
        # vecteurs documents
        list_cos = self.get_list_distances_recherche_documents(
            in_vector_recherche = text_vectorized
        )

        # On détermine les documents qui correspondent le mieux à la recherche
        df_best_docs = self.show_best_results(
            in_list_cos = list_cos,
            in_nb_docs_to_return = in_nb_docs_to_return,
            in_source = in_source
        )

        return df_best_docs


    def vectorize_texte(
        self,
        in_text: str
    ) -> lil_matrix:

        # On nettoie le texte
        text = nettoyer_texte(in_str = in_text)

        # On split le texte en mots
        list_mots = text.split()

        # On initailise le vecteur recherche TF
        vecteur_recherche_tf = np.zeros(len(self.dict_mots))

        # Pour chaque mot de la recherche
        for mot in list_mots:

            # On cherche l'id du mot
            num_mot = self.dict_mots.get(mot, {}).get('id_mot', None)

            # Si le mot est dans le corpus
            if num_mot is not None:

                # On met à jour le vecteur recherche
                vecteur_recherche_tf[num_mot] += 1

        # On applique les coefficients IDF au vecteur TF
        vecteur_recherche_tf_idf = lil_matrix(vecteur_recherche_tf * self.idf_mots)

        return vecteur_recherche_tf_idf


    def get_list_distances_recherche_documents(
        self,
        in_vector_recherche: lil_matrix
    ) -> list[float]:

        # On calcule la norme du vecteur recherche
        norme_vecteur_recherche = np.sqrt(
            in_vector_recherche.multiply(in_vector_recherche).sum()
        )

        # On initalise la liste des distances (cosinus)
        list_cos = []

        # Pour chaque document
        for num_row, vector_document in enumerate(tqdm(
            self.matrix_tf_idf,
            total = self.matrix_tf_idf.shape[0],
            desc = "Recherche dans le corpus",
            unit = "document"
        )):

            # On calcule le produit scalaire entre la recherche et le document
            prod_scal_recherche_doc = float(
                vector_document.multiply(in_vector_recherche).sum()
            )

            # On calucle la norme du vecteur document
            norme_vecteur_document = np.sqrt(
                vector_document.multiply(vector_document).sum()
            )

            # Calcule le cosinus entre le vecteur recherche et le vecteur document
            cos_recherche_document = (
                prod_scal_recherche_doc /
                (norme_vecteur_recherche * norme_vecteur_document)
                if norme_vecteur_recherche and norme_vecteur_document else 0
            )

            # Ajoute à la liste l'id du doc et son cos avec le vecteur recherche
            list_cos.append(cos_recherche_document)

        return list_cos


    def get_top_mots(
        self,
        in_nb_mots: int = 15,
        in_source: str | None = None
    ) -> pd.DataFrame:
        """Classe les mots par score TF-IDF moyen dans les documents retenus.

        :param in_nb_mots: Nombre maximal de mots à retourner.
        :param in_source: Source retenue, ou None pour tout le corpus.
        :return: Tableau des mots et de leur score TF-IDF moyen décroissant.
        :raises ValueError: Si le nombre de mots ou la source est invalide.
        """
        if in_nb_mots < 1:
            raise ValueError("Le nombre de mots doit être positif.")
        if in_source not in (None, "Reddit", "Arxiv"):
            raise ValueError("Source inconnue : choisissez Reddit ou Arxiv.")

        # Les identifiants des documents correspondent aux lignes de la matrice.
        lignes = [
            id_doc for id_doc, document in self.corpus.documents.items()
            if in_source is None or document.type == in_source
        ]
        if not lignes:
            return pd.DataFrame(columns = ["mot", "score_tf_idf"])

        # On conserve la matrice creuse : seul le vecteur moyen devient dense.
        scores = np.asarray(
            self.matrix_tf_idf.tocsr()[lignes].mean(axis = 0)
        ).ravel()

        df_mots = pd.DataFrame(
            [
                {"mot": mot, "score_tf_idf": scores[stats["id_mot"]]}
                for mot, stats in self.dict_mots.items()
            ],
            columns = ["mot", "score_tf_idf"],
        )

        # On écarte les scores nuls, les mots courts et ceux avec une apostrophe.
        df_mots = df_mots.loc[
            (df_mots["score_tf_idf"] > 0)
            & (df_mots["mot"].str.len() >= 3)
            & ~df_mots["mot"].str.contains("['’‘ʼ]", regex = True, na = False)
        ]
        return (
            df_mots.sort_values(
                ["score_tf_idf", "mot"], ascending = [False, True]
            )
            .head(in_nb_mots)
            .reset_index(drop = True)
        )


    def show_best_results(
        self,
        in_list_cos: list[float],
        in_nb_docs_to_return: int,
        in_source: str | None = None
    ) -> pd.DataFrame:

        # On stocke les documents dans un Dictionnaire
        dict_documents = self.corpus.documents.copy()

        # On convertit les documents en DataFrame
        df = pd.DataFrame.from_dict(
            dict_documents,
            orient = "index",
            columns = ['titre', 'url', 'type', 'auteur'],
        )

        # Ajout de la mesure de distance entre recherche et documents
        df['cos_recherche_document'] = in_list_cos

        # Filtre avant de limiter le nombre de résultats.
        if in_source is not None:
            df = df.loc[df['type'] == in_source]

        # On trie le DataFrame selon la mesure et conserve uniquement un top
        df = (
            df.sort_values(
                "cos_recherche_document", ascending = False, kind = "stable"
            )
            .head(in_nb_docs_to_return)
        )

        print(df.to_string())

        return df
