import sys, os
import tkinter

from PIL import Image, ImageTk

import time

root = tkinter.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()
canvas = tkinter.Canvas(root,width=w,height=h)
canvas.pack()
canvas.configure(background='black')

def showPIL(pilImage):
    imgWidth, imgHeight = pilImage.size
 # resize photo to full screen 
    ratio = min(w/imgWidth, h/imgHeight)
    imgWidth = int(imgWidth*ratio)
    imgHeight = int(imgHeight*ratio)
    pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)   
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.update_idletasks()
    root.update()
#    root.bind("", lambda e: (e.widget.withdraw(), e.widget.quit()))

dir="/home/eramox/Temp/trash/test_kiosk"

names = os.listdir(dir)

print(names)

for file in names:
    print(file)
    if file[-4:] == ".jpg":
        file=Image.open(dir+file)
        showPIL(file)
        time.sleep(5)
