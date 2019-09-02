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

Titles = [tag.get_text("h2", {"class": "t4 media-heading"}) for tag in soup.find_all("h2", {"class": "t4 media-heading"})]

##Date de publication des offres
Date_publication = [tag.get_text("p", {"class": "date"}) for tag in soup.find_all("p", {"class": "date"})]

##Contrats des offres
Type_Contrat = [tag.get_text("p", {"class": "contrat visible-xs"}) for tag in soup.find_all("p", {"class": "contrat visible-xs"})]

##Ville des offres
Localisation = [tag.get_text("p", {"class": "subtext"}) for tag in soup.find_all("p", {"class": "subtext"})]

#Conversion en Dataframe 
result = pd.concat([pd.DataFrame(Titles), pd.DataFrame(Date_publication), pd.DataFrame(Type_Contrat), pd.DataFrame(Localisation)], axis=1)
result.columns=['Nom offre','Date de parution','Type de contrat','Localisation']
result['Localisation'].replace('p',' ',inplace=True, regex=True)
result['Date de parution'].replace('pO',' O',inplace=True, regex=True)


#Sauvegarde format CSV
result.to_csv('~/Documents/Projet_3_webscraping/CSV/Offres_python_2_sept_2019.csv', index=False, header=True)


#Création d'une nouvelle soupe pour récup de nouvelles infos
#ATTENTION!!! Cela ne marche que pour une offre définie, faudra voir pour automatiser ça

url=urlopen("https://candidat.pole-emploi.fr/offres/recherche/detail/0363134").read()
soup2 = BeautifulSoup(url, features="lxml")

##Récup du numéro de l'offre
info_offre=[tag.get_text("span", {"itemtype": "http://schema.org/PropertyValue"}) for tag in soup2.find_all("span", {"itemtype": "http://schema.org/PropertyValue"})]

#Ajout Dataframe (ne pas garder)
result2= pd.concat([result, pd.DataFrame(info_offre)], axis=1)
result2.columns=['Nom offre','Date de parution','Type de contrat','Localisation','Numéro']
result2['Numéro'].replace('span',' ',inplace=True, regex=True)


#Pour imprimer l'ensemble des urls d'une page
#Note:Donne tous les URL, faut voir pour limiter ça aux URL des offres 
for anchor in soup.find_all('a', href=True):
    print(anchor['href'])
