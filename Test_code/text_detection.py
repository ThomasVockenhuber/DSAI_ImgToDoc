import cv2
import pytesseract
import os
os.environ["TESSDATA_PREFIX"] = "/opt/homebrew/share/tessdata/"

# Pfad zur Tesseract-Installation (nur für Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Pfad\zu\tesseract.exe'

# Bild laden
image = cv2.imread("img2_scan.jpeg")

# Bild in Graustufen umwandeln
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Bild vorverarbeiten (z.B. Rauschen entfernen)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# OCR mit Tesseract
text = pytesseract.image_to_string(thresh, lang="deu")  # 'deu' für deutsche Sprache

# Ergebnis ausgeben
print("Erkannter Text:")
print(text)

# Bild anzeigen (optional)
cv2.imshow("Vorverarbeitetes Bild", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
