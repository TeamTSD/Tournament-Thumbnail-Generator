import tkinter as tk
from PIL import Image, ImageDraw, ImageOps, ImageEnhance, ImageFont, ImageFilter
import objects
import item_creator
import drawing
import pickle
from tkinter import filedialog as fd
import pandas as pd

class object_holder:
    def __init__(self, root, object=None, index=0) -> None:
        self.frame = tk.Frame(master=root,)
        self.object = object
        self.index = index
        self.add_wigits()
        pass
    def add_wigits(self):
        self.empty_object_frame = tk.Frame(master=self.frame)
        self.full_object_frame = tk.Frame(master=self.frame)

def save_data():
    global object_list
    fp = fd.asksaveasfilename(title="Save layout file", initialfile="layout_data")
    
    file = open(file=fp,mode="wb")
    pickle.dump(object_list, file)
    pass
def load_data():
    global object_list
    global root
    fp = fd.askopenfile("rb", title="Select Layout File")
    object_list = pickle.load(fp)
    draw_edit_choice(root, object_list)
    pass
def delete_button_pressed(i):
    global root
    global object_list
    object_list.pop(i)
    print(object_list)
    draw_edit_choice(root, object_list)
def edit_button_pressed(object, index):
    print((object, index))
    generator = item_creator.object_generator(object.get_type(), insert_object, object.get_args(), index, master)

def draw_edit_choice(root, objects):
    global lastFrame
    if lastFrame is not None:
        lastFrame.destroy()
    object_item_frame = tk.Frame(master=root)
    for i in range(len(objects)):
        this_object = objects[i]
        descriptor = this_object.get_type()
        name_label = (tk.Label(master=object_item_frame, text=(str(i+1) + ". " + descriptor), anchor="w").grid(row=i, column=0))
        edit_button = (tk.Button(master=object_item_frame, text="Edit", command=lambda this_object=this_object, i=i:edit_button_pressed(this_object, i)).grid(row = i, column=1))
        delete_button = (tk.Button(master=object_item_frame, text="Delete", command=lambda i=i:delete_button_pressed(i)).grid(row = i, column=2))
    object_item_frame.grid(row=1, column=0, columnspan=3, sticky="W")
    lastFrame = object_item_frame
    

def insert_object(object, dst):
    global object_list
    global root
    if (dst == -1):
        object_list.append(object)
    else:
        object_list[dst] = object
    draw_edit_choice(root, object_list)

def summon_generator():
    text = object_to_create.get()
    generator = item_creator.object_generator(text, insert_object, master=master)


def draw_object(objects, batch=False):
    image = drawing.draw_image(objects)
    if (batch == False):
        #fp = fd.asksaveasfilename(defaultextension=".png", title="Save As", initialfile="thumbnail.png")

        #image.save(fp)
        image.show()
    return image

def batch_draw(objects):
    f = fd.askopenfilename(title="Select the batch file")
    csv = pd.read_csv(f,header=None)
    number_of_items = len(csv.loc[1,:])
    number = len(csv.loc[:,1]) - 1
    directory_name = ""
    

    for i in range(number):
        for ii in range(number_of_items):
            object_ID = int(csv.iloc[0,ii])-1
            objects[object_ID].alter_value(csv.iloc[i+1,ii])
        image = draw_object(objects, True)
        if (directory_name == ""):
            directory_name = fd.askdirectory(title="Select the Folder to save images to")
        image.save(fp=directory_name + "/thumbnail" + str(i) +".png")
        

    






master = tk.Tk()
master.geometry("400x400")
root = tk.Frame(master=master).place(relwidth=1, relheight=1)
object_options = ["Base Image", "External Image", "Rectangle", "Text"]
object_to_create = tk.StringVar()
object_to_create.set(object_options[0])

styler = {
    "padx":5,
    "pady":5
}

lastFrame = None

add_new_item_frame = tk.Frame(master=root, **styler)
object_creator_label = tk.Label(master=root, text=" Create Object:")
object_creator_label.grid(row=0, column=0)
object_creator_dropdown = tk.OptionMenu(root, object_to_create, *object_options)
object_creator_dropdown.grid(row=0, column=1, **styler)
object_creator_button = tk.Button(master=root, text="Create", command=summon_generator)
object_creator_button.grid(row=0, column=2, **styler)
add_new_item_frame.grid(row=0, column=0)

object_list = []

draw_object_framer = tk.Frame(master=root, **styler)
draw_button = tk.Button(master=draw_object_framer, text="Generate Image", command=lambda:draw_object(object_list))
draw_button.pack(side=tk.LEFT)
batch_draw_button = tk.Button(master=draw_object_framer, text="Batch Draw", command=lambda:batch_draw(object_list))
batch_draw_button.pack(side=tk.LEFT)
draw_object_framer.grid(row=2, column=0, sticky="w")

save_layout = tk.Frame(master=root, **styler)
save_button = tk.Button(master=save_layout, text="Save Layout", command=save_data).pack(side=tk.LEFT)
load_button = tk.Button(master=save_layout, text="Load Layout", command=load_data).pack(side=tk.LEFT)
save_layout.grid(row=3, column=0, sticky="w")



master.mainloop()