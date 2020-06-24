import csv
import io
import json
import logging
import re
import time
from datetime import datetime

import requests
from pymongo import MongoClient, errors

from bs4 import BeautifulSoup

logging.basicConfig(filename='logging.log', level=logging.DEBUG)

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


url = "http://archive.luftdaten.info/"
#index.html downloaden
myfile = requests.get(url)

#ab diesem Datum werden Daten heruntergeladen
#bis in die Gegenwart
date = time.strptime("22/06/2020", "%d/%m/%Y")

dayList  = []
csvList  = []
sensorList = []
x = {}

#Datenbank konfigurieren
MONGO_HOST='localhost'
MONGO_PORT=8888
MONGO_USERNAME='mongoadmin'
MONGO_PASSWORD='secret'

maxSevSelDelay=1

try:
    client = MongoClient(host='localhost', port=8888, username='mongoadmin', password='secret',
                         serverSelectionTimeoutMS=maxSevSelDelay)

except errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    # tryagain later
    print(err)
#Datenbanke anlegen
db = client.patricksDB3
sensoren = db.sensoren

#Ordnerstruktur auslesen in dayList beinhaltet
#hier eventeull noch Abfrage um Zeitraum zu begrenzen
soup = BeautifulSoup(myfile.content, 'html.parser')
for link in soup.find_all('a'):
    #if re.search("2020-\d\d-\d\d/",link.get('href')):
    if re.search("\d\d\d\d-\d\d-\d\d/",link.get('href')):
        test = re.findall("\d\d\d\d-\d\d-\d\d", link.get('href'))
        date2 = time.strptime(test[0], "%Y-%m-%d")
        if date2 >= date:
            dayList.append(link.get('href'))
            print(link.get('href'))


#ab hier for Schleife alle Tagesordner durchlaufen
for day in dayList:
    url2 = url + day

    #index.html für den jeweiligen Tagesordner downloaden
    myfile = requests.get(url2)

    #liste des Inhalts des Ordners auslesen in csvList gespeichert
    soup = BeautifulSoup(myfile.content, 'html.parser')
    for link in soup.find_all('a'):
        #print(link.get('href'))
        if re.search("sds011_sensor",link.get('href')) or re.search("sps30_sensor",link.get('href')):
            csvList.append(url2 + link.get('href'))
    #print(csvList)

#alle gültigen CSV Dateien (Links in csvList) downloaden und bearbeiten
for csvEintrag in csvList:
    download = requests.get(csvEintrag)
    myfile = download.content.decode('utf-8')
    csv_reader_object = csv.reader(myfile.splitlines(), delimiter=';')
    #sds011
    #sensor_id;sensor_type;location;lat;lon;timestamp;P1;durP1;ratioP1;P2;durP2;ratioP2
    if re.search("sds011_sensor", csvEintrag):
        csv_reader_object = csv.reader(myfile.splitlines(), delimiter=';')
        csv_reader_object.__next__()
        for row in csv_reader_object:
            #Falsches Zeitformat abfangen Zeile wird ignoriert
            if re.search("\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d", row[5]):
                x = {
                    "sensor_id": row[0],
                    "sensor_type": row[1],
                    "location": {
                        "type": "point",
                        "coordinates": [row[4], row[3]]
                    },
                    "timestamp": datetime.fromisoformat(row[5]),
                    "PM1": "",
                    "PM4": "",
                    "PM2": row[9],
                    "PM10": row[6],
                    "N10": "",
                    "N4": "",
                    "N2": "",
                    "N1": "",
                    "N05": "",
                    "TS": ""
                }
                sensorList.append(x)
    #sps30
    #sensor_id;sensor_type;location;lat;lon;timestamp;P1;P4;P2;P0;N10;N4;N25;N1;N05;TS
    if re.search("sps30_sensor", csvEintrag):
        csv_reader_object = csv.reader(myfile.splitlines(), delimiter=';')
        csv_reader_object.__next__()
        for row in csv_reader_object:
            #Falsches Zeitformat abfangen Zeile wird ignoriert
            if re.search("\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d", row[5]):
                x = {
                    "sensor_id": row[0],
                    "sensor_type": row[1],
                    "location": {
                        "type": "point",
                        "coordinates": [row[4], row[3]]
                    },
                    "timestamp": datetime.fromisoformat(row[5]),
                    "PM1": row[6],
                    "PM4": row[7],
                    "PM2": row[8],
                    "PM10": row[9],
                    "N10": row[10],
                    "N4": row[11],
                    "N2": row[12],
                    "N1": row[13],
                    "N05": row[14],
                    "TS": row[15]
                }
                sensorList.append(x)

    sensoren.insert_many(documents=sensorList)
    logging.info("Datei in Datenbank gespeichert: " + csvEintrag)
    sensorList = []