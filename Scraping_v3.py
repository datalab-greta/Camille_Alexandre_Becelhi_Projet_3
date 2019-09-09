# -*- coding: utf-8 -*-

#import requests, json, sys, re, os, configparser
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from sqlalchemy import create_engine, text

#Définition de l'accès à la BDD
user='team'
password='DataLab@2019'
machine='172.20.152.200'
#machine='127.0.0.1'
#machine='217.119.179.226'
base_donnees='Job_Bot_AlCaBe'
#TBL = "Offres"
#base = "/home/moi/Documents/Projet_3_webscraping/CSV/Scrap_donnees_Centre.csv"
mySQLengine = create_engine("mysql://%s:%s@%s/%s?charset=utf8" % (user, password, machine, base_donnees))


#Définition de l'url et conversion BeautifulSoup


html= urlopen("https://candidat.pole-emploi.fr/offres/recherche?lieux=24R&motsCles=data&offresPartenaires=true&range=0-500&tri=0").read()
soup = BeautifulSoup(html, features="lxml")

#Nombre offres pour Data et Centre Val de Loire

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

#datecomplete=[]
#Création Data frame et csv
data={'Nom des offres': Titles,
      'Date de parution': Date_publication,
      'Type de contrat': Type_Contrat,
      'Localisation': Localisation,
      'Références': Reference,
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

Date=[]
for links in df['Liens']:
    htmlall=links
    urlopen(htmlall).read()
    soup2 = BeautifulSoup(urlopen(htmlall).read(), features="lxml")
    #print(soup2)

    
    for a in soup2.find_all(itemprop="datePosted"):
#        print(a.contents)
        Date.append(str(a.text))


data={'Nom des offres': Titles,
      'Date de parution': Date_publication,
      'Date actu/publication': Date,
      'Type de contrat': Type_Contrat,
      'Localisation': Localisation,
      'Références': Reference,
      'Liens':Lien}
df = pd.DataFrame(data)
df['Localisation'].replace('-p', '- ', inplace=True, regex=True)
df['Date de parution'].replace('pO', ' O', inplace=True, regex=True)
df['Date de parution'].replace('Offre avec peu de candidats', '- (Offre avec peu de candidats)', inplace=True, regex=True)
df['Liens'].replace('/offres/', 'https://candidat.pole-emploi.fr/offres/', inplace=True, regex=True)

##CSV
#df.to_csv('~/Documents/Projet_3_webscraping/CSV/Offres_data_6_sept_2019.csv', index=False, header=True)
df.to_csv('/home/moi/Documents/Projet_3_webscraping/CSV/Scrap_data_Centre.csv',index=False, header=True)
#df.to_sql('Offres_région_Centre', mySQLengine, if_exists='append', index=False,chunksize=1)


