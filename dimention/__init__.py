import cv2
from Tkinter import *
from PIL import ImageTk, Image
import math
import tkMessageBox

points = [(0,0),(0,0)]
dimention = float(0.000)
mm_pix = float(0.000)
dim = 'free'

class get:
    def __init__(self,images):
        self.image = images
        self.root = Toplevel()
        self.root.title("get dimentions")

        self.frame = cv2.imread(self.image)
        self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
        self.img = ImageTk.PhotoImage(Image.fromarray(self.frame))

        self.root.geometry(str(self.img.width()+300) + "x" + str(self.img.height()))

    def return_pixels(self):
        global points
        global dim

        if dim == "x":
            return abs(points[0][0]-points[1][0])
        elif dim == "y":
            return abs(points[0][1] - points[1][1])
        else:
            x =  abs(points[0][0]-points[1][0])
            y =  abs(points[0][1] - points[1][1])
            return math.sqrt(math.pow(x,2)+math.pow(y,2))

    def return_mm_pix(selfs):
        global dimention

        pixel_lengte = selfs.return_pixels()

        if pixel_lengte != 0:
            return float(dimention/pixel_lengte)
        else:
            return 0


    def add_label(self):
        global dimention
        global dim
        global mm_pix

        self.var_pix = StringVar()
        self.var_dim = StringVar()
        self.var_ass = StringVar()
        self.var_mm_pix = StringVar()

        self.var_dim.set(str(round(dimention,3)))
        self.var_pix.set(str(round(self.return_pixels(),3)))
        self.var_mm_pix.set(str(round(self.return_mm_pix(),3)))
        self.var_ass.set(dim)

        pix_var_label = Label(self.root,textvariable = self.var_pix)
        pix_var_label.place(x=190,y=50)

        dim_var_label = Label(self.root,textvariable = self.var_dim)
        dim_var_label.place(x=190,y=80)

        mm_pix_var_label = Label(self.root, textvariable=self.var_mm_pix)
        mm_pix_var_label.place(x=190, y=110)

        ass_var_label = Label(self.root, textvariable=self.var_ass)
        ass_var_label.place(x=190, y=140)

        pix_label = Label(self.root,text="Pixel Dimention",fg='LightSteelBlue4')
        pix_label.place(x=10,y=50)

        dim_label = Label(self.root, text="Entered dimention", fg='LightSteelBlue4')
        dim_label.place(x=10, y=80)

        mm_pix_label = Label(self.root, text="mm per pixel", fg='LightSteelBlue4')
        mm_pix_label.place(x=10, y=110)

        ass_label = Label(self.root, text="Measuring direction", fg='LightSteelBlue4')
        ass_label.place(x=10, y=140)

        data_label = Label(self.root, text="Data", font=("Helvetica", 16))
        data_label.place(x=30, y=20)

        data_label = Label(self.root, text="Set", font=("Helvetica", 16))
        data_label.place(x=30, y=180)

        ass_set_label = Label(self.root, text="Measuring direction", fg='LightSteelBlue4')
        ass_set_label.place(x=10, y=210)

        dimention_set_label = Label(self.root, text="Dimention (mm)", fg='LightSteelBlue4')
        dimention_set_label.place(x=10, y=240)

    def add_entry(self):
        global dimention

        self.Dimention_entry = Entry(self.root,width=8)
        self.Dimention_entry.insert(0,str(dimention))

        self.Dimention_entry.place(x=193, y=240)

    def add_optionmenu(self):
        global dim

        self.ass_set_var = StringVar()
        self.ass_set_var.set(dim)

        ass_set_optionmenu = OptionMenu(self.root,self.ass_set_var,'x','y','free')
        ass_set_optionmenu.place(x=190, y=210)

    def add_button(self):
        save_button = Button(self.root,text="Save",command=self.save)
        save_button.place(x=10 ,y=280)

    def label_update(self):
        global dim
        global dimention

        dim = self.ass_set_var.get()
        dimention = float(self.Dimention_entry.get())

        self.var_dim.set(str(round(dimention,3)))
        self.var_pix.set(str(round(self.return_pixels(),3)))
        self.var_mm_pix.set(str(round(self.return_mm_pix(),3)))
        self.var_ass.set(dim)

        self.root.update_idletasks()

    def add_image(self):
        self.panel = Label(self.root, image=self.img)
        self.panel.place(x=300,y=0)

    def loop(self):
        self.root.mainloop()

        return self.return_mm_pix()

    def mouse_event(self):
        self.panel.bind("<Button-1>",self.set_point)
        self.root.bind("<Button-1>", self.update_all)

    def set_point(self,event):
        global points
        points[1] = points[0]
        points[0] = (event.x,event.y)
        self.update_image()
        self.label_update()

    def update_image(self):
        global points
        global dim

        frame_copy = self.frame.copy()

        if dim == "x":
            cv2.line(frame_copy,(points[0][0],0),(points[0][0],self.img.height()),(255,0,0),1)
            cv2.line(frame_copy,(points[1][0],0),(points[1][0],self.img.height()),(255,0,0),1)

        elif dim == "y":
            cv2.line(frame_copy,(0,points[0][1]),(self.img.width(),points[0][1]),(255,0,0),1)
            cv2.line(frame_copy,(0,points[1][1]),(self.img.width(),points[1][1]),(255,0,0),1)

        else:
            cv2.line(frame_copy,points[0], points[1], (255, 0, 0), 2)

        img = ImageTk.PhotoImage(Image.fromarray(frame_copy))
        self.panel.config(image = img)
        self.panel.image = img

    def update_all(self,event):
        self.label_update()
        self.update_image()

    def save(self):
        global points
        global dimention
        global mm_pix

        mm_pix = self.return_mm_pix()

        if mm_pix != 0.0:
            self.root.quit()
            self.root.destroy()
            mm_pix = self.return_mm_pix()
        else:
            tkMessageBox.showerror("error","Not all values of the parameters are known")


def main(filename):
    global mm_pix

    get_dimention = get(filename)
    get_dimention.add_label()
    get_dimention.add_image()
    get_dimention.add_entry()
    get_dimention.add_button()
    get_dimention.add_optionmenu()
    get_dimention.mouse_event()

    return get_dimention.loop()



if __name__ == '__main__':
    main('/Users/jellevissers/Desktop/minor/3.mp4image.jpg')