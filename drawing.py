from PIL import Image
def corner_of(obj, center_loc):
    corner = (center_loc[0] - int(obj.size[0] / 2), center_loc[1] - int(obj.size[1] / 2))
    return (int(corner[0]), int(corner[1]))
def better_paste(base, new_layer, location):
    blank = Image.new("RGBA", base.size)
    blank.paste(new_layer, corner_of(new_layer, location))
    base.alpha_composite(blank)
    return base

def draw_image(objects):
    image = None
    for i in range(len(objects)):
        if image is not None:
            new_image = objects[i].draw_image()
            image = better_paste(image, new_image, objects[i].dst)
        else:
            image = objects[i].draw_image()
    return image


