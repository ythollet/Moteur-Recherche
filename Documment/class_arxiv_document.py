from dataclasses import dataclass

from Documment.class_document import Document


@dataclass
class ArxivDocument(Document):
    """ Étend un Document avec les noms des auteurs d'une publication Arxiv."""

    list_auteurs: list[str]
    """ Liste des noms des auteurs de la publication """

    def __str__(self):
        """
        Renvoie tous les attributs
        """
        res = ''
        for k, v in self.__dict__.items():
            res += f'{k}: {v}\n'

        return res


    def get_list_auteurs(self):
        """ Renvoie la liste des auteurs de la publication """

        return self.list_auteurs


    def set_list_auteurs(
        self,
        list_auteurs: list[str]
    ):
        """ Remplace la liste des auteurs par la liste fournie

        :param list_auteurs: Liste des noms des auteurs à conserver
        """
        self.list_auteurs = list_auteurs

    def get_type(self):
        """ Renvoie la source enregistrée dans l'attribut ``type``.

        :returns: Source du document.
        """
        return self.type
