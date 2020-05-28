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




