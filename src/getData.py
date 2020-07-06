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

today = datetime.today()
logging.basicConfig(filename='log/' + today.strftime("%d:%m:%Y_%H:%M:%S") + '.log', level=logging.DEBUG)

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


url = "http://archive.luftdaten.info/"
#index.html downloaden
myfile = requests.get(url)

#ab diesem Datum werden Daten heruntergeladen
#bis in die Gegenwart
dateBeginn = time.strptime("01/05/2020", "%d/%m/%Y")
dateEnd = time.strptime("30/06/2020", "%d/%m/%Y")

dayList  = []
csvList  = []
sensorList = []
x = {}

#Datenbank konfigurieren
MONGO_HOST='localhost'
MONGO_PORT=8888
MONGO_USERNAME='mongoadmin'
MONGO_PASSWORD='Ze3cr1t!'

maxSevSelDelay=1

try:
    client = MongoClient(host='localhost', port=8888, username='mongoadmin', password='Ze3cr1t!',
                         serverSelectionTimeoutMS=maxSevSelDelay)

except errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    # tryagain later
    print(err)
#Datenbanke anlegen
db = client.airq_db
sensoren = db.airq_sensors
logging.info("Datenbank: airq_db")


#Ordnerstruktur auslesen in dayList beinhaltet
#hier eventeull noch Abfrage um Zeitraum zu begrenzen
soup = BeautifulSoup(myfile.content, 'html.parser')
for link in soup.find_all('a'):
    #if re.search("2020-\d\d-\d\d/",link.get('href')):
    if re.search("\d\d\d\d-\d\d-\d\d/",link.get('href')):
        test = re.findall("\d\d\d\d-\d\d-\d\d", link.get('href'))
        dateNow = time.strptime(test[0], "%Y-%m-%d")
        if dateNow >= dateBeginn and dateNow <= dateEnd:
            dayList.append(link.get('href'))
            #print(link.get('href'))
            logging.info(link.get('href'))


#ab hier for Schleife alle Tagesordner durchlaufen
for day in dayList:
    url2 = url + day

    #index.html für den jeweiligen Tagesordner downloaden
    myfile = requests.get(url2)

    #liste des Inhalts des Ordners auslesen in csvList gespeichert
    soup = BeautifulSoup(myfile.content, 'html.parser')
    for link in soup.find_all('a'):
        #print(link.get('href'))
        #if re.search("sds011_sensor_25443",link.get('href')):
        if re.search("sds011_sensor",link.get('href')) or re.search("sps30_sensor",link.get('href')):
            if not re.search("indoor",link.get('href')):
            	csvList.append(url2 + link.get('href'))
    #print(csvList)

#alle gültigen CSV Dateien (Links in csvList) downloaden und bearbeiten
for csvEintrag in csvList:
    download = requests.get(csvEintrag)
    myfile = download.content.decode('utf-8')
    csv_reader_object = csv.reader(myfile.splitlines(), delimiter=';')
    try:
        #sds011
        #sensor_id;sensor_type;location;lat;lon;timestamp;P1;durP1;ratioP1;P2;durP2;ratioP2
        if re.search("sds011_sensor", csvEintrag):
            csv_reader_object = csv.reader(myfile.splitlines(), delimiter=';')
            csv_reader_object.__next__()
            for row in csv_reader_object:
                for index in range(len(row)):
                    if row[index] == "" or row[index] == "unavailable" or row[index] == "%.1f":
                        row[index] = None
                #Falsches Zeitformat abfangen Zeile wird ignoriert
                if re.search("\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d", row[5]):
                    x = {
                        "sensor_id": int(row[0]),
                        "sensor_type": row[1],
                        "location": {
                            "type": "Point",
                            "coordinates": [(row[4] if (not row[4]) else float(row[4])), (row[3] if (not row[3]) else float(row[3]))]
                        },
                        "timestamp": datetime.fromisoformat(row[5]),
                        "PM1": None,
                        "PM4": None,
                        "PM2": (row[9] if (not row[9]) else float(row[9])),
                        "PM10": (row[6] if (not row[6]) else float(row[6])),
                        "N10": None,
                        "N4": None,
                        "N2": None,
                        "N1": None,
                        "N05": None,
                        "TS": None
                    }
                    sensorList.append(x)
        #sps30
        #sensor_id;sensor_type;location;lat;lon;timestamp;P1;P4;P2;P0;N10;N4;N25;N1;N05;TS
        if re.search("sps30_sensor", csvEintrag):
            csv_reader_object = csv.reader(myfile.splitlines(), delimiter=';')
            csv_reader_object.__next__()
            for row in csv_reader_object:
                for index in range(len(row)):
                    if row[index] == "" or row[index] == "unavailable" or row[index] == "%.1f":
                        row[index] = None
                #Falsches Zeitformat abfangen Zeile wird ignoriert
                if re.search("\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d", row[5]):
                    x = {
                        "sensor_id": int(row[0]),
                        "sensor_type": row[1],
                        "location": {
                            "type": "Point",
                            "coordinates": [(row[4] if (not row[4]) else float(row[4])), (row[3] if (not row[3]) else float(row[3]))]
                        },
                        "timestamp": datetime.fromisoformat(row[5]),
                        "PM1": (row[6] if (not row[6]) else float(row[6])),
                        "PM4": (row[7] if (not row[7]) else float(row[7])),
                        "PM2": (row[8] if (not row[8]) else float(row[8])),
                        "PM10": (row[9] if (not row[9]) else float(row[9])),
                        "N10": (row[10] if (not row[10]) else float(row[10])),
                        "N4": (row[11] if (not row[11]) else float(row[11])),
                        "N2": (row[12] if (not row[12]) else float(row[12])),
                        "N1": (row[13] if (not row[13]) else float(row[13])),
                        "N05": (row[14] if (not row[14]) else float(row[14])),
                        "TS": (row[15] if (not row[15]) else float(row[15]))
                    }
                    sensorList.append(x)

        sensoren.insert_many(documents=sensorList)
        logging.info("Datei in Datenbank gespeichert: " + csvEintrag)
        sensorList = []
    except:
        logging.warning("Datei nicht in Datenbank gespeichert: " + csvEintrag)
        logging.warning()
        sensorList = []