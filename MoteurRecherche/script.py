import praw
import urllib.request
# import xmltodict
# import numpy as np
# import json
# import pickle
# import datetime
# import pandas as pd
import arxiv
import os

# taille_docs=10

# # Récupération de textes depuis Reddit
# reddit = praw.Reddit(
#     client_id=os.getenv('CLIENT_ID'), 
#     client_secret=os.getenv('CLIENT'), 
#     user_agent=os.getenv('Walid_M1')
# )


# subr = reddit.subreddit('vosfinances')

# posts = list(subr.hot(limit=taille_docs))

# textes_Reddit = []
# for post in posts:

#     # Titre toujours présent
#     texte = post.title.replace("\n", " ") + ". "

#     if post.selftext:
#         texte += post.selftext.replace("\n", " ")
#     elif post.url:
#         texte += post.url

#     textes_Reddit.append(texte)

# print("\n\n Nombre de posts Reddit collectés :", len(textes_Reddit))

# for texte in textes_Reddit[:5]:
#     print("\n\n\n---")
#     print(texte)


# # Initialisation du client
# client = arxiv.Client(
#     page_size=10,
#     delay_seconds=3.0,  # Respecte la politique de rate limit d'arXiv
#     num_retries=3
# )

# # Recherche par mots-clés ou catégorie (ex: Computer Vision / cs.CV)
# search = arxiv.Search(
#     query="cat:cs.CV AND deep learning",
#     max_results=5,
#     sort_by=arxiv.SortCriterion.SubmittedDate
# )

# for result in client.results(search):
#     print(f"Titre : {result.title}")
#     print(f"Auteurs : {', '.join(a.name for a in result.authors)}")
#     print(f"Date : {result.published.date()}")
#     print(f"PDF : {result.pdf_url}")
#     print(f"Résumé : {result.summary[:150]}...")
#     print("-" * 40)