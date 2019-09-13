# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from sqlalchemy import create_engine, text

#Définition de l'accès à la BDD
user='team'
password='DataLab@2019'
machine='127.0.0.1'
base_donnees='Job_Bot_AlCaBe'
#base_donnees='BDD_Alexandre_job_bot' #Ceci est ma base de test
mySQLengine = create_engine("mysql://%s:%s@%s/%s?charset=utf8" % (user, password, machine, base_donnees))

#Définition du lieu, des mots clés et de l'url
lieu="24R"
motcle="data"

html= urlopen("https://candidat.pole-emploi.fr/offres/recherche?lieux="+lieu+"&motsCles="+motcle+"&offresPartenaires=true&range=0-150&tri=0").read()#Définition de l'url et conversion BeautifulSoup

soup = BeautifulSoup(html, features="lxml")

#Définition du nombre d'offres
titre = soup.find('h1', class_ ='title')
nb_offre = titre.next_element.replace('\n', '')
N=nb_offre.replace(' offres', '')
N=int(N)

#Intégration de la boucle, avec liste des URL différents (si applicables) dans une dataframe
Urlsliste=[]

i=0
while(i<N):
    imax = i+99 if (i+99<N) else N
    if imax>N:
        imax=N
    rg="%d-%d" % (i, imax)
    print(rg)
    URL="https://candidat.pole-emploi.fr/offres/recherche?lieux="+lieu+"&motsCles="+motcle+"&offresPartenaires=true&range="+rg+"&tri=0"
    print(URL)
    Urlsliste.append(URL)
    print(Urlsliste)
    i+=100

#Définition du contenu de la dataframe globale
Titles=[]
Type_Contrat=[]
Localisation=[]
Reference=[]
Lien=[]
Urlsliste=pd.DataFrame(Urlsliste)
Urlsliste.columns=["Urls"]
##Boucles pour récupération du contenu de la page d'accueil Pôle Emploi

for myurls in Urlsliste["Urls"]:
    soup = BeautifulSoup(urlopen(myurls).read(), features="lxml")
    for tag in soup.find_all('h2', class_ ='t4 media-heading'):
        Titles.append(tag.text)
    for tag in soup.find_all('p', class_ ='contrat visible-xs'):
        Type_Contrat.append(tag.text)
    for tag in soup.find_all('p', class_ ='subtext'):
        Localisation.append(tag.text)
    for result in soup.find_all(class_ ='result'):
        Reference.append(result['data-id-offre'])
        Lien.append(result.find('a', class_ ='btn-reset')['href'])


###Création d'une dataframe avec lien et adresse complète
Liendf=pd.DataFrame(Lien)
Liendf.columns=['Liens']
Liendf['Liens'].replace('/offres/', 'https://candidat.pole-emploi.fr/offres/', inplace=True, regex=True)

##Boucles pour récupération du contenu des offres Pole emploi
Date=[]
Exp=[]
#Competence=[]
for links in Liendf['Liens']:
    soup2 = BeautifulSoup(urlopen(links).read(), features="lxml")    
    for a in soup2.find_all(itemprop="datePosted"):
        Date.append(a.text)
    for exp in soup2.find_all(itemprop="experienceRequirements"):
        Exp.append(exp.text)

#Création Data frame pour csv
data={'Nom des offres': Titles,
      'Date de parution': Date,
      'Type de contrat': Type_Contrat,
      'Expérience': Exp,
      'Localisation': Localisation,
      'Références': Reference,
      'Liens':Lien}
df = pd.DataFrame(data)

##Regex
df['Localisation'].replace('-p', '- ', inplace=True, regex=True)
df['Date de parution'].replace('pO', ' O', inplace=True, regex=True)
#df['Date de parution'].replace('Offre avec peu de candidats', '- (Offre avec peu de candidats)', inplace=True, regex=True)
df['Liens'].replace('/offres/', 'https://candidat.pole-emploi.fr/offres/', inplace=True, regex=True)

titre = soup.find('h1', class_ ='title')
nb_offre = titre.next_element.replace('\n', '')
print(df)
print("Ma recherche comporte", nb_offre, "en région Centre !")

##CSV

df.to_sql('Archives_région_Centre', mySQLengine, if_exists='append', index=False,chunksize=1)

#Database
statement = text("""
INSERT INTO `Offres_région_Centre`
SELECT DISTINCT * FROM `Archives_région_Centre` WHERE `Archives_région_Centre`.`Références`NOT IN (SELECT `Références` FROM `Offres_région_Centre`)
ON DUPLICATE KEY UPDATE Offres_région_Centre.Expérience = Archives_région_Centre.Expérience
;
""")
mySQLengine.execute(statement)

select = mySQLengine.execute('SELECT * FROM Offres_région_Centre')
ResultSet = select.fetchall()
ResultSet = pd.DataFrame(ResultSet)
print("Voilà la base :", ResultSet)
ResultSet.to_csv('~/Archive/CSV/Base_content.csv',index=False, header=False)
