# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

html= urlopen("https://candidat.pole-emploi.fr/offres/recherche?lieux=24R&motsCles=SQL&offresPartenaires=true&range=0-9&rayon=10&tri=0").read()
req=requests.get(html, "lxml")
soup = BeautifulSoup(html, features="html.parser")

print(soup.find_all('h2'))
soup.find_all('h2')


for sub_heading in soup.find_all("h2", {"class": "title"}):
    print(sub_heading.text)

Titles1 = [tag.get_text("h2", {"class": "t4 media-heading"}) for tag in soup.find_all("h2", {"class": "t4 media-heading"})]
