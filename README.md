Roman, Patrick Nam Coden in der Luft

INSTALLATION ANLEITUNG

Voraussetzung:
 - Eine funktionierende Git Version auf deinem Computer
 - Funktionierende Python Umgebung (3.8x) und Basic Skills in der Nutzung und Installation von Python
 - VPN Verbindung ins Hochschulnetz (Anleitung siehe hier: https://wiki.reutlingen-university.de/pages/viewpage.action?pageId=21201453)

Steps to do:
 - Download des Projektes von Github
 - Erstellung einer virtual Python Env auf Basis einer Python 3.8 Instanz
 - Installation der relevanten Pakete in die "virtuelle Umgebung" über die requirements.txt
 

 Wie downloade ich das Projekt von Github?
 
  - Frage das Team (Roman, Nam, Patrick) nach dem Einladungslink, um für das Projekt berechtigt zu werden
  - Klone dir das Projekt über den Befehl
            git clone https://github.com/HazeHawk/Luft.git <pfad/zum/ordner>
 
Wie setze ich eine Virtualenv auf?
Die folgenden Befehle sind in der Console deiner Wahl einzugeben (bash, cmd, PowerShell etc.)

    - installiere in deiner Python Umgebung deiner Wahl virtualenv
            pip install virtualenv
    - führe im gewünschten Python interpreter den folgenden Befehl aus:
      (Empfehlung ist es die virtuelle Umgebung in einem neuen Ordner im Git Repository zu erstellen)
            py -3.8 -m virtualenv <pfad/zum/env_ordner>
    - Aktiviere deine virtuelle Umgebung, um in der virtualenv die relevanten Pakete zu installieren
            source <pfad/zum/env_ordner/Scripts/activate>
    - Installiere die requirements.txt pakete:
      (Die requirements.txt befindet sich im repo)
            pip install -r </path/to/requirements.txt>

Wie starte ich die Anwendung ?
 - Stelle sicher das du dich im VPN der Hochschule Reutlingen befindest. Als test könnt ihr versuchen den folgenden Link aufzurufen:
            http://hucserv193:8081/
   Es sollte eine HTML Seite kommen, wo drin steht, dass ihr versuch auf die DB über n Browser zuzugreifen (was logischer weise nicht klappt ;))
 - Stelle sicher, dass ihr den Python Intepreter aus der virtuellen Umgebungen aktiviert habt
             source <pfad/zum/env_ordner/Scripts/activate>
 - Führe die main.py im Repository aus
             python main.py


Weitere Hinweise:
Der source Befehl muss für jede Consolen Instanz extra ausgeführt werden. 
Startet ihr das Projekt aus aus einer Entwicklungsumgebung, sind die meisten IDE intelligent genug, um die virtuelle Umgebung zu erkennen und 
nutzen den korrekten Interpreter.



---------------------------------------------------------------------------------------



HINWEISE UND ANLEITUNG FUER DAS DEV TEAM !

Da die Virtualenv ziemlich groß wird, ist es empfehlenswert, die Python Version und die
requirements.txt zu sharen.

Diese sollte zentral gepflegt werden und nur vereinzelt committet !!

Wie generiere ich requirements.txt in einer Shell (bash e.g.):

            pip freeze > requirements.txt

Wie setze ich eine Virtualenv auf?
Die folgenden Befehle sind in der Console deiner Wahl einzugeben (bash, cmd, PowerShell etc.)

    - installiere in deiner Python Umgebung deiner Wahl virtualenv
            pip install virtualenv
    - führe im gewünschten Python interpreter den folgenden Befehl aus:
            py -3.8 -m virtualenv <pfad/zum/env_ordner>
    - aktiviere deine virtuelle Umgebung, um in der virtualenv die relevanten Pakete zu installieren
            source <pfad/zum/env_ordner/Scripts/activate>
    - Installiere die requirements.txt pakete:
            pip install -r </path/to/requirements.txt>


Docker Desktop Windows Erfahrung:

Mounts / Volumes
    Für bindmounts muss bei Docker Desktop unter Settings > Ressources > File Sharing der Workspace Ordner hinzugefügt werden, sodass das Shared Folder zwischen Host (dein Rechner) <-> Docker Host VM (Docker Desktop) <-> Docker Container funktioniert.


Docker run -v
    Achtet darauf wie ihr Pfade angebt in der jeweiligen shell. Nicht jedes Format funktioniert ohne weiteres.
    Windows Powershell verwendet Windowspfade wohingegen git bash bspw. POSIX Format verwendet.





------

Area Data:

https://jqplay.org/ für die Compact Erstellung der JSON Datei. jq --compact-output '.features'
