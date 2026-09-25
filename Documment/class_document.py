from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:
    
    titre: str
    """ Titre du document """

    auteur: str 
    """ Nom de l’auteur """

    date: datetime 
    """ Date de publication """

    url: str
    """ URL source """

    texte: str
    """ Contenu textuel du document """