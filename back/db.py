###############################################################################
#Fichier base de données
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#10/04/2018
#Les fonctions d'insertion dans la BDD sont encascadées selon les dépendances
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import pyodbc
import data_mining as dm
import pandas as pd
import getpass
import csv
from collections import namedtuple
###############################################################################


###############################################################################
#FONCTION
###############################################################################
#Initialisation de la base de données
#Retourne le contexte
def init_db():
    server = '10.2.38.20,1433'
    database = 'Planner'
    username = 'SOLUTEC\rcavalieri'
    password = getpass.getpass(prompt="Planner's password : ")
    connexion = pyodbc.connect('Trusted_connection=yes;DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return connexion


#Permet de réaliser une commande sql
def command(db_cmd, arg):
    context=init_db()
    handler=context.cursor()
    res=handler.execute(db_cmd, arg)
    context.commit()
    return res


#Insertion des parametres dans la BDD : time |�distance |�heuristic |�position_id(FK)
def insert_param(time, distance, heuristic):
    res=command('INSERT INTO param([time],[distance],[heuristic]) VALUES(?,?,?)',(time, distance, heuristic))
    return res


#R�cup�ration de toutes les places et instanciation de objets
def placesToCsv():
    temp = dm.getPlacesGps('../data/cities.csv', '../data/data_place.json')
    Submission=namedtuple('Submission', ['id_', 'name', 'photo', 'types', 'geometry', 'visitsCount', 'city_id'])
    with open('../data/all_places.csv', 'w', encoding='utf8') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(Submission._fields)
        for member in temp:
            wr.writerow([member.getId(), member.getName(), member.getPhoto(), str(member.getTypes()), str(member.getGeometry()), str(member.getVisitsCount()), str(member.getCity_id())])
###############################################################################
