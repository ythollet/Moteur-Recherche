import re
import string


def nettoyer_texte(
    in_str: str
) -> str:

    texte = re.sub(
        rf'\d+|\n+|\t+|[{re.escape(string.punctuation)}]', ' ', in_str
        ).lower()

    return texte