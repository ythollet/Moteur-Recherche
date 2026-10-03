from dataclasses import dataclass

from Documment.document import Document

@dataclass
class Author:

    name: str
    """ Nom de l'auteur """

    productions: dict[int, Document]
    """ Documents écrits par l’auteur. """



    def nb_docs(
        self
    ):
        """ Renvoie le nombre de documents publiés """
        return len(self.productions)

    def add_document(
        self,
        in_document: Document,
        in_id_document: int,
    ) -> None:

        self.productions |= {in_id_document : in_document}

    def __str__(self) -> str:

        return f"name: {self.name}, nb_docs: {self.nb_docs}, production: {self.productions}"

    @staticmethod
    def show_stats(
        in_name_author: str,
        in_dict_authors: dict
    ):

        author = in_dict_authors.get(in_name_author)

        if not author:
            raise KeyError("L'auteur n'existe pas")
            return

        taille_totale_docs = (sum(len(doc.texte) for doc in author.productions.values()))

        taille_moyenne_docs = taille_totale_docs / author.nb_docs

        print(
            f'name: {author.name} | '
            f'nb_docs: {author.nb_docs} |  '
            f'taille_moyenne_docs: {taille_moyenne_docs}'
        )


if __name__ == "__main__":
    from datetime import datetime

    # Exemple indépendant des API et des fichiers CSV.
    document = Document(
        titre="Document de test",
        list_auteurs=["Alice"],
        date=datetime(2026, 10, 3),
        url="https://example.org/document",
        texte="Bonjour",
        origine="Reddit",
    )

    authors = {
        "Alice": Author(name="Alice", nb_docs=1, productions={1: document})
    }

    # Résultat attendu : 1 document et une taille moyenne de 7 caractères.
    Author.show_stats(in_name_author="Alice", in_dict_authors=authors)

