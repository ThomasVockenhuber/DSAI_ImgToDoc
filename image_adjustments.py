import cv2 as cv
import numpy as np
import copy
from tkinter import filedialog
from PIL import Image, ImageTk

mainfame_padding = (40, 257)

def get_corners(image):

    color_img = image
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.GaussianBlur(gray, (9, 9), 0)

    # Kanten erkennen
    image = cv.Canny(image, threshold1=30, threshold2=120)
    kernel = np.ones((15, 15), np.uint8)
    image = cv.dilate(image, kernel, iterations=2)


    # Farbbereiche entfernen
    color_img = color_img.astype(np.float32) / 255.0
    diff_rg = np.abs(color_img[:, :, 0] - color_img[:, :, 1])  # Difference between R and G
    diff_rb = np.abs(color_img[:, :, 0] - color_img[:, :, 2])  # Difference between R and B
    diff_gb = np.abs(color_img[:, :, 1] - color_img[:, :, 2])  # Difference between G and B

    threshold = 0.15
    mask = (diff_rg < threshold) & (diff_rb < threshold) & (diff_gb < threshold)

    mask = (mask * 255).astype(np.uint8)  
    kernel = np.ones((10, 10), np.uint8)
    mask = cv.dilate(mask, kernel, iterations=2) 
    mask = (mask * 255).astype(np.uint8)
    image = cv.bitwise_and(image, image, mask=mask)



    # Nicht weiße objekte entfernen
    color_img = color_img.astype(np.float32) * 255.0
    color_img = cv.GaussianBlur(color_img, (101,101),0)
    hsv = cv.cvtColor(color_img, cv.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 140])   # Adjust based on brightness
    upper_white = np.array([255, 40, 255]) 

    mask = cv.inRange(hsv, lower_white, upper_white)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=2)  # Close gaps
    kernel = np.ones((100, 100), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1)   # Remove small noise
    image = cv.bitwise_and(image, image, mask=mask)

    # Konturen finden
    kernel = np.ones((100, 100), np.uint8)  # Größeren Kern verwenden
    cc = cv.dilate(image, kernel, iterations=2)
    contours, _ = cv.findContours(cc, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

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

        if nearest:
            cv.circle(out, nearest, 5, 100, -1)
            original_points.append([round(nearest[0]*proportional_size[0]), round(nearest[1]*proportional_size[1])] )
            
    return original_points

def adjust_points(points, original_size, new_size):
    original_width, original_height = original_size
    new_width, new_height = new_size
    
    # Calculate scaling factors
    scale_x = new_width / original_width
    scale_y = new_height / original_height
    
    # Adjust each point
    adjusted_points = [(int(x * scale_x), int(y * scale_y)) for (x, y) in points]
    return adjusted_points

def warp_img(exp_img, exp_image_size, img_size, points):
    exp_img_cpy = copy.copy(exp_img)

    adjusted_points = adjust_points(points, img_size, exp_image_size)
    src_points = np.float32(adjusted_points)
    dst_points = np.float32([[0, 0], [exp_image_size[0], 0], [0, exp_image_size[1]], [exp_image_size[0], exp_image_size[1]]])

    # Compute the perspective transformation matrix
    matrix = cv.getPerspectiveTransform(src_points, dst_points)

    # Apply the perspective transformation
    exp_img_cpy = cv.warpPerspective(exp_img_cpy, matrix, exp_image_size)

    return cv.cvtColor(exp_img_cpy, cv.COLOR_BGR2GRAY)

def scan_image(gray):
    gray = cv.GaussianBlur(gray, (7, 7), 0)
    #gray = cv.GaussianBlur(gray, (7, 7), 0)

    # Step 3: Apply adaptive thresholding for a scanned effect
    exp_img_cpy = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY, 11, 3)


    # Invert the image (optional: small black -> small white)
    inverted = cv.bitwise_not(exp_img_cpy)

    # Find connected components
    num_labels, labels, stats, _ = cv.connectedComponentsWithStats(inverted, connectivity=8)

    # Remove small components
    min_size = 50  # Adjust this threshold as needed
    filtered_image = np.zeros_like(inverted)

    for i in range(1, num_labels):  # Skip the background label
        if stats[i, cv.CC_STAT_AREA] >= min_size:
            filtered_image[labels == i] = 255

    # Invert back to restore the original format
    exp_img_cpy = cv.bitwise_not(filtered_image)

    return copy.copy(exp_img_cpy)

def scale_points(exp_image_size, img_size, corners):
    original_width, original_height = exp_image_size
    new_width, new_height = img_size
    
    scale_x = new_width / original_width
    scale_y = new_height / original_height 
    
    return [(int(x * scale_x), int(y * scale_y)) for (x, y) in corners]

def draw_frame(points, draw_color, image):
    for point in points:
        cv.circle(image, point, 5, draw_color, -1)

    cv.line(image, points[0], points[1], draw_color, 2) 
    cv.line(image, points[1], points[2], draw_color, 2) 
    cv.line(image, points[2], points[3], draw_color, 2) 
    cv.line(image, points[3], points[0], draw_color, 2) 

    return [points[1],points[2],points[0],points[3]], image

def img_size_calc(main_frame, exp_image_size):
    default_img_size = main_frame.winfo_width()-mainfame_padding[0], main_frame.winfo_height()-mainfame_padding[1]
    factor = default_img_size[1]/exp_image_size[1]
    if default_img_size[0]/exp_image_size[0] < factor: factor = default_img_size[0]/exp_image_size[0]
    return round(factor*exp_image_size[0]), round(factor*exp_image_size[1])

def load_img():
    file_path = filedialog.askopenfilename()
    image = cv.imread(file_path)
    name = file_path.split('.')[0]
    x,y,_ = image.shape
    exp_image_size = y,x

    return image, name, exp_image_size

def img_to_tkimg(image):
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    return ImageTk.PhotoImage(image=pil_image)