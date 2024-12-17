# Installieren and Verwenden

## Installation

Zuerst muss auf dem Lokalen rechner Python (version 3.13.0) installiert werden.
Danach das Projekt.

``` git clone https://github.com/ThomasVockenhuber/DSAI_ImgToDoc.git ```

Nun muss das venv für dieses Projekt verwendet werden. `source venv/bin/activate`
Das Projekt kann nun gestartet werden.

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

#### Text Extrahieren
Nachdem das Dokument gespeichert wurde, kann der Text mit der **Extract Text** Taste extrahiert werden. Dieser Text wird als .txt in dem Ordner abgespeichert. Die Sprache ist auf Deutsch eingestellt, deshalb könnte das Programm mit anderen Sprachen probleme haben. Sollte das Dokument viele Vormen haben kann das Programm diese auch fehlerhalt als Text lesen.

> Alle Befehle in diesem Dokument sind für MAC-OS

# Funktionsweise

## Umgebung

## Dokument Scannen
Zuerst wird das Bild in diese Funktion geladen. Hier ist das Beispiel Bild.
<img src="./README_images/0.png" alt="Alt Text" width="200">
Zuerst wird das Bild leicht verschwommen um Rauschen zu entfernen und zu Graustufen umgewandelt.

``gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
blured = cv.GaussianBlur(gray, (9, 9), 0)``

<img src="./README_images/1.png" alt="Alt Text" width="200">
<img src="./README_images/2.png" alt="Alt Text" width="200">
<img src="./README_images/3.png" alt="Alt Text" width="200">
<img src="./README_images/4.png" alt="Alt Text" width="200">
<img src="./README_images/5.png" alt="Alt Text" width="200">

### Eckenerkennung

### Artefakte Entfernen

## Text Extrahieren