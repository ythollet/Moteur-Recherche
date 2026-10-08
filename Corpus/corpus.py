import ast
import re
from pathlib import Path
from typing import Optional

import pandas as pd

from API.load_reddit_arxiv import load_raw_data
from Author.author import Author
from Documment.class_arxiv_document import ArxivDocument
from Documment.class_document import Document
from Documment.class_document_factory import DocumentFactory
from Documment.class_reddit_document import RedditDocument


class Corpus:
    """ Regroupe des documents et leurs auteurs """

    nom: str
    """ Nom du corpus """

    id_document: int
    """ Compteur de documents """

    documents: dict[int, Document]
    """ Documents du corpus, indexés par leur identifiant """

    authors: dict[str, Author]
    """ Auteurs des documents du corpus, indexés par leur nom """

    __all_docs: Optional[str] = None
    """ contient tous les documents concaténés en une seule chaine de caractère """

    __nb_docs: Optional[int] = None

    _instance = None
    """ Instance unique du corpus """

    @property
    def all_docs(self):

        if self.__all_docs is None:

            # Assemble les textes retenus en les séparant par un espace.
            self.__all_docs = ' '.join(
                document.texte
                for document
                in self.documents.values()
            )

        return self.__all_docs

    @property
    def nb_docs(self):

        if self.__nb_docs is None:
            self.__nb_docs = len(self.documents)
        else:
            return self.nb_docs


    def __init__(
        self,
        nom: str
    ):

        # Si l'objet a déjà été initialisé, on s'arrête.
        if getattr(self, "_initialise", False):
            return

        self.nom = nom

        self.id_document = 0
        self._initialise = True



    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    def show_docs_order_by_date(
        self,
        in_nb_docs: int
    ):
        """
        Affiche les identifiants et documents du plus récent au plus ancien.

        :param in_nb_docs: Nombre maximal de documents à afficher.
        """

        # Le tri porte sur la date de publication de chaque document.
        dict_sorted = dict(
            sorted(
                self.documents.items(), key = lambda x: x[1].date,
                reverse = True
                )
            )

        # Pour chaque document du dictionnaire
        for idx, (k, v) in enumerate(dict_sorted.items()):

            # Si on a atteint le nombre de docs demandés
            if idx == in_nb_docs:
                break
            print(k, v)


    def show_docs_order_by_title(
        self,
        in_nb_docs: int
    ):
        """
        Affiche les documents par titre croissant

        :param in_nb_docs: Nombre maximal de documents à afficher
        """

        # Les titres sont comparés tels quels, avec distinction de la casse.
        dict_sorted = dict(
            sorted(
                self.documents.items(), key = lambda x: x[1].titre,
                reverse = False
                )
            )

        # Pour chaque document du dictionnaire
        for idx, (k, v) in enumerate(dict_sorted.items()):

            # Si on a atteint le nombre de docs demandés
            if idx == in_nb_docs:
                break
            print(k, v)


    def save(self):
        """
        Sauvegarde les documents dans ``CorpusData/<nom>.csv``
        """

        # Une ligne contient les attributs propres au document et son
        # identifiant
        df = pd.DataFrame(
            [
                {'id': id} | document.__dict__
                for id, document
                in self.documents.items()
            ]
        )

        # Construit le chemin du dossier qui contiendra les données du Corpus
        path_folder = Path(__file__).resolve().parent.parent / "CorpusData"

        # On crée le dossier si nécessaire
        path_folder.mkdir(exist_ok = True)

        # On exporte le Corpus au format CSV
        df.to_csv(path_folder / f"{self.nom}.csv", index = False, sep = "\t")


    def load(
        self
    ) -> None:
        """
        Charge le Corpus et reconstruit les auteurs depuis la sauvegarde.

        :raises FileNotFoundError: Si le fichier de sauvegarde n'existe pas
        :raises Exception: Si un document indique une source non prise en charge
        """

        path_coprus = (
            Path(__file__)
            .resolve().parent.parent / "CorpusData" / f"{self.nom}.csv"
        )

        # Si le Corpus est sur le disque local
        if path_coprus.is_file():

            # literal_eval restaure les listes d'auteurs enregistrées sous forme de texte.
            df = pd.read_csv(
                path_coprus,
                sep = "\t",
                converters = {
                    "list_auteurs": lambda value: ast.literal_eval(value) if value
                    else []
                },
                dtype = {
                    "id": int,
                    "titre": str,
                    "url": str,
                    "texte": str,
                    "type": str,
                    "auteur": str,
                    "nb_comments": "Int64"
                },
                parse_dates = ["date"]
            )

            # Initialise les attributs
            self.id_document = len(df)
            self.authors = {}
            self._load_helper_document(in_df = df)
            self._load_helper_list_auteurs()


        # Si le corpus n'est pas présent en local
        else:

            # Chargement des données Reddit et Arxiv en DataFrame
            df = load_raw_data()

            # Initialise les attributs
            self.id_document = len(df)
            self.authors = {}
            self._load_helper_document(in_df = df)
            self._load_helper_list_auteurs()

            self.save()

    def _load_helper_document(
        self,
        in_df: pd.DataFrame
    ):
        """ Initialise l'attribut `document` à partir d'un DataFrame de
        documents

        :param in_df: Tableau contenant ``id``, ``titre``, ``date``, ``url``,
          ``texte``, ``type``, ainsi que:
            - ``auteur`` et ``nb_comments`` pour Reddit
            - ``list_auteurs`` pour Arxiv

        :raises Exception: Si une source diffère de 'Reddit' et 'Arxiv'.
        """

        self.documents = {}

        # La source détermine la classe et les attributs nécessaires à sa création.
        for row in in_df.itertuples():

            # On crée un document a partir de la ligne du DataFrame
            document = DocumentFactory.create_document(row)

            # On ajoute le document aux autres
            self.documents |= {row.id: document}


    def _load_helper_list_auteurs(
        self,
    ):
        """ Initialise l'attribut `list_auteurs` à partir d'un DataFrame de
        documents.
        """

        # Pour chaque document
        for id_doc, document in self.documents.items():

            # Reddit possède un auteur unique ; Arxiv fournit une liste d'auteurs.
            auteurs = (
                [document.auteur] if isinstance(document, RedditDocument)
                else document.list_auteurs
            )

            # Pour chaque auteur
            for auteur in auteurs:

                # Si l'auteur n'est oas encore dans le dictionnaire des auteurs
                if auteur not in self.authors:

                    # On l'ajoute
                    self.authors[auteur] = Author(
                        name = auteur,
                        productions = {id_doc: document}
                    )

                # Si l'auteur est déja présent dans le dictionnaire des auteurs
                else:

                    # On ajoute le document à ses productions
                    self.authors[auteur].productions[id_doc] = document


    def show_articles(
        self
    ):
        """
        Affiche le titre et la source de chaque document
        """

        # Pour chaque document
        for d in self.documents.values():

            # On affiche le titre et le type
            print(f'{d.titre} - {d.get_type()}\n')

    def search(
        self,
        in_word: str
    ) -> Optional[list[str]]:

        res = re.findall(rf'\w*\s*\b{in_word}\b\s*\w*', self.all_docs)

        return res


    def concorde(
        self,
        in_word: str,
        in_nb_char_context: int
    ) -> Optional[list[str]]:

        # TODO - res est vide
        res = re.findall(
            rf'(.{{0,{in_nb_char_context}}})\s*\b(in_word)\b\s*(.{{0,{in_nb_char_context}}})',
            self.all_docs
        )

        pass




if __name__ == "__main__":



    from datetime import datetime

    # Exemple indépendant des API, avec des documents Reddit et Arxiv.
    documents = {
        1: RedditDocument(
            titre = "titre1", date = datetime(2026, 10, 1),
            url = "https://example.org/python",
            texte = "Un document sur Python.",
            type = "Reddit", nb_comments = 5, auteur = "Alice",
        ),
        2: ArxivDocument(
            titre = "titre2", date = datetime(2026, 10, 3),
            url = "https://example.org/arxiv", texte = "Un document sur Arxiv.",
            type = "Arxiv", list_auteurs = ["Alice", "Bob"],
        ),
        3: RedditDocument(
            titre = "titre3", date = datetime(2026, 10, 2),
            url = "https://example.org/reddit",
            texte = "Un document sur Reddit.",
            type = "Reddit", nb_comments = 3, auteur = "Bob",
        ),
    }

    corpus = Corpus(
        nom = "test",
        authors = {},
        documents = documents,
    )

    # Résultat attendu : documents 2, 3 (les deux plus récents).
    print("Tri par date :")
    corpus.show_docs_order_by_date(2)

    # Résultat attendu : documents 1, 2 (les deux premiers titres triés).
    print("\nTri par titre :")
    corpus.show_docs_order_by_title(2)

    print("\nSauvegarde du corpus :")
    corpus.save()
    print(f"Fichier créé : CorpusData/{corpus.nom}.csv")

    # Un nouveau corpus vide permet de vérifier que load restaure les données.
    corpus_charge = Corpus(
        nom = "test",
        authors = {},
        documents = {},
    )
    corpus_charge.load()

    assert corpus_charge is corpus
    assert corpus_charge.documents is documents
    assert corpus_charge.documents == corpus.documents
    assert corpus_charge.id_document == len(documents)
    assert set(corpus_charge.authors) == {"Alice", "Bob"}
    assert corpus_charge.authors["Alice"].productions == {
        1: documents[1], 2: documents[2]
    }
    assert corpus_charge.authors["Bob"].productions == {
        2: documents[2], 3: documents[3]
    }
    assert all(
        auteur.nb_docs() == 2 for auteur in corpus_charge.authors.values()
        )
    print(
        "Chargement réussi : les 3 documents et les 2 auteurs ont été restaurés."
        )

    corpus_charge.show_articles()

