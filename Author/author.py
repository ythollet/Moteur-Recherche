from dataclasses import dataclass

from Documment.document import Document


@dataclass
class Author:
    """ Représente un auteur et ses documents """

    name: str
    """ Nom de l'auteur """

    productions: dict[int, Document]

    """ Documents écrits par l'auteur, associés à leur identifiant dans le 
    corpus """


    def __str__(self) -> str:

        chain = (f"name: {self.name}, "
                 f"nb_docs: {self.nb_docs}, "
                 f"production: {self.productions}")

        return chain


    def nb_docs(
        self
    ) -> int:
        """
        Renvoie le nombre de documents présents dans les productions.
        """
        return len(self.productions)


    def add_document(
        self,
        in_document: Document,
        in_id_document: int,
    ):
        """
        Ajoute un document aux productions de l'auteur

        :param in_document: Document à associer à l'auteur.
        :param in_id_document: Identifiant du document dans le corpus.
        """

        self.productions |= {in_id_document: in_document}


    @staticmethod
    def show_stats(
        in_name_author: str,
        in_dict_authors: dict
    ):
        """ Recherche un auteur et affiche ses statistiques

        :param in_name_author: Nom de l'auteur (utilisé comme clé dans
          `in_dict_authors`).
        :param in_dict_authors: Dictionnaire associant les noms aux objets
          Author.
        :raises KeyError: Si l'auteur demandé est absent.
        """

        # On stocke l'objet Author
        author = in_dict_authors.get(in_name_author)

        # Si l'auteur ne figure pas dans le dictionnaire
        if not author:
            raise KeyError("L'auteur n'existe pas")

        # Nombre total de caractères dans l'ensemble des documents de l'auteur
        taille_totale_docs = (
            sum(len(doc.texte) for doc in author.productions.values())
        )

        # Calucle la taille moyenne des documents
        taille_moyenne_docs = taille_totale_docs / author.nb_docs

        # Affiche les statistiques
        print(
            f'name: {author.name} | '
            f'nb_docs: {author.nb_docs} |  '
            f'taille_moyenne_docs: {taille_moyenne_docs}'
        )


if __name__ == "__main__":
    from datetime import datetime

    # Exemple indépendant des API et des fichiers CSV, à adapter au modèle actuel.
    document = Document(
        titre = "Document de test",
        date = datetime(2026, 10, 3),
        url = "https://example.org/document",
        texte = "Bonjour",
        type = "Reddit",
    )

    authors = {
        "Alice": Author(
            name = "Alice", productions = {1: document}
            )
    }

    # Résultat visé après correction de l'exemple : 1 document et 7 caractères.
    Author.show_stats(in_name_author = "Alice", in_dict_authors = authors)
