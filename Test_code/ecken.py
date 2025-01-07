import cv2 as cv
import numpy as np
from tkinter import filedialog
import copy

def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Datei auswählen und Bild laden
file_path = filedialog.askopenfilename()
image = cv.imread(file_path)
original_img = copy.copy(image)

cv.imshow('Gefilterte Eckenerkennung', image)
cv.waitKey(0)
cv.destroyAllWindows()

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
blured = cv.GaussianBlur(gray, (9, 9), 0)

cv.imshow('Gefilterte Eckenerkennung', blured)
cv.waitKey(0)
cv.destroyAllWindows()

# Kanten erkennen
edged_image = cv.Canny(blured, threshold1=20, threshold2=100)
#closing = cv.dilate(edged_image,(100,100),iterations = 5)

kernel = np.ones((15, 15), np.uint8)  # Größeren Kern verwenden
closing = cv.dilate(edged_image, kernel, iterations=2)

cv.imshow('Gefilterte Eckenerkennung', closing)
cv.waitKey(0)
cv.destroyAllWindows()

_,thr_img = cv.threshold(gray, np.mean(gray)-20, 255, cv.THRESH_BINARY)
kernel = np.ones((15, 15), np.uint8)
thr_img = cv.dilate(thr_img, kernel, iterations=4)

cv.imshow('Gefilterte Eckenerkennung', thr_img)
cv.waitKey(0)
cv.destroyAllWindows()

closing = cv.bitwise_and(closing, thr_img)

cv.imshow('Gefilterte Eckenerkennung', closing)
cv.waitKey(0)
cv.destroyAllWindows()

# Konturen finden
contours, _ = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

largest_box = max(contours, key=lambda c: cv.contourArea(c), default=None)
rect = cv.minAreaRect(largest_box)
largest_box = np.int32(cv.boxPoints(rect))

# Now draw only the largest box if it exists
if largest_box is not None:
    cv.drawContours(closing, [largest_box], 0, (100, 0, 0), 2)  # Using a color tuple for BGR

print(largest_box)

cv.imshow('Gefilterte Eckenerkennung', closing)
cv.waitKey(0)
cv.destroyAllWindows()

original_img_size = closing.shape
img_size = (400,600)
proportional_size = (original_img_size[1]/img_size[0], original_img_size[0]/img_size[1])
rezised = cv.resize(closing, img_size)

out = copy.copy(rezised)
original_points = []

cv.imshow('Gefilterte Eckenerkennung', rezised)
cv.waitKey(0)
cv.destroyAllWindows()

# Assuming `resized` is a binary image (with 255 for white points and 0 for black)
white_points = np.argwhere(rezised == 255)  # Get all white points' coordinates

for corner in largest_box:
    nearest = None
    min_distance = float('inf')  # Set a high initial distance

    pointX = round(corner[0] / proportional_size[0])
    pointY = round(corner[1] / proportional_size[1])

    print(f"{pointX},{pointY}")

    cv.circle(out, (pointX, pointY), 5, 170, -1)

    # Loop over all white points to find the closest one
    for white_point in white_points:
        whiteY, whiteX = white_point

        # Calculate the Euclidean distance
        distance = np.sqrt((whiteX - pointX)**2 + (whiteY - pointY)**2)

        # Update if this white point is closer
        if distance < min_distance:
            min_distance = distance
            nearest = [whiteX, whiteY]

    print(nearest)
    if nearest:
        cv.circle(out, nearest, 5, 100, -1)
        original_points.append([round(nearest[0]*proportional_size[0]), round(nearest[1]*proportional_size[1])] )
        print(original_points)


cv.imshow('Gefilterte Eckenerkennung', out)
cv.waitKey(0)
cv.destroyAllWindows()
        
for original_point in original_points:
    cv.circle(original_img, original_point, 40, (255,0,0), -1)

cv.imshow('Gefilterte Eckenerkennung', original_img)
cv.waitKey(0)
cv.destroyAllWindows()

"""
# Neues Bild für die gefilterten Kanten erstellen
filtered_edges = np.zeros_like(closing)

# Konturen filtern nach einer Mindestlänge (z.B. 50 Pixel)
min_length = 2000
for contour in contours:
    if cv.arcLength(contour, closed=False) > min_length:
        cv.drawContours(filtered_edges, [contour], -1, 255, 1)

cv.imwrite('save.jpg', filtered_edges)

# Ergebnis anzeigen
cv.imshow('Gefilterte Eckenerkennung', filtered_edges)
cv.waitKey(0)
cv.destroyAllWindows()
"""