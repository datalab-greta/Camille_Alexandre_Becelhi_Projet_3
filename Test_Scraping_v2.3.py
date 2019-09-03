# -*- coding: utf-8 -*-

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
Reference=[]
Lien=[]
for result in soup.find_all(class_ ='result'):
    Reference.append(result['data-id-offre'])
    Lien.append(result.find('a', class_ ='btn-reset')['href'])

#Création Data frame et csv
data={'Nom des offres': Titles,
      'Date de parution': Date_publication,
      'Type de contrat': Type_Contrat,
      'Localisation': Localisation,
      'Référence': Reference,
      'Liens':Lien}
df = pd.DataFrame(data)

##Regex
df['Localisation'].replace('-p', '- ', inplace=True, regex=True)
df['Date de parution'].replace('pO', ' O', inplace=True, regex=True)
df['Date de parution'].replace('Offre avec peu de candidats', '- (Offre avec peu de candidats)', inplace=True, regex=True)
df['Liens'].replace('/offres/', 'https://candidat.pole-emploi.fr/offres/', inplace=True, regex=True)

titre = soup.find('h1', class_ ='title')
nb_offre = titre.next_element.replace('\n', '')
print("Ma recherche comporte", nb_offre, "!")
print(df)

##CSV
df.to_csv('~/Documents/Projet_3_webscraping/CSV/Offres_python_3_sept_2019.csv', index=False, header=True)


