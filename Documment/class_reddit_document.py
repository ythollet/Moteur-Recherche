from dataclasses import dataclass

from Documment.class_document import Document


@dataclass
class RedditDocument(Document):
    """Étend un document avec les informations propres à une publication Reddit."""

    nb_comments: int
    """Nombre de commentaires de la publication."""

    auteur: str
    """Nom de l'auteur de la publication."""


    def __str__(self):
        """
        Renvoie tous les attributs, chacun sur une ligne terminée par un saut de
        ligne.
        """

        res = ''
        # Inclut les attributs hérités, l'auteur et le nombre de commentaires.
        for k, v in self.__dict__.items():
            res += f'{k}: {v}\n'
        return res


    def get_nb_comments(self):
        """
        Renvoie le nombre de commentaires enregistré.
        """
        return self.nb_comments


    def set_nb_comments(self, nb_comments):
        """
        Remplace le nombre de commentaires

        :param nb_comments: Nouveau nombre de commentaires de la publication
        """

        self.nb_comments = nb_comments


    def get_auteur(
        self
    ) -> str:
        """
        Renvoie le nom de l'auteur de la publication

        :returns: Nom de l'auteur
        """
        return self.auteur


    def set_auteur(self, auteur):
        """
        Remplace le nom de l'auteur.

        :param auteur: Nouveau nom à associer à la publication.
        """
        self.auteur = auteur


    def get_type(self):
        """
        Renvoie la source enregistrée dans l'attribut ``type``

        :return: Source du document.
        """
        return self.type
