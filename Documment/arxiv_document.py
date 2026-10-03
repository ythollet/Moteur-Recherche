from dataclasses import dataclass

from Documment.document import Document


@dataclass
class ArxivDocument(Document):

    list_auteurs: list[str]
    """ Nom de l’auteur (ou des autheurs) """

    def __str__(self):
        res = ''
        for k, v in self.__dict__.items():
            res += f'{k}: {v}\n'
        return res

    def get_list_auteurs(self):
        return self.list_auteurs

    def set_list_auteurs(self, list_auteurs):
        self.list_auteurs = list_auteurs
