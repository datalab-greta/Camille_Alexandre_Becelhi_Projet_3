# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

#Définition de l'url et conversion BeautifulSoup

html= urlopen("https://candidat.pole-emploi.fr/offres/recherche?lieux=24R&motsCles=python&offresPartenaires=true&range=0-500&tri=0").read()
soup = BeautifulSoup(html, features="lxml")


#Nombre offres pour SQL Centre Val

#Extraction et conversion en dataframes

soup.find_all
##Titres des offres

Titles = [tag.get_text("h2", {"class": "t4 media-heading"}) for tag in soup.find_all("h2", {"class": "t4 media-heading"})]

##Date de publication des offres
Date_publication = [tag.get_text("p", {"class": "date"}) for tag in soup.find_all("p", {"class": "date"})]

##Contrats des offres
Type_Contrat = [tag.get_text("p", {"class": "contrat visible-xs"}) for tag in soup.find_all("p", {"class": "contrat visible-xs"})]

##Ville des offres
Localisation = [tag.get_text("p", {"class": "subtext"}) for tag in soup.find_all("p", {"class": "subtext"})]

##Code Rémi pour ajout référence et lien
for reference in soup.find_all('li', class_ ='result'):
    print(reference['data-id-offre'])  

for liens_desc in soup.find_all('h2', class_ ='t4 media-heading'):
    print(liens_desc.find('a', class_ ='btn-reset')['href'])  

Reference=[]
Lien=[]
for result in soup.find_all(class_ ='result'):
    Reference.append(result['data-id-offre'])
    Lien.append(result.find('a', class_ ='btn-reset')['href'])
#Création Data frame et csv

data={'Nom des offres': Titles,
      'Date de parution': Date_publication,
      'Type de de contrat': Type_Contrat,
      'Localisation': Localisation,
      'Référence': Reference,
      'Liens':Lien}
df = pd.DataFrame(data)

##Regex
df['Localisation'].replace('p',' ',inplace=True, regex=True)
df['Date de parution'].replace('pO',' O',inplace=True, regex=True)

##CSV
df.to_csv('~/Documents/Projet_3_webscraping/CSV/Offres_python_3_sept_2019.csv', index=False, header=True)


