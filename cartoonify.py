# imports
import cv2 # to process images
import easygui # to choose files
import numpy as np # arrays for storing images
import imageio # read file from file box
import matplotlib.pyplot as plt # plotting
import sys
import os
import tkinter as tk # creating GUI elements
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image



# To choose file using fileopenbox()
def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)


# ImagePath = easygui.fileopenbox()
def cartoonify(ImagePath):
    # Store image
    imageOrig = cv2.imread(ImagePath)
    imageOrig = cv2.cvtColor(imageOrig, cv2.COLOR_BGR2RGB)

    # Check if image is chosen
    if imageOrig is None:
        print("Please choose an image file.")
        sys.exit()

    # Resize image
    imageResized1 = cv2.resize(imageOrig, (960,540))
    # plt.imshow(imageResized1, cmap='gray')

    # To grayscale
    imageGrayscale = cv2.cvtColor(imageOrig, cv2.COLOR_BGR2GRAY)
    imageResized2 = cv2.resize(imageGrayscale, (960,540))
    # plt.imshow(imageResized2, cmap='gray')

    # Blur photo
    imageGraySmooth = cv2.medianBlur(imageGrayscale, 5)
    imageResized3 = cv2.resize(imageGraySmooth, (960,540))
    # plt.imshow(imageResized3, cmap='gray')

    # Getting borders to emphasize for cartoon
    getEdge = cv2.adaptiveThreshold(imageGraySmooth, 255,
              cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9,9)
    imageResized4 = cv2.resize(getEdge, (960,540))
    # plt.imshow(imageResized4, cmap='gray')

    # Bilateral filter to keep edges and remove noise
    imageColor = cv2.bilateralFilter(imageOrig, 9, 300, 300)
    imageResized5 = cv2.resize(imageColor, (960, 540))
    # plt.imshow(imageResized5, cmap='gray')


    # Mask smoothed and cartoon together
    imageCartoon = cv2.bitwise_and(imageColor, imageColor, mask=getEdge)
    imageResized6 = cv2.resize(imageCartoon, (960,540))
    plt.imshow(imageResized6, cmap='gray')


    # Show transformation
    images = [imageResized1, imageResized2, imageResized3, imageResized4,
            imageResized5, imageResized6]
    fig, axes = plt.subplots(3,2)
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    plt.show()



# Making window
top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image!')
top.configure(background='#23395D')
label=Label(top,background='black')

# Upload Button UI
uploadBut = Button(top, text = "Cartoonify", command = upload, padx=10, pady=5)
uploadBut.configure(background='#364156', foreground='black')
uploadBut.pack(side=TOP, pady=50)

top.mainloop()
