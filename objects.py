from PIL import Image, ImageDraw, ImageOps, ImageEnhance, ImageFont, ImageFilter
from abc import ABC, abstractmethod
def clean(input):
    output = []
    for i in input:
        output.append(int(i))
    return tuple(output)

def center_of(obj, corner_loc):
    center = (corner_loc[0] + int(obj.size[0] / 2), corner_loc[1] + int(obj.size[1] / 2))
    return (int(center[0]), int(center[1]))
def corner_of(obj, center_loc):
    corner = (center_loc[0] - int(obj.size[0] / 2), center_loc[1] - int(obj.size[1] / 2))
    return (int(corner[0]), int(corner[1]))

class object(ABC):
    @abstractmethod
    def get_default(self):
        pass
    
    @abstractmethod
    def draw_base(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

    def add_effects(self, img):
        image = img
        for i in self.effects_array:
            image = i.draw_effect(image)
        return image
    def set_effects(self, effects):
        self.effects_array = effects


    def draw_image(self):
        img = self.draw_base()
        img = self.add_effects(img)
        return img
class effect(ABC):
    @abstractmethod
    def draw_effect(self):
        pass
    @abstractmethod
    def get_default():
        pass
    @abstractmethod
    def get_type(self):
        pass
    @abstractmethod
    def get_args(self):
        pass
    def set_effects(self, effects):
        self.effects_array = effects






class baseImage(object):
    def get_default():
        details = {}
        details["size"] = (1080, 720)
        details["color"] = (255, 255, 255, 255)
        return details

    def __init__(self, dict) -> None:
        self.size = clean(dict["size"])
        self.color = clean(dict["color"])
        print(self.color)
        self.effects_array = []
        pass
    def draw_base(self):
        img = Image.new("RGBA", self.size, self.color)
        return img
    def get_type(self):
        return "Base Image"
    def get_args(self):
        details = {}
        details["size"] = self.size
        details["color"] = self.color
        true_details = {
            "details":details,
            "effects": self.effects_array
        }
        return true_details
    
class external_png(object):
    def alter_value(self, value):
        self.file = value
    def get_default():
        details = {}
        details["location"] = (480, 640)
        details["file"] = ("file_input_flag", "example.txt")
        return details
    def __init__(self, dict) -> None:
        self.dst = clean(dict["location"])
        self.file = dict["file"][0]
        self.effects_array = []
        pass
    def draw_base(self):
        img = Image.open(self.file)
        return img
    def get_type(self):
        return "External Image"
    def get_args(self):
        details = {}
        details["location"] = self.dst
        details["file"] = ("file_input_flag", self.file)
        true_details = {
            "details":details,
            "effects": self.effects_array
        }
        return true_details

class rectangle(object):
    def get_default():
        details = {}
        details["size"] = (640, 640)
        details["color"] = (255, 255, 255, 255)
        details["location"] = (640, 480)
        return details
    def __init__(self, dict) -> None:
        self.dst = clean(dict["location"])
        self.size = clean(dict["size"])
        self.color = clean(dict["color"])
        self.effects_array = []
        pass
    def draw_base(self):
        img = Image.new("RGBA", self.size,self.color)
        return img
    def get_type(self):
        return "Rectangle"
    def get_args(self):
        details = {}
        details["size"] = self.size
        details["color"] = self.color
        details["location"] = self.dst
        true_details = {
            "details":details,
            "effects": self.effects_array
        }
        return true_details

class text(object):
    def alter_value(self, value):
        self.text = value
    def get_default():
        details = {}
        details["text"] = ("",)
        details["font"] = ("file_input_flag", "example.txt")
        details["font size"] = (100,)
        details["color"] = (255, 255, 255, 255)
        details["location"] = (640, 480)
        return details
    def __init__(self, dict) -> None:
        self.text = dict["text"][0]
        self.font = dict["font"][0]
        self.dst = clean(dict["location"])
        self.font_size = int(dict["font size"][0])
        self.color = clean(dict["color"])
        self.effects_array = []
        pass
    def draw_base(self):
        
        
        type_font = ImageFont.truetype(self.font, self.font_size)
        temper = Image.new("RGBA", (2000, 2000))
        temperer = ImageDraw.Draw(temper)
        max_size = temperer.textsize(self.text, type_font)
        image = Image.new("RGBA", max_size)
        
        draw = ImageDraw.Draw(image)
        draw.text(center_of(image, (0,0)), self.text, font=type_font, anchor="mm", fill=self.color)
        return image
    def get_type(self):
        return "Text"
    def get_args(self):
        details = {}
        details["text"] = (self.text,)
        details["font"] = ("file_input_flag", self.font)
        details["font size"] = (self.font_size,)
        details["color"] = self.color
        details["location"] = self.dst
        true_details = {
            "details":details,
            "effects": self.effects_array
        }
        return true_details


























class resize_effect(effect):
    def get_default():
        details = {}
        details["size"] = (480, 640)
        return details
    def get_type(self):
        return "Resize"
    
    def draw_effect(self, img):
        image = img.resize(clean(self.size))
        return image
    def __init__(self, dict) -> None:
        self.size = clean(dict["size"])
    def get_args(self):
        details = {}
        details["size"] = self.size
        true_details = {
            "details":details,
            "effects": []
        }
        return true_details
    
class rotate_effect(effect):
    def get_default():
        details = {}
        details["angle"] = (0,)
        return details
    def get_type(self):
        return "Rotate"
    
    def draw_effect(self, img):
        
        image = img.resize((img.size[0] * 4, img.size[1] * 4))
        image = image.rotate(int(self.angle[0]), expand=True)
        image = image.resize((round(image.size[0] / 4) , round(image.size[1] / 4)))
        return image
    def __init__(self, dict) -> None:
        self.angle = dict["angle"]
    def get_args(self):
        details = {}
        details["angle"] = self.angle
        true_details = {
            "details":details,
            "effects": []
        }
        return true_details
    
class border_effect(effect):
    def get_default():
        details = {}
        details["color"] = (255, 255, 255, 255)
        details["size"] = (5,)
        return details
    def get_type(self):
        return "Border"
    
    def draw_effect(self, img):
        color = self.color
        size = self.size
        strength = self.strength
        border = img
        
        border = ImageOps.expand(border, size * 4)
        border = border.convert("L")
        filter_func = lambda x: 0 if x < 1 else 255
        border = border.point(filter_func)
        
        
        border = border.filter(ImageFilter.GaussianBlur(size))
        
        filter_func2 = lambda x: min(x * strength, 255)
        border = border.point(filter_func2)
        border = border.convert("L")
        
        
        box = Image.new("RGBA", border.size,color)
        box.putalpha(border)
        blank = Image.new("RGBA", box.size)
        blank.paste(img, (size * 4,size * 4))
        box.alpha_composite(blank)
        blank = Image.new("RGBA", box.size)
        blank.alpha_composite(box)
        img = blank
        return img
    def __init__(self, dict) -> None:
        self.size = int(dict["size"][0])
        self.color = clean(dict["color"])
        self.strength = 255
    def get_args(self):
        details = {}
        details["size"] = (self.size,)
        details["color"] = self.color
        true_details = {
            "details":details,
            "effects": []
        }
        return true_details
    
class aura_effect(effect):
    def get_default():
        details = {}
        details["color"] = (255, 255, 255, 255)
        details["size"] = (10,)
        details["strength"] = (2.2,)
        return details
    def get_type(self):
        return "Aura"
    
    def draw_effect(self, img):
        color = self.color
        size = self.size
        strength = self.strength
        border = img
        
        border = ImageOps.expand(border, size * 4)
        border = border.convert("L")
        filter_func = lambda x: 0 if x < 1 else 255
        border = border.point(filter_func)
        
        
        border = border.filter(ImageFilter.GaussianBlur(size))
        
        filter_func2 = lambda x: min(x * strength, 255)
        border = border.point(filter_func2)
        border = border.convert("L")
        
        
        box = Image.new("RGBA", border.size,color)
        box.putalpha(border)
        blank = Image.new("RGBA", box.size)
        blank.paste(img, (size * 4,size * 4))
        box.alpha_composite(blank)
        blank = Image.new("RGBA", box.size)
        blank.alpha_composite(box)
        img = blank
        return img
    def __init__(self, dict) -> None:
        self.size = int(dict["size"][0])
        self.color = clean(dict["color"])
        self.strength = float(dict["strength"][0])
    def get_args(self):
        details = {}
        details["size"] = (self.size,)
        details["color"] = self.color
        details["strength"] = (self.strength,)
        true_details = {
            "details":details,
            "effects": []
        }
        return true_details
    
class color_gradient(effect):
    def get_default():
        details = {}
        details["size"] = (480, 640)
        details["location"] = (0,0)
        details["angle"] = (0,)
        details["color 1"] = (255, 255, 255, 255)
        details["color 2"] = (255, 255, 255, 255)
        return details
    def get_type(self):
        return "Color Gradient"
    def draw_effect(self, img):
        gradient = Image.new("RGBA", self.size)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                color= [0,0,0,0]
                factor = y / self.size[1]
                for i in range(len(color)):
                    color[i] = int(self.color_1[i] * factor + self.color_2[i] * (1 - factor))     
                gradient.putpixel((x, y), (color[0],color[1],color[2],color[3]))
                
        gradient = gradient.rotate(self.angle, expand=True)
        image_true = img
        image_bordered = Image.new("RGBA", img.size)
        image_bordered.paste(image_true, (0,0))

        image_bordered.paste(gradient, corner_of(gradient, self.location))
        print(type(image_bordered))
        for x in range(image_true.size[0]):
            for y in range(image_true.size[1]):
                coord = (x,y)
                if (image_true.getpixel(coord) != (0,0,0,0)):
                    image_true.putpixel(coord, image_bordered.getpixel(coord) )


        return image_true
    def __init__(self, dict) -> None:
        self.size = clean(dict["size"])
        self.location = clean(dict["location"])
        self.angle = int(dict["angle"][0])
        self.color_1 = clean(dict["color 1"])
        self.color_2 = clean(dict["color 2"])
    def get_args(self):
        details = {}
        details["size"] = self.size
        details["location"] = self.location
        details["angle"] = (self.angle,)
        details["color 1"] = self.color_1
        details["color 2"] = self.color_2
        true_details = {
            "details":details,
            "effects": []
        }
        return true_details
    
class opacity_gradient(effect):
    def get_default():
        details = {}
        details["size"] = (480, 640)
        details["location"] = (0,0)
        details["angle"] = (0,)
        details["opacity 1"] = (255,)
        details["opacity 2"] = (255,)
        return details
    def get_type(self):
        return "Opacity Gradient"
    def draw_effect(self, img):
        gradient = Image.new("L", self.size)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                color= [0]
                factor = y / self.size[1]
                for i in range(len(color)):
                    color[i] = int(self.color_1[0] * factor + self.color_2[0] * (1 - factor))     
                gradient.putpixel((x, y), (color[0]))
        gradient = gradient.rotate(self.angle, expand=True)
        image_true = img
        image_bordered = Image.new("L", img.size,color=255)

        image_bordered.paste(gradient, corner_of(gradient, self.location))
        for x in range(image_true.size[0]):
            for y in range(image_true.size[1]):
                coord = (x,y)
                if (image_true.getpixel(coord)[3] == (0)):
                    image_bordered.putpixel(coord, (0,) )
                
        image_true.putalpha(image_bordered)

        return image_true
    def __init__(self, dict) -> None:
        self.size = clean(dict["size"])
        self.location = clean(dict["location"])
        self.angle = int(dict["angle"][0])
        self.color_1 = clean(dict["opacity 1"])
        self.color_2 = clean(dict["opacity 2"])
    def get_args(self):
        details = {}
        details["size"] = self.size
        details["location"] = self.location
        details["angle"] = (self.angle,)
        details["opacity 1"] = self.color_1
        details["opacity 2"] = self.color_2
        true_details = {
            "details":details,
            "effects": []
        }
        return true_details

class fadeout_border_effect(effect):
    def get_default():
        details = {}
        details["size"] = (10,)
        details["strength"] = (4,)
        return details
    def get_type(self):
        return "Fade Edge"
    
    def draw_effect(self, img):
        size = self.size
        border = Image.new(size=img.size, mode="L")
        border.paste(img, (0,0))

        border = border.convert("L")


        filter_func = lambda x: 0 if x < 1 else 255
        border = border.point(filter_func)
        border = ImageOps.expand(border, size * 4, 0)
        border = border.filter(ImageFilter.GaussianBlur(size))
        filter_func_2 = lambda x: 0 if (255 - ((255 - x) * self.strength)) < 0 else (255 - ((255 - x) * self.strength))
        border = border.point(filter_func_2)
        border.show()
        border = border.convert("L")
        border = border.crop((size * 4, size * 4, size * 4 + img.size[0], size * 4 + img.size[1]))
        
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                coord = (x,y)
                if (img.getpixel(coord)[3] == (0)):
                    border.putpixel(coord, (0,) )
        print(border.size)
        print(img.size)
        img.putalpha(border)
        return img
    def __init__(self, dict) -> None:
        self.size = int(dict["size"][0])
        self.strength = float((dict["strength"][0]))
    def get_args(self):
        details = {}
        details["size"] = (self.size,)
        details["strength"] = (self.strength,)
        true_details = {
            "details":details,
            "effects": []
        }
        return true_details