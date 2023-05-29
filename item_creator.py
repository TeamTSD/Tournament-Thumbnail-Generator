import objects
import tkinter as tk
from tkinter import filedialog as fd
import os
import shutil

class option_menu:
    def file_choicer_pressed(self):
        f = fd.askopenfilename()
        base_name = os.path.basename(f)
        base_name = "uploads/"+base_name
        shutil.copy(f,base_name)
        self.textVars[0].set(base_name)
    def __init__(self, master, label_text, label_count) -> None:
        styler = {
            "padx":5,
            "pady":5
        }
        root = tk.Frame(master=master, **styler)
        
        self.label_text = label_text
        self.label = tk.Label(master=root, text=self.label_text, **styler).pack(side=tk.LEFT)
        self.textVars = []
        if label_count[0] == "file_input_flag":
            textVar = tk.StringVar(master=root)
            textVar.set(label_count[1])
            self.textVars.append(textVar)
            entry_object = tk.Button(master=root, text="Add File", width=5, command = self.file_choicer_pressed)
            entry_object.pack(side=tk.LEFT)
        else:
            for i in range(len(label_count)):
                textVar = tk.StringVar(master=root)
                textVar.set(label_count[i])
                entry_object = tk.Entry(master=root, textvariable=textVar, width=5)
                self.textVars.append(entry_object)
                entry_object.pack(side=tk.LEFT)
        root.pack(side=tk.TOP, anchor="w")
    def get_index(self):
        return self.label_text
    def get_input(self):
        output = []
        for i in self.textVars:
            output.append(i.get())
        return output

      
class object_generator:
    effect_or_object = {}
    
    object_classer = {}
    object_classer["Base Image"] = objects.baseImage
    object_classer["External Image"] = objects.external_png
    object_classer["Rectangle"] = objects.rectangle
    object_classer["Text"] = objects.text
    


    effect_classer = {}
    effect_options = []
    effect_classer["Resize"] = objects.resize_effect
    effect_classer["Rotate"] = objects.rotate_effect
    effect_classer["Border"] = objects.border_effect
    effect_classer["Aura"] = objects.aura_effect
    effect_classer["Color Gradient"] = objects.color_gradient
    effect_classer["Opacity Gradient"] = objects.opacity_gradient
    effect_classer["Fade Edge"] = objects.fadeout_border_effect

    item_classer = {}

    for i in object_classer:
        effect_or_object[i] = "object"
        item_classer[i] = object_classer[i]
    for i in effect_classer:
        effect_or_object[i] = "effect"
        effect_options.append(i)
        item_classer[i] = effect_classer[i]

    def delete_button_pressed(self, i):
        self.effect_list.pop(i)
        
        self.draw_edit_choice(self.root, self.effect_list)
    def edit_button_pressed(self, i):
        generator = object_generator(self.effect_list[i].get_type(), self.insert_effect, self.effect_list[i].get_args(), i, self.master)

    def draw_edit_choice(self, root, objects):
        if self.effect_framer is not None:
            self.effect_framer.destroy()
        
        object_item_frame = tk.Frame(master=root)
        for i in range(len(objects)):
            this_object = objects[i]
            descriptor = this_object.get_type()
            name_label = tk.Label(master=object_item_frame, text=(str(i+1) + ". " + descriptor), anchor="w").grid(row=i, column=0)
            edit_button = tk.Button(master=object_item_frame, text="Edit", command=lambda i=i:self.edit_button_pressed(i)).grid(row = i, column=1)
            delete_button = tk.Button(master=object_item_frame, text="Delete", command=lambda i=i:self.delete_button_pressed(i)).grid(row = i, column=2)
        object_item_frame.grid(row=2, column=0, columnspan=3, sticky="W")

        self.effect_framer = object_item_frame

    def insert_effect(self, object, index=-1):
        if (index == -1):
            self.effect_list.append(object)
        else:
            self.effect_list[index] = object
        self.draw_edit_choice(self.root, self.effect_list)

    def summon_generator(self):
        text = self.effect_to_create.get()
        generator = object_generator(text, self.insert_effect, master=self.master)

    def cancel(self):
        self.root.destroy()



    def create_button_pressed(self, dst):
        kwargs = {}
        for i in self.option_menus:
            kwargs[i.get_index()] = i.get_input()
        object = self.object_type(dict=kwargs)
        object.set_effects(self.effect_list)
        self.return_func(object, dst)
        self.root.destroy()
    
    def set_effect_choice(self, choice):
        self.effect_to_create.set(choice)
        self.object_creator_dropdown.set(choice)

    def __init__(self, type, return_func, input_args=None, output_location=-1, master=None) -> None:
        styler = {
            "padx":5,
            "pady":5
        }
        self.index_dst = output_location
        self.effect_list = []
        self.master = master
        self.root = tk.Frame(master=self.master)
        self.root.place(relwidth=1, relheight=1)
        self.root.tkraise()
        
        self.return_func = return_func
        self.effect_framer = None
        self.object_type = object_generator.item_classer[type]
        self.options = self.object_type.get_default()
        if input_args is not None:
            print(input_args)
            for i in input_args["details"]:
                self.options[i] = input_args["details"][i]
            self.effect_list = input_args["effects"]
        self.option_menus = []
        self.option_holder = tk.Frame(master=self.root)
        for i in self.options:
            new_option_menu = option_menu(self.option_holder, i, self.options[i])
            self.option_menus.append(new_option_menu)
        self.option_holder.grid(row=0,column=0, sticky="W")

        #I HOPE THIS WORKS
        self.add_new_item_frame = tk.Frame(master=self.root, **styler)
        self.effect_to_create = tk.StringVar(self.add_new_item_frame)
        self.effect_to_create.set(object_generator.effect_options[0])
        self.object_creator_label = tk.Label(master=self.add_new_item_frame, text=" Create Effect:")
        self.object_creator_label.grid(row=0, column=0)
        self.object_creator_dropdown = tk.OptionMenu(self.add_new_item_frame, self.effect_to_create, *object_generator.effect_options)
        self.object_creator_dropdown.grid(row=0, column=1, **styler)
        self.object_creator_button = tk.Button(master=self.add_new_item_frame, text="Create", command=self.summon_generator)
        self.object_creator_button.grid(row=0, column=2, **styler)
        if (object_generator.effect_or_object[type] == "object"):
            self.add_new_item_frame.grid(row=1, column=0, sticky="W")
        if (len(self.effect_list) > 0):
            self.draw_edit_choice(self.root, self.effect_list)
        #I HOPE THAT WORKED

        self.confirm_or_cancel = tk.Frame(master=self.root)
        confirm_button = tk.Button(master=self.confirm_or_cancel, text="Confirm", command=lambda:self.create_button_pressed(self.index_dst), **styler) 
        cancel_button = tk.Button(master=self.confirm_or_cancel, text="Back", command=self.cancel, **styler)
        confirm_button.grid(row=0, column=0, sticky="w")
        cancel_button.grid(row=0, column=1, sticky="w")
        self.confirm_or_cancel.grid(row=3, column=0, sticky="w")