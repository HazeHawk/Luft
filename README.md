Roman, Patrick Nam Coden in der Luft


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


Setup:

setup.sh Skript muss noch geschrieben werden.
Das Skript muss im root Ordner vom Projekt / Workspace ausgeführt werden.
