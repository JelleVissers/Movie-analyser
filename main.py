import color
import filter

import cv2
import tkFileDialog
import numpy as np
import math
import os
from Tkinter import *
import tkMessageBox
import tkSimpleDialog

filename    = None
outputmap   = None
pixel_mm    = None
color_min   = None
color_max   = None
blur_img    = None
blur_mask   = None
size_point  = None
space_point = None
frames_sec  = None
mouse_blob  = None
data        = []
speed       = 10

def settings():
    global filename
    global outputmap
    global pixel_mm
    global color_min
    global color_max
    global blur_img
    global blur_mask
    global size_point
    global space_point

    if filename == None:
        tkMessageBox.showerror("Error",'No plot imported')

    else:
        if outputmap == None:
            tkMessageBox.showerror("Error", 'Export directory not initialized')
        else:
            color_min, color_max, blur_img, blur_mask, blob, pixel_mm =  color.main(filename,outputmap)

            size_point  = blob[0]
            space_point = blob[1]

def blob_detect(image):
    global size_point
    global space_point

    blob = (size_point, space_point)
    detector = cv2.SimpleBlobDetector()

    # Detect blobs
    keypoints = detector.detect(image)

    new_keypoints = []
    # filter blob on size
    for points in keypoints:
        if points.size >= blob[0]:
            new_keypoints = new_keypoints + [points]

    keypoints = color.remove_double(new_keypoints, blob[1])

    # Draw detected blobs as red circles
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    return cv2.drawKeypoints(image, keypoints, np.array([]), (255, 0, 0),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS),keypoints

def change_place(keypoint,data):
    delta_x = abs(abs(keypoint.pt[0])-abs(data[0]/pixel_mm))
    delta_y = abs(abs(keypoint.pt[1])-abs(data[1]/pixel_mm))
    change  = math.sqrt(math.pow(delta_x,2)+math.pow(delta_y,2))
    return change

def find_next_blob(keypoints,data):
    global pixel_mm

    last_point = data[len(data)-1]

    old_x = last_point[0] / pixel_mm
    old_y = last_point[1] / pixel_mm

    print old_x,old_y

    smallest_distance = 99999999
    smallest_point    = None

    for points in keypoints:
        delta_x = abs(points.pt[0]-abs(old_x))
        delta_y = abs(points.pt[1]-abs(old_y))

        delta = math.sqrt(math.pow(delta_x,2)+math.pow(delta_y,2))

        if delta < smallest_distance:
            smallest_point = points
            smallest_distance = delta

    print smallest_point.pt[0],smallest_point.pt[1]

    print "\n"

    return  smallest_point

def analyse():
    global filename
    global outputmap
    global pixel_mm
    global color_min
    global color_max
    global blur_img
    global blur_mask
    global size_point
    global space_point
    global frames_sec
    global data
    global mouse_blob
    global speed

    #calculate time per frame (ms):
    time = float(1000.0000/float(frames_sec))

    if filename == "Camera":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(filename)

    low_array = np.array([color_min[0], color_min[1], color_min[2]])
    high_array = np.array([color_max[0], color_max[1], color_max[2]])
    data = []   # [[x1,y1,time-1],[x2,y2,time-2]]

    while True:
        flag, frame = cap.read()

        if flag:
            framenummer = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = cv2.blur(frame,blur_img)

            # generate color mask
            mask = cv2.inRange(frame, low_array, high_array)

            mask = cv2.blur(mask, blur_mask)

            # make new image
            frame_mask = cv2.bitwise_and(frame, frame, mask=mask)
            frame_blob,keypoints = blob_detect(frame_mask)
            #cv2.imshow('video', cv2.cvtColor(frame_blob, cv2.COLOR_RGB2BGR))

            if len(data) == 0:

                x = mouse_blob.pt[0]
                y = mouse_blob.pt[1]

                point = color.find_mouse_blob(keypoints,x,y)
                print point.pt[0], point.pt[1]
                data = [[point.pt[0] * pixel_mm, point.pt[1] * pixel_mm, framenummer * time]]
            else:
                if len(keypoints) == 1:
                    change = change_place(keypoints[0], data[len(data) - 1])

                    print 'first:\t'+str(change)

                    if change < (speed*pixel_mm):
                        data = data + [[keypoints[0].pt[0]*pixel_mm,keypoints[0].pt[1]*pixel_mm,framenummer * time]]

                elif len(keypoints) == 0:
                    print "no points found"

                else:
                    point = find_next_blob(keypoints, data)

                    change = change_place(point, data[len(data) - 1])
                    print 'second:\t' + str(change)

                    if change < (speed*pixel_mm):
                        data = data + [[point.pt[0] * pixel_mm, point.pt[1] * pixel_mm, framenummer * time]]


#            if len(keypoints) != 0:
#                if len(keypoints) == 1:
#                    if len(data) != 0:
#                        change = change_place(keypoints[0],data[len(data)-1])
#                        print 'first:\t'+str(change)
#                        if change < (speed*pixel_mm):
#                            data = data + [[keypoints[0].pt[0]*pixel_mm,keypoints[0].pt[1]*pixel_mm,framenummer * time]]
#                    else:
#                        x = mouse_blob.pt[0]
#                        y = mouse_blob.pt[1]
#                        print x, y
#                        keypoint = find_next_blob(keypoints, [x, y, 0])
#                        print keypoint[0].pt[0], keypoint[0].pt[1]
#                        data = [[keypoint[0].pt[0] * pixel_mm, keypoint[0].pt[1] * pixel_mm, framenummer * time]]

#                else:
#                    if len(data) == 0:
#                        x = mouse_blob.pt[0]
#                        y = mouse_blob.pt[1]
#                        print x,y
#                        keypoint = find_next_blob(keypoints,[x,y,0])
#                        print keypoint[0].pt[0],keypoint[0].pt[1]
#                        data = data + [[keypoint[0].pt[0] * pixel_mm, keypoint[0].pt[1] * pixel_mm, framenummer * time]]


#                    else:
#                        keypoints = find_next_blob(keypoints,data[len(data)-1])

#                        change = change_place(keypoints[0], data[len(data) - 1])
#                        'second:\t' + str(change)

#                        if change < (speed*pixel_mm):
#                            data = data + [[keypoints[0].pt[0] * pixel_mm, keypoints[0].pt[1] * pixel_mm, framenummer * time]]

        else:
            cv2.destroyAllWindows()
            break

        if len(data) >0:
            last_point = data[len(data)-1]

            X_last = int(last_point[0]/pixel_mm)
            Y_last = int(last_point[1]/pixel_mm)

            cv2.circle(frame_blob,(X_last,Y_last),20,(0,255,0),4)
            cv2.imshow('video', cv2.cvtColor(frame_blob, cv2.COLOR_RGB2BGR))

        if cv2.waitKey(10) == 27:
            cv2.destroyAllWindows()
            break
    plot_ask = tkMessageBox.askyesno("Plot","Do you want to plot the results")

    if plot_ask:
        #plot gegevens
        print data
        filter.main(data)

class window:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("330x460")
        self.window.title("Movie Analyser")

    def settings(self):
        global filename
        global outputmap
        global pixel_mm
        global color_min
        global color_max
        global blur_img
        global blur_mask
        global size_point
        global space_point
        global mouse_blob

        if filename == None:
            tkMessageBox.showerror("Error", 'No image imported')

        else:
            if outputmap == None:
                tkMessageBox.showerror("Error", 'Export directory not initialized')
            else:
                color_min, color_max, blur_img, blur_mask, blob, pixel_mm, mouse_blob = color.main(filename, outputmap)

                size_point = blob[0]
                space_point = blob[1]
                print mouse_blob

        self.update_var_label()

    def add_button(self):
        run_button = Button(self.window, text="analyse", command=analyse)
        run_button.place(x=220, y=420)

        setting_button = Button(self.window, text="change settings", command=self.settings)
        setting_button.place(x=20, y=420)

    def add_var_labels(self):
        global filename
        global outputmap
        global pixel_mm
        global color_min
        global color_max
        global blur_img
        global blur_mask
        global size_point
        global space_point
        global frames_sec

        self.var_input_str       = StringVar()
        self.var_output_str      = StringVar()
        self.var_pix_mm_str      = StringVar()
        self.color_min_str       = StringVar()
        self.color_max_str       = StringVar()
        self.blur_image_str      = StringVar()
        self.blur_mask_str       = StringVar()
        self.min_point_size_str  = StringVar()
        self.min_point_space_str = StringVar()
        self.var_frames_sec_str  = StringVar()

        self.var_input_str.set(str(filename))
        self.var_output_str.set(str(outputmap))
        self.var_pix_mm_str.set(str(pixel_mm))
        self.color_min_str.set(str(color_min))
        self.color_max_str.set(str(color_max))
        self.blur_image_str.set(str(blur_img))
        self.blur_mask_str.set(str(blur_mask))
        self.min_point_size_str.set(str(size_point))
        self.min_point_space_str.set(str(space_point))
        self.var_frames_sec_str.set(str(frames_sec))

        input_var_label       = Label(self.window, textvariable=self.var_input_str, fg="red")
        output_var_label      = Label(self.window, textvariable=self.var_output_str, fg="red")
        pix_mm_var_label      = Label(self.window, textvariable=self.var_pix_mm_str, fg="red")
        col_min_var_label     = Label(self.window, textvariable=self.color_min_str, fg="red")
        col_max_var_label     = Label(self.window, textvariable=self.color_max_str, fg="red")
        blur_img_var_label    = Label(self.window, textvariable=self.blur_image_str, fg="red")
        blur_mask_var_label   = Label(self.window, textvariable=self.blur_mask_str, fg="red")
        point_size_var_label  = Label(self.window, textvariable=self.min_point_size_str, fg="red")
        point_space_var_label = Label(self.window, textvariab=self.min_point_space_str, fg="red")
        frames_sec_var_label = Label(self.window, textvariab=self.var_frames_sec_str, fg="red")

        input_var_label.place(x=220,y=10)
        output_var_label.place(x=220,y=35)
        pix_mm_var_label.place(x=220,y=60)
        col_min_var_label.place(x=220,y=85)
        col_max_var_label.place(x=220,y=110)
        blur_img_var_label.place(x=220,y=135)
        blur_mask_var_label.place(x=220,y=160)
        point_size_var_label.place(x=220,y=185)
        point_space_var_label.place(x=220,y=210)
        frames_sec_var_label.place(x=220,y=235)

    def add_static_label(self):
        input_static_label       = Label(self.window, text="Input plot")
        output_static_label      = Label(self.window, text="Output directory")
        pix_mm_static_label      = Label(self.window, text="Pixelsize (mm)")
        col_min_static_label     = Label(self.window, text="Lower limit color")
        col_max_static_label     = Label(self.window, text="Upper limit color")
        blur_img_static_label    = Label(self.window, text="Blur matrix image")
        blur_mask_static_label   = Label(self.window, text="Blur matrix mask")
        point_size_static_label  = Label(self.window, text="Minumum Size points")
        point_space_static_label = Label(self.window, text="Minimum Space points")
        frames_per_second_label  = Label(self.window, text="Frames per second")
        inputfile_label = Label(self.window, text="Import plot from")
        outputdir_label = Label(self.window, text="export files to")
        fps_label = Label(self.window, text="Frames per second")

        input_static_label.place(x=20, y=10)
        output_static_label.place(x=20, y=35)
        pix_mm_static_label.place(x=20, y=60)
        col_min_static_label.place(x=20, y=85)
        col_max_static_label.place(x=20, y=110)
        blur_img_static_label.place(x=20, y=135)
        blur_mask_static_label.place(x=20, y=160)
        point_size_static_label.place(x=20, y=185)
        point_space_static_label.place(x=20, y=210)
        frames_per_second_label.place(x=20, y=235)

        inputfile_label.place(x=20,y= 305)
        outputdir_label.place(x=20,y= 335)
        fps_label.place(x=20, y=365)

    def add_Optionmenu(self):
        global filename
        global outputmap
        global frames_sec

        self.file_var = StringVar()
        self.dir_var = StringVar()
        self.fps_var = StringVar()

        self.file_var.set(filename)
        self.dir_var.set(outputmap)
        self.fps_var.set(frames_sec)

        file_option_menu = OptionMenu(self.window,self.file_var,"Camera","File")
        dir_option_menu = OptionMenu(self.window, self.dir_var, "Directory")
        fps_option_menu = OptionMenu(self.window, self.fps_var, "10","15","30","50","60","120","240","480","Custom")

        file_option_menu.place(x=220,y=305)
        dir_option_menu.place(x=220, y=335)
        fps_option_menu.place(x=220, y=365)

        self.file_var.trace('w',self.change_file_var)
        self.dir_var.trace('w', self.change_dir_var)
        self.fps_var.trace('w', self.change_fps_var)

    def change_fps_var(self,*args):
        global frames_sec
        frames_sec = self.fps_var.get()

        if frames_sec == "Custom":
            frames_sec = tkSimpleDialog.askfloat("Frames per second","Frames per second")
            self.var_frames_sec_str.set(str(round(frames_sec,3)))
        else:
            frames_sec = int(frames_sec)
            self.var_frames_sec_str.set(str(frames_sec))
        self.window.update_idletasks()

    def update_var_label(self):
        self.var_input_str.set(str(filename.split('/')[-1]))
        self.var_output_str.set(str(outputmap.split('/')[-1]))
        self.var_pix_mm_str.set(str(round(pixel_mm,3)))
        self.color_min_str.set(str(color_min))
        self.color_max_str.set(str(color_max))
        self.blur_image_str.set(str(blur_img))
        self.blur_mask_str.set(str(blur_mask))
        self.min_point_size_str.set(str(size_point))
        self.min_point_space_str.set(str(space_point))
        self.var_frames_sec_str.set(str(round(frames_sec,3)))
        self.window.update_idletasks()

    def change_file_var(self,*args):
        global filename
        filename = self.file_var.get()

        if filename == "File":
            filename = tkFileDialog.askopenfilename()
            self.var_input_str.set(filename.split('/')[-1])
            if filename == "":
                self.file_var.set(None)
                filename = None
                self.var_input_str.set(None)
        else:
            self.var_input_str.set(str(filename))
        self.window.update_idletasks()

    def change_dir_var(self,*args):
        global outputmap

        outputmap = self.dir_var.get()
        outputmap = tkFileDialog.askdirectory()
        self.var_output_str.set(outputmap.split('/')[-1])
        if outputmap == "":
            self.dir_var.set(None)
            outputmap = None
            self.var_output_str.set(str(outputmap))

        self.window.update_idletasks()

    def loop(self):
        self.window.mainloop()

def main():
     gui = window()
     gui.add_button()
     gui.add_var_labels()
     gui.add_Optionmenu()
     gui.add_static_label()
     gui.loop()

if __name__ == '__main__':
    main()