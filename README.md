# Installieren and Verwenden

## Installation

Zuerst muss auf dem Lokalen rechner Python (version 3.13.0) installiert werden.
Danach muss das venv für dieses Projekt intalliert und verwendet werden.
`source venv/bin/activate`
Nun kann das Projekt gestartet werden.

## Verwendung

### Starten

Nachdem das venv verwendet wurde kann man mit dem Befehl `python3 main.py` das Projekt starten. Sollte sich das Fenster nicht gleich öffenen, kann es sein dass man über die Taskleiste darauf zugreifen muss.

### Verwenden

#### Ausschneiden
Nun kann man über die Taste **Open Image** ein Bild ausgewählt werden. Das Programm versucht nun automatisch die Ecken des Dokuments zu erkennen, sollte die erkennung nicht funktioniert haben und der vorgezeichnente Ramen nicht stimmen kann der Ramen auch manuell eingestellt werden. Dazu klick man auf das Bild um den alten Ramen zu löschen und Beginnt bei der oberen linken Ecke die Ecken im Uhrzeigersinn mit einem Mausklick zu makieren.
Ist man nun zufrieden kann man das Dokument mit **Done Cropping** ausscheniden und Auf die Richtige größte vormen. Nun sollte man das Bild in schlechter Qualität in der Vorschau sehen, mit **Undo Cropping** kann man dies Wieder rückgängig machen und den Ramen neu Wählen.
Mit dem Taster **Turn** kann das Dokument im Uhrzeiersinn gedreht werden.

#### Speichern
Sollte die Vorschau passen (Wenn die Vorschau unreinheiten enthällt werden diese meist in den gespeicherten Files entfernt), kann man mit **Save** das Dokument Speichern (Dies kann einige Sekunden dauern) es wird dafür neben dem Spicherort des Bildes ein Ordner mit dem "Namen"_scan erstellt. In diesem werden nun das Dokument als .jpg und .pdf gespeichert.

* Alle Befehle in diesem Dokument sind für MAC-OS