from Documment.class_document import Document


class Author:

    name: str
    """ Nom de l'auteur """

    nb_docs: str
    """ Nombre de documents publiés """

    production: dict
    """ Dictionnaire des documents écrits par l’auteur. """

    def add_documents(
        self,
        in_documents: Document
    ):

        self.nb_docs += 1
        self.production |= in_documents

    def __str__(self) -> str:

        return f"name: {self.name}, nb_docs: {self.nb_docs}, production: {self.production}"