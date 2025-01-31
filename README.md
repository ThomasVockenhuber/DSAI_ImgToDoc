# Installieren and Verwenden

## Installation

Zuerst muss auf dem Lokalen rechner Python (version 3.13.0) installiert werden.
Danach das Projekt.

``` git clone https://github.com/ThomasVockenhuber/DSAI_ImgToDoc.git ```

Nun muss das venv für dieses Projekt verwendet werden. `source venv/bin/activate`
Das Projekt kann nun gestartet werden.

Damit die Texterkennung funktioniert muss `tessdata/deu` installiert sein und im main.py file der Pfad dorthin je nach speicherort angepasst werden.
`os.environ["TESSDATA_PREFIX"] = "/opt/homebrew/share/tessdata/"`

## Verwendung

### Starten

Nachdem das venv verwendet wurde kann man mit dem Befehl `python3 main.py` das Projekt starten. Sollte sich das Fenster nicht gleich öffenen, kann es sein dass man über die Taskleiste darauf zugreifen muss.

### Verwenden

#### Ausschneiden
Nun kann man über die Taste **Open Image** ein Bild ausgewählt werden. Das Programm versucht nun automatisch die Ecken des Dokuments zu erkennen, sollte die erkennung nicht funktioniert haben und der vorgezeichnente Ramen nicht stimmen (Dies kann passieren wenn der Kontrast zwischen Hintergrund und Papier zu klein ist oder das Papier kein weißes Dokument ist) kann der Ramen auch manuell eingestellt werden. Dazu klick man auf das Bild um den alten Ramen zu löschen und Beginnt bei der oberen linken Ecke die Ecken im Uhrzeigersinn mit einem Mausklick zu makieren.
Ist man nun zufrieden kann man das Dokument mit **Done Cropping** ausscheniden und Auf die Richtige größte vormen. Nun sollte man das Bild in schlechter Qualität in der Vorschau sehen, mit **Undo Cropping** kann man dies Wieder rückgängig machen und den Ramen neu Wählen.
Mit dem Taster **Turn** kann das Dokument im Uhrzeiersinn gedreht werden.

#### Speichern
Sollte die Vorschau passen (Wenn die Vorschau unreinheiten enthällt werden diese meist in den gespeicherten Files entfernt), kann man mit **Save** das Dokument Speichern (Dies kann einige Sekunden dauern) es wird dafür neben dem Spicherort des Bildes ein Ordner mit dem "Namen"_scan erstellt. In diesem werden nun das Dokument als .jpg und .pdf gespeichert.

#### Text Extrahieren
Nachdem das Dokument gespeichert wurde, kann der Text mit der **Extract Text** Taste extrahiert werden. Dieser Text wird als .txt in dem Ordner abgespeichert. Die Sprache ist auf Deutsch eingestellt, deshalb könnte das Programm mit anderen Sprachen probleme haben. Sollte das Dokument viele Vormen haben kann das Programm diese auch fehlerhalt als Text lesen.

> Alle Befehle in diesem Dokument sind für MAC-OS

# Funktionsweise

## Umgebung

## Eckenerkennung

Die Eckenerkennung ist der Schwierigste Teil des Projektes deshab habe ich mich dazu entschlossen diesen hier, mit ein paar Code Beispieben und Bildern genauer zu beschreiben.

Zuerst wird das Bild in diese Funktion geladen. Hier ist das Beispiel Bild.

<img src="./README_images/0.png" alt="Bsp Image" width="200">

Zuerst wird das Bild leicht verschwommen um Rauschen zu entfernen und zu Graustufen umgewandelt.

``` 
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
blured = cv.GaussianBlur(gray, (9, 9), 0) 
```

<img src="./README_images/1.png" alt="Gray Image" width="200">

Nun werded die Ecken erkannt und vergrößert, damit kleine Lücken geschlossen werden.

```
edges = cv.Canny(blured, threshold1=20, threshold2=100)
kernel = np.ones((15, 15), np.uint8)
ecken_vergrößert = cv.dilate(edges, kernel, iterations=2)
```

<img src="./README_images/2.png" alt="Edge Image" width="200">

Hier werden die Hellen stellen des Bildes gefundenn und mit einem dicken Ramen umramt, damit kleine dunkle Flecken wie z.B. Buchstaben nicht entfernt werden werden.

```
_,thr_img = cv.threshold(gray, np.mean(gray)-20, 255, cv.THRESH_BINARY)
kernel = np.ones((15, 15), np.uint8)
thr_img = cv.dilate(thr_img, kernel, iterations=4)
```

<img src="./README_images/3.png" alt="Alt Text" width="200">

nun Werden alle Ecken, welche im Dunklen bereich des Bildes sind entfernt.

```
ecken = cv.bitwise_and(ecken_vergrößert, thr_img)
```

<img src="./README_images/4.png" alt="Alt Text" width="200">

Nun werden mögliche rechteckige Konturen des Dokuments gefunden und die, welche die größte Fläche hat wird als die Kontur des Dokuments gewählt.
```
contours, _ = cv.findContours(ecken, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
largest_box = max(contours, key=lambda c: cv.contourArea(c), default=None)
rect = cv.minAreaRect(largest_box)
largest_box = np.int32(cv.boxPoints(rect))
```

<img src="./README_images/5.png" alt="Alt Text" width="200">

Nun wird das Bild auf eine kleinere Größe komprimiert, damit der nächste schritt nicht so lange braucht.
```
img_size = (400,600)
proportional_size = (original_img_size[1]/img_size[0], original_img_size[0]/img_size[1])
rezised = cv.resize(ecken, img_size)
```

<img src="./README_images/6.png" alt="Alt Text" width="200">

Hier werden von den Ecken der Kontur die nächsten Punkte des Papiers gefunden, diese werden schließlich als die Ecken des Dokuments gewählt.
```
white_points = np.argwhere(rezised == 255)

for corner in largest_box:
    min_distance = float('inf')

    pointX = round(corner[0] / proportional_size[0])
    pointY = round(corner[1] / proportional_size[1])

    nearest = None
    for white_point in white_points:
        whiteY, whiteX = white_point
        distance = np.sqrt((whiteX - pointX)**2 + (whiteY - pointY)**2)

        if distance < min_distance:
            min_distance = distance
            nearest = [whiteX, whiteY]

    corners.append(nearest[0], nearest[1])
```

<img src="./README_images/7.png" alt="Alt Text" width="200">

Nun müssen die Ecken wieder auf die Orginalgrößre angepasst werden.
```
original_corners = [round(nearest[0]*proportional_size[0]), round(nearest[1]*proportional_size[1])]
```

<img src="./README_images/8.png" alt="Alt Text" width="200">

## Dokument Scannen

Um das Dokument zu scannen wird nun das Bild so verzerrt, dass die gefundenen Ecken, die Ecken des entstehenden Bildes sind.

Danach wird ein Threshold berechnet und damit die Schrift Schwarz und das Blatt Weiß gemacht. Kleine Artefakte werden davor mittels Gausschen Blurr entfernt.

Weitere Kleine Artefakte, welche aber so eine größe haben, dass sie nahe an die Größe der i Punkte oder Kommas kommen, werden manuell durch einen Algorithmus entfernt.

Schlussendlich wird das Dokument als JPEG und PDF abgespeichert.

## Text Extrahieren

Um den Text aus dem Gescannten Dokument zu extrahieren, muss ein Neuronales Netzwerk angewendet werden. Da das Trainieren eines solchen Modells zu kompiziert für dieses Projekt wäre habe ich mich entschieden `pytesseract` dafür zu verwenden.

Dafür wird nur ein Simpler Code verwendet:

```
_, thresh = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
text = pytesseract.image_to_string(thresh, lang="deu")

pattern = r'\b[a-zA-Z0-9]\b'
text = re.sub(pattern, '', text)
```

Zuwest wird das Bild noch angepasst um gut weiterverarbeitet zu werden dann wird der Text extrahiert. Die Sprache ist auf deutsch gestellt, sollten andere Sprachen verwendet werden müssen diese installiert und hier manuell geändert werden.

Danach wird der Text gefiltert und nur Buchstaben so wie Zahlen werden akzeptiert, da sonnst of Striche und Artefakte als Text erkannt werden.

# Probleme

## Umgebung

Ein großes Problem war es, dass je nachdem wo ich das Foto des Dokuments machte die Belichtung so wie der Hintergrund sich änderte. So stellte ich oft die Parameter zu strickt und die Erkennung funktionierte nur bei den Testfotos.
Sollte jemand wieder so ein Projekt probieren würde ich als ersten Schritt empfehlen nicht nur ein schnelles Bild zum probieren zu machen, sondern gleich mehrere unterschiedliche und diese vorallem auch nach jeder änderung zu testen um sich Probleme am ende des Projektes zu ersparen.

## Abhängigkeiten

Auch war es schwierig für alle Libraries die verwendet wurden alle Abhängigkeiten zu installieren. Denn diese wurden oft erst erwähnt wenn ich mittels der Fehlernachricht nach diesen gesucht habe, nicht aber bei den schritten der Installation die im Internet vorgeschlagen wurden.
Ich hätte mir viel Zeit ersparrt, hätte ich diese Fehlermelungen einfach Chat-GPT geschickt und gefragt was ich tun sollte. Denn im Internet findet man meist bessere Lösungen aber man braucht meist viel mehr zeit diese zu finden.

## Einfachere Lösungen

Die idee dieses Projektes war nicht die einfachste Lösung zu dem Problem zu finden, denn dafür gibt es warscheinlich hunderte fertige Projekte. Dieses Projekt sollte aber selbst gemacht sein, dies war aber auch ein Problem, denn viele Lösungen zu Problemen die ich hatte waren zu einfach, sie würden das Projekt mit einem Fertigen ersetzen.