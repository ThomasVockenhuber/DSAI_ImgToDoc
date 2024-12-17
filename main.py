import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import copy
import ttkbootstrap as ttkb
import os

import image_adjustments as iaj
import text_extraction as tex

os.environ["TESSDATA_PREFIX"] = "/opt/homebrew/share/tessdata/"

# Global variables
points = []
max_points = 4
image, original_image = None, None
canvas_image = None
img_size = (588, 832)
exp_image_size, exp_img = None, None
draw_color = (189, 195, 83)
cropped = False
saved_img = None
saved = False
folder_name, name = None, None
warped_img = None

def get_text():
    global warped_img, folder_name, saved
    if saved != None:

        text = tex.extract_text(warped_img)
        text = tex.remove_extra_blank_lines(text)

        with open(folder_name + "_scan.txt", "w") as file:
            file.write(text)

def turn_img():
    if cropped == True:
        cpy_points = copy.copy(points)
        points[0] = cpy_points[2]
        points[1] = cpy_points[0]
        points[2] = cpy_points[3]
        points[3] = cpy_points[1]

        crop_and_resize_image()
        update_canvas_image()

def click_event(event):
    global points, max_points, image
    
    if len(points) < max_points:
        x, y = event.x, event.y
        points.append((x, y))

        cv.circle(image, (x, y), 5, draw_color, -1)

        if len(points) > 1:
            cv.line(image, points[-2], points[-1], draw_color, 2) 

        update_canvas_image()

        if len(points) == max_points:
            cv.line(image, points[0], points[3], draw_color, 2) 
            points = [points[0],points[1],points[3],points[2]]
            print("Maximum points reached:", points)
            crop_btn.configure(bootstyle="success")
            update_canvas_image()
    else:
        end_cropping()
            
def end_cropping():
    global points, cropped, image
    cropped = False
    save_btn.configure(bootstyle="danger")
    crop_btn.configure(text="Done Cropping")
    points = []
    image = copy.copy(original_image)
    crop_btn.configure(bootstyle="danger")
    turn_btn.configure(bootstyle="danger")
    update_canvas_image() 

def done_croping():
    global cropped, points
    if cropped:
        end_cropping()     
    elif len(points) == 4:
        crop_and_resize_image()
        save_btn.configure(bootstyle="success")
        crop_btn.configure(text="Undo Cropping")
        turn_btn.configure(bootstyle="success")
        cropped = True
    else:
        print("Not enough Points")

def save_img():
    global warped_img, folder_name, name, exp_img, exp_image_size, points, img_size, text_btn, saved

    print("Saving...")

    warped_img = iaj.warp_img(exp_img, exp_image_size, img_size, points)

    exp_img_cpy  = iaj.scan_image(warped_img)

    saved = True

    folder_name = name + '_scan'
    os.makedirs(folder_name, exist_ok=True)
    img_name = name.split('/')
    folder_name = folder_name + '/' + img_name[-1]

    cv.imwrite(folder_name + '_scan.jpeg', exp_img_cpy)

    text_btn.configure(bootstyle="success")

    im = Image.fromarray(cv.cvtColor(exp_img_cpy, cv.COLOR_BGR2RGB))
    im.save(folder_name + "_scan.pdf", "PDF")
    print("Saved")

# Function to update the image on the Tkinter canvas
def update_canvas_image():
    global image, canvas_image, tk_image, canvas
    
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    
    tk_image = ImageTk.PhotoImage(image=pil_image)

    canvas.itemconfig(canvas_image, image=tk_image)

# Function to crop and resize the image based on the four selected points
def crop_and_resize_image():
    global image, original_image, canvas_image, tk_image, canvas, points

    image = original_image

    src_points = np.float32(points)
    dst_points = np.float32([[0, 0], [img_size[0], 0], [0, img_size[1]], [img_size[0], img_size[1]]])

    matrix = cv.getPerspectiveTransform(src_points, dst_points)
    image = cv.warpPerspective(image, matrix, img_size)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY, 11, 2)

    update_canvas_image()

# Function to open the image using OpenCV and display it on Tkinter canvas
def open_image():
    global img_size, name, exp_img, exp_image_size, original_image, image, canvas_image, tk_image, canvas, points, main_frame
    
    image, name, exp_image_size = iaj.load_img()
    exp_img = copy.copy(image)

    img_size = iaj.img_size_calc(main_frame, exp_image_size)
    canvas.configure(height=img_size[1], width=img_size[0])

    corners = iaj.get_corners(image)
    points = iaj.scale_points(exp_image_size, img_size, corners)

    image = cv.resize(image, img_size)
    original_image = copy.copy(image)

    points, image = iaj.draw_frame(points, draw_color, image)

    crop_btn.configure(bootstyle="success")
    update_canvas_image()

    tk_image = iaj.img_to_tkimg(image)

    canvas_image = canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.bind("<Button-1>", click_event)

# Function to create the Tkinter UI
def create_ui():
    global canvas, crop_btn, save_btn, turn_btn, text_btn, main_frame
    
    # Use ttkbootstrap for the themed root window and style
    root = ttkb.Window(themename="flatly")  # Choose a modern theme, e.g., "flatly"
    root.title('Image Point Selector')

    # Create a frame to contain all widgets
    main_frame = ttk.Frame(root, padding=(20, 20))
    main_frame.pack(expand=True, fill="both")

    # Style and configure buttons
    open_btn = ttkb.Button(main_frame, text="Open Image", command=open_image, bootstyle="primary")
    open_btn.grid(row=0, column=0, pady=(0, 10), sticky="ew")

    crop_btn = ttkb.Button(main_frame, text="Done Cropping", command=done_croping, bootstyle="danger")
    crop_btn.grid(row=1, column=0, pady=(0, 10), sticky="ew")

    save_btn = ttkb.Button(main_frame, text="Save", command=save_img, bootstyle="danger")
    save_btn.grid(row=2, column=0, pady=(0, 10), sticky="ew")

    turn_btn = ttkb.Button(main_frame, text="Turn", command=turn_img, bootstyle="danger")
    turn_btn.grid(row=3, column=0, pady=(0, 10), sticky="ew")

    text_btn = ttkb.Button(main_frame, text="Extract Text", command=get_text, bootstyle="danger")
    text_btn.grid(row=4, column=0, pady=(0, 10), sticky="ew")

    # Create a canvas to display the image with a modern border style
    canvas = tk.Canvas(main_frame, width=img_size[0], height=img_size[1], bg="#f0f0f0", highlightthickness=1, highlightbackground="#ccc")
    canvas.grid(row=5, column=0, pady=(0, 0), sticky="nsew")

    # Make the main frame resizable
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    main_frame.rowconfigure(5, weight=1)
    main_frame.columnconfigure(0, weight=1)

    # Start the Tkinter main loop
    root.mainloop()

# Run the UI
if __name__ == "__main__":
    create_ui()
