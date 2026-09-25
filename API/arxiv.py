import urllib
import xmltodict
import pandas as pd

def func_fetch_data_arxiv():

    query = (
        'all:%22personal%20finance%22%20OR%20'
        'all:%22retail%20investor%22%20OR%20'
        'all:%22individual%20investor%22%20OR%20'
        'all:%22household%20finance%22'
    )

    url = (
        f"https://export.arxiv.org/api/query?"
        f"search_query={query}"
        f"&start=0"
        f"&max_results=10"
    )


    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Moteur-Recherche/1.0",
            "Accept": "application/atom+xml"
        }
    )

    # Téléchargement du PDF en mémoire
    with urllib.request.urlopen(req) as response:
        xml_data = response.read().decode("utf-8")

        dict_arxiv = xmltodict.parse(xml_data)

    entries = dict_arxiv["feed"].get("entry", [])
    if isinstance(entries, dict):
        entries = [entries]

    print("Nombre d'articles Arxiv trouvés :", len(entries))

    textes_Arxiv = []
    for entry in entries:
        texte = entry["summary"].replace("\n", " ").strip()
        textes_Arxiv.append(texte)

    for texte in textes_Arxiv[:5]:
        print("\n\n\n---")
        print(texte)

    df_arxiv = pd.DataFrame(textes_Arxiv, columns=["text"])

    df_arxiv["origine"] = "Arxiv"

    df_arxiv.to_csv("data/df_arxiv.csv", index_label="id", sep="\t")