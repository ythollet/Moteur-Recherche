from dataclasses import dataclass

from Documment.document import Document

@dataclass
class Author:

    name: str
    """ Nom de l'auteur """

    nb_docs: int
    """ Nombre de documents publiés """

    productions: list[Document]
    """ Dictionnaire des documents écrits par l’auteur. """


    def add_document(
        self,
        in_document: Document
    ) -> None:

        self.nb_docs += 1
        self.productions.append(in_document)

    def __str__(self) -> str:

        return f"name: {self.name}, nb_docs: {self.nb_docs}, production: {self.productions}"


    def show_stats(self):

        taille_totale_docs = (sum(len(p) for p in self.productions))

        taille_moyenne_docs = taille_totale_docs / self.nb_docs

        print(
            f'name: {self.name} | '
            f'nb_docs: {self.nb_docs} |  '
            f'taille_moyenne_docs: {taille_moyenne_docs}'
        )
