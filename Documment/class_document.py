from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Document:

    titre: Optional[str]
    """ Titre du document """

    auteurs: Optional[list[str]]
    """ Nom de l’auteur (ou des autheurs) """

    date: Optional[datetime]
    """ Date de publication """

    url: Optional[datetime]
    """ URL source """

    texte: Optional[str]
    """ Contenu textuel du document """

    origine : Optional[str]
    """ Source du document """

    def infos(self):

        for k,v in vars(self).items():
            print(f'{k} : {v}')


    def __str__(self):

        return f'Titre : {self.titre}'



if __name__ == '__main__':

    document = Document(
        auteur = 'Jean michel',
        date = datetime.now(),
        texte = 'blablabla',
        titre = 'titre1',
        url = 'http://ckhnvubvfzubaefifabù',
        origine = 'Reddit'
    )
    document.infos()

    print()
    print(document)