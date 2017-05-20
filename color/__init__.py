import cv2
import tkFileDialog
from Tkinter import *

from PIL import ImageTk, Image
import time
import numpy as np
import math
import os

import dimention


color_low  = (0,0,0)
color_high = (255,255,255)
blur_mask = (0,0)
blur_image = (0,0)
mm_pix = 0.0
blob =(0,0)
mouseblob = None

running = True

def find_mouse_blob(keypoints,mouseX,mouseY):

    smallest_distance = 99999999
    smallest_point    = None

    for points in keypoints:
        delta_x = abs(points.pt[0]-mouseX)
        delta_y = abs(points.pt[1]-mouseY)

        delta = math.sqrt(math.pow(delta_x,2)+math.pow(delta_y,2))

        if delta < smallest_distance:
            smallest_point = points
            smallest_distance = delta

    return  smallest_point

def remove_double(keypoints,space):
    new_list = []

    if len(keypoints) != 0:
        for points in keypoints:
            if len(new_list) == 0:
                new_list = [points]
            else:
                found = True
                for item in new_list:
                    delta_x = abs(points.pt[0] - item.pt[0])
                    delta_y = abs(points.pt[1] - item.pt[1])
                    lenght = math.sqrt(math.pow(delta_y, 2) + math.pow(delta_x, 2))
                    if lenght < space:
                        found = False

                if found:
                    new_list = new_list + [points]
    return new_list

class get:
    def __init__(self,imagename):
        self.image = imagename
        cv2.namedWindow("input image")
        cv2.setMouseCallback('input image', self.mouse_event)
        self.copy_image()

    def copy_image(self):
        self.image_copy = self.image.copy()

    def mouse_event(self,event, x, y, flags, param):
        global color
        global running

        if event == cv2.EVENT_MOUSEMOVE:
            self.copy_image()
            color = (int(self.image[y,x,0]),int(self.image[y,x,1]),int(self.image[y,x,2]))
            cv2.circle(self.image_copy, (x, y), 5, (0, 0, 255), 1)
            cv2.rectangle(self.image_copy, (10,10),(50,50),color,-1)

        if event == cv2.EVENT_LBUTTONUP:
            running = False

    def show(self):
        cv2.imshow("input image", self.image_copy)

def select_color(imagename):
    global running
    image = cv2.imread(imagename)
    get_color = get(image)

    while running:
        get_color.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

class getcolor:
    def __init__(self,images,outmap):
        # open window and import image
        self.outputmap = outmap
        self.low_color   = (0,0,0)
        self.heigh_color = (255,255,255)

        self.root = Toplevel()
        self.root.title("set color")
        self.image = self.outputmap + '/image.jpg'

        if self.image == 'Camera':
            cam = cv2.VideoCapture(0)
            rval, frame = cam.read()
            cv2.imshow("frame",frame)
            cv2.imwrite(self.image,frame)

        else:
            cam = cv2.VideoCapture(images)
            rval, frame = cam.read()
            cv2.imwrite(self.image,frame)


        self.cv2_image = cv2.imread(self.image)


        self.cv2_image = cv2.cvtColor(self.cv2_image, cv2.COLOR_BGR2RGB)
        self.img = ImageTk.PhotoImage(Image.fromarray(self.cv2_image))
        self.root.geometry(str(self.img.width() + 300) + "x" + str(self.img.height()))

    def event_pack(self):
        self.root.bind("<Motion>", self.update_image)
        self.panel.bind("<Button-1>",self.get_low_collor)
        self.panel.bind("<Double-Button-1>", self.get_high_collor)
        self.panel.bind('<Double-Button-2>', self.select_point)

    def select_point(self, event):
        global mouseblob
        print event.x,event.y

        if len(self.keypoints) != 0:
            mouseblob = find_mouse_blob(self.keypoints,event.x,event.y)

        print mouseblob

    def get_low_collor(self, event):
        cv2_image = cv2.imread(self.image)
        cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        self.low_color=(int(cv2_image[event.y,event.x,0]),int(cv2_image[event.y,event.x,1]),int(cv2_image[event.y,event.x,2]))
        print self.low_color

        self.red_low_slider.set(self.low_color[0])
        self.green_low_slider.set(self.low_color[1])
        self.blue_low_slider.set(self.low_color[2])
        self.update_image(None)

    def get_high_collor(self, event):
        print event.x,event.y
        cv2_image = cv2.imread(self.image)
        cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        self.heigh_color = (int(cv2_image[event.y,event.x,0]),int(cv2_image[event.y,event.x,1]),int(cv2_image[event.y,event.x,2]))
        print self.heigh_color

        self.red_high_slider.set(self.heigh_color[0])
        self.green_high_slider.set(self.heigh_color[1])
        self.blue_high_slider.set(self.heigh_color[2])
        self.update_image(None)

    def add_buttons(self):
        update_button = Button(self.root, text='Reset', command=self.reset)
        update_button.place(x=10, y=680)

        dimention_button = Button(self.root, text='Get dimention', command=self.get_dimention)
        dimention_button.place(x=80, y=680)


        load_button = Button(self.root, text='Save colors',command=self.return_value)
        load_button.place(x=200,y=680)

    def get_dimention(self):
        global mm_pix
        mm_pix = float(dimention.main(self.image))

    def loop(self):
        self.root.mainloop()
        os.remove(self.image)

    def add_image(self):
        self.panel = Label(self.root, image=self.img)
        self.panel.place(x=300, y=-2)

    def add_sliders(self):
        # red low slider
        self.red_low_slider = Scale(self.root, from_=0, to=255, length=200, orient=HORIZONTAL)
        self.red_low_slider.set(self.low_color[0])
        self.red_low_slider.place(x=80, y=40)

        # green low slider
        self.green_low_slider = Scale(self.root, from_=0, to=255, length=200, orient=HORIZONTAL)
        self.green_low_slider.set(self.low_color[1])
        self.green_low_slider.place(x=80, y=90)

        # blue low slider
        self.blue_low_slider = Scale(self.root, from_=0, to=255, length=200, orient=HORIZONTAL)
        self.blue_low_slider.set(self.low_color[2])
        self.blue_low_slider.place(x=80, y=140)

        # red higth slider
        self.red_high_slider = Scale(self.root, from_=0, to=255, length=200, orient=HORIZONTAL)
        self.red_high_slider.set(self.heigh_color[0])
        self.red_high_slider.place(x=80, y=240)

        # green higth slider
        self.green_high_slider = Scale(self.root, from_=0, to=255, length=200, orient=HORIZONTAL)
        self.green_high_slider.set(self.heigh_color[1])
        self.green_high_slider.place(x=80, y=290)

        # blue higth slider
        self.blue_high_slider = Scale(self.root, from_=0, to=255, length=200, orient=HORIZONTAL)
        self.blue_high_slider.set(self.heigh_color[2])
        self.blue_high_slider.place(x=80, y=340)

        # blur sliders image
        self.blur_imageX_slider = Scale(self.root, from_=1, to=200, length=90, orient=HORIZONTAL)
        self.blur_imageX_slider.set(0)
        self.blur_imageX_slider.place(x=80, y=440)

        self.blur_imageY_slider = Scale(self.root, from_=1, to=200, length=90, orient=HORIZONTAL)
        self.blur_imageY_slider.set(0)
        self.blur_imageY_slider.place(x=190, y=440)

        # blur sliders mask
        self.blur_maskX_slider = Scale(self.root, from_=1, to=200, length=90, orient=HORIZONTAL)
        self.blur_maskX_slider.set(0)
        self.blur_maskX_slider.place(x=80, y=490)

        self.blur_maskY_slider = Scale(self.root, from_=1, to=200, length=90, orient=HORIZONTAL)
        self.blur_maskY_slider.set(0)
        self.blur_maskY_slider.place(x=190, y=490)

        # pointsize
        self.point_size_slider = Scale(self.root, from_=0, to=50, length=200,resolution=0.01, orient=HORIZONTAL)
        self.point_size_slider.set(500)
        self.point_size_slider.place(x=80, y=570)

        # point distens between
        self.point_between_slider = Scale(self.root, from_=0, to=50, length=200,resolution=0.01,orient=HORIZONTAL)
        self.point_between_slider.set(0)
        self.point_between_slider.place(x=80, y=620)

    def reset(self):
        self.low_color = (0,0,0)
        self.heigh_color = (255,255,255)

        self.red_low_slider.set(self.low_color[0])
        self.green_low_slider.set(self.low_color[1])
        self.blue_low_slider.set(self.low_color[2])

        self.red_high_slider.set(self.heigh_color[0])
        self.green_high_slider.set(self.heigh_color[1])
        self.blue_high_slider.set(self.heigh_color[2])

        self.blur_imageX_slider.set(0)
        self.blur_imageY_slider.set(0)

        self.blur_maskX_slider.set(0)
        self.blur_maskY_slider.set(0)

        self.point_size_slider.set(500)
        self.point_between_slider.set(0)

        self.update_image(None)

    def blob_detect(self,image):
        global blob

        blob = (self.point_size_slider.get(),self.point_between_slider.get())
        detector = cv2.SimpleBlobDetector()

        # Detect blobs
        keypoints = detector.detect(image)

        new_keypoints = []
        # filter blob on size
        for points in keypoints:
            if points.size >= blob[0]:
                new_keypoints = new_keypoints +[points]

        self.keypoints = remove_double(new_keypoints,blob[1])

        # Draw detected blobs as red circles
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        return cv2.drawKeypoints(image, self.keypoints, np.array([]), (255, 0, 0),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    def update_image(self,event):
        global mouseblob

        cv2_image = cv2.imread(self.image)
        cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)

        self.low_color = (int(self.red_low_slider.get()), int(self.green_low_slider.get()), int(self.blue_low_slider.get()))
        self.heigh_color = (int(self.red_high_slider.get()), int(self.green_high_slider.get()), int(self.blue_high_slider.get()))
        self.blur_image = (self.blur_imageX_slider.get(),self.blur_imageY_slider.get())
        self.blur_mask  = (self.blur_maskX_slider.get(),self.blur_maskY_slider.get())

        low_array = np.array([self.low_color[0], self.low_color[1], self.low_color[2]])
        high_array = np.array([self.heigh_color[0], self.heigh_color[1], self.heigh_color[2]])

        #
        cv2_image = cv2.blur(cv2_image,self.blur_image)

        # generate color mask
        mask = cv2.inRange(cv2_image, low_array, high_array)
        mask = cv2.blur(mask,self.blur_mask)

        # make new image
        cv2_image = cv2.bitwise_and(cv2_image, cv2_image, mask=mask)

        # draw blobs
        cv2_image = self.blob_detect(cv2_image)

        if mouseblob != None:
            print int(mouseblob.pt[0]),int(mouseblob.pt[1])
            cv2.circle(cv2_image, (int(mouseblob.pt[0]),int(mouseblob.pt[1])), 8, (0, 255, 0), 2)

        img = ImageTk.PhotoImage(Image.fromarray(cv2_image))
        self.panel.configure(image=img)
        self.panel.image = img

    def add_label(self):
        minimum_values_label = Label(self.root,text="Minimum values",font=("Helvetica", 16))
        minimum_values_label.place(x=80,y=20)

        maximum_values_label = Label(self.root, text="Maximum values", font=("Helvetica", 16))
        maximum_values_label.place(x=80, y=220)

        blur_values_label = Label(self.root, text="Blur", font=("Helvetica", 16))
        blur_values_label.place(x=80, y=390)

        point_values_label = Label(self.root, text= "Points", font=("Helvetica", 16))
        point_values_label.place(x=80, y=550)

        red_low_label = Label(self.root,text="Red",fg="red")
        red_low_label.place(x=30,y=55)

        green_low_label = Label(self.root,text="Green",fg="green")
        green_low_label.place(x=30,y=105)

        blue_low_label = Label(self.root,text="Blue",fg="Blue")
        blue_low_label.place(x=30,y=155)

        red_high_label = Label(self.root,text="Red",fg="red")
        red_high_label.place(x=30,y=255)

        green_high_label = Label(self.root,text="Green",fg="green")
        green_high_label.place(x=30,y=305)

        blue_high_label = Label(self.root,text="Blue",fg="Blue")
        blue_high_label.place(x=30,y=355)

        blur_image_label = Label(self.root, text="Image")
        blur_image_label.place(x=30, y=455)

        blur_mask_label = Label(self.root, text="Mask")
        blur_mask_label.place(x=30, y=505)

        size_point_label = Label(self.root, text="Size")
        size_point_label.place(x=30, y=585)

        distance_point_label = Label(self.root, text="Space")
        distance_point_label.place(x=30, y=635)

        blur_width_label = Label(self.root, text="Width")
        blur_width_label.place(x=100, y=420)

        blur_height_label = Label(self.root, text="Height")
        blur_height_label.place(x=210, y=420)


    def return_value(self):
        global color_low
        global color_high
        global blur_image
        global blur_mask
        global mm_pix

        color_low  = self.low_color
        color_high = self.heigh_color
        blur_image = self.blur_image
        blur_mask  = self.blur_mask

        if mm_pix == 0.00:
            mm_pix = dimention.main(self.image)

        self.root.destroy()
        self.root.quit()

def main(filename,ouputmap):
    global color_low
    global color_high
    global blur_mask
    global blur_image
    global mouseblob

    findcolor = getcolor(filename,ouputmap)
    findcolor.add_sliders()
    findcolor.add_label()
    findcolor.add_buttons()
    findcolor.add_image()
    findcolor.event_pack()
    findcolor.loop()

    return color_low,color_high,blur_image,blur_mask,blob,mm_pix,mouseblob

if __name__ == "__main__":
    main('path')
