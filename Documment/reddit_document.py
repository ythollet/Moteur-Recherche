from dataclasses import dataclass

from Documment.document import Document


@dataclass
class RedditDocument(Document):

    nb_comments: int
    """ Nombre de commentaires du post """

    auteur: str
    """ Nom de l’auteur """


    def __str__(self):

        res = ''
        for k,v in self.__dict__.items():
            res +=  f'{k}: {v}\n'
        return res

    def get_nb_comments(self):
        return self.nb_comments

    def set_nb_comments(self, nb_comments):
        self.nb_comments = nb_comments

    def get_auteur(self):
        return self.auteur

    def set_auteur(self, auteur):
        self.auteur = auteur