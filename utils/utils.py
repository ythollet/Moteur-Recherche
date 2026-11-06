import re
import string


STOPWORDS = {
    'a', 'about', 'all', 'also', 'am', 'an', 'and', 'any', 'are', 'as',
    'at', 'be', 'been', 'but', 'by', 'can', 'do', 'for', 'from', 'has',
    'have', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'i’m', 'just',
    'm', 'me', 'more', 'my', 'now', 'of', 'on', 'or',
    'other', 'our', 'out', 's', 'should', 'so', 'some', 't', 'that', 'the',
    'there', 'they', 'this', 'to', 'up', 'was', 'we', 'what', 'which',
    'will', 'with', 'would', 'you', 'had', 'when', 'because', 'much', 'need'
}


def nettoyer_texte(
    in_str: str
) -> str:


    # Remplacement des sauts de ligne, tabulations, ponctuation par " "
    # et conversion en minuscule
    texte = (
        re.sub(rf'\n+|\t+|[{re.escape(string.punctuation)}]', ' ', in_str)
        .lower()
    )

    # Suppression des stopwords
    liste_mots = [
        mot
        for mot in texte.split()
        if (mot not in STOPWORDS) and (not mot.isdigit())
    ]

    texte = ' '.join(liste_mots)

    return texte
