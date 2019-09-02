# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

#Définition de l'url et conversion BeautifulSoup

html= urlopen("https://candidat.pole-emploi.fr/offres/recherche?lieux=24R&motsCles=python&offresPartenaires=true&range=0-500&rayon=500&tri=0").read()
soup = BeautifulSoup(html, features="lxml")


#Nombre offres pour SQL Centre Val

#Extraction et conversion en dataframes

soup.find_all
##Titres des offres

Titles1 = [tag.get_text("h2", {"class": "t4 media-heading"}) for tag in soup.find_all("h2", {"class": "t4 media-heading"})]

##Date de publication des offres
Date_publication = [tag.get_text("p", {"class": "date"}) for tag in soup.find_all("p", {"class": "date"})]

##Contrats des offres
Type_Contrat = [tag.get_text("p", {"class": "contrat visible-xs"}) for tag in soup.find_all("p", {"class": "contrat visible-xs"})]

##Ville des offres
Localisation = [tag.get_text("p", {"class": "subtext"}) for tag in soup.find_all("p", {"class": "subtext"})]

#Conversion en Dataframe 
result = pd.concat([pd.DataFrame(Titles1), pd.DataFrame(Date_publication), pd.DataFrame(Type_Contrat), pd.DataFrame(Localisation)], axis=1)
result.columns=['Nom offre','Date de parution','Type de contrat','Localisation']

#Sauvegarde format CSV

result.to_csv('Offres_python_2_sept_2019.csv', index=False, header=True)
