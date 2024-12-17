import cv2 as cv
import numpy as np
from tkinter import filedialog
import copy

def get_corners(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.GaussianBlur(image, (9, 9), 0)

    # Kanten erkennen
    image = cv.Canny(image, threshold1=20, threshold2=100)
    kernel = np.ones((15, 15), np.uint8)
    image = cv.dilate(image, kernel, iterations=3)

    # Konturen finden
    contours, _ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    largest_area = 0
    largest_box = None

    # Iterate through all contours to find the largest one
    for contour in contours:
        area = cv.contourArea(contour)
        if area > largest_area:
            largest_area = area
            rect = cv.minAreaRect(contour)
            largest_box = cv.boxPoints(rect)
            largest_box = np.int32(largest_box)

    original_img_size = image.shape
    img_size = (400,600)
    proportional_size = (original_img_size[1]/img_size[0], original_img_size[0]/img_size[1])
    rezised = cv.resize(image, img_size)

    out = copy.copy(rezised)
    original_points = []

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
            
    return original_points