Roman, Patrick Nam Coden in der Luft


Docker Desktop Windows Erfahrung:

Mounts / Volumes
    Für bindmounts muss bei Docker Desktop unter Settings > Ressources > File Sharing der Workspace Ordner hinzugefügt werden, sodass das Shared Folder zwischen Host (dein Rechner) <-> Docker Host VM (Docker Desktop) <-> Docker Container funktioniert.



Docker run -v
    Achtet darauf wie ihr Pfade angebt in der jeweiligen shell. Nicht jedes Format funktioniert ohne weiteres.
    Windows Powershell verwendet Windowspfade wohingegen git bash bspw. POSIX Format verwendet.


Setup:

setup.sh Skript muss noch geschrieben werden.
Das Skript muss im root Ordner vom Projekt / Workspace ausgeführt werden.