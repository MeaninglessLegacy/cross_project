############################################################################
############################################################################

#Ui elements

import math,\
    Game_Scripts.ui_assets,\
    Game_Scripts.functions,\
    pyglet

ui_assets = Game_Scripts.ui_assets
functions = Game_Scripts.functions

'''
    this script is basically what you call when you want to draw various ui_elements except the combat_ui because that boi is a special boi in it's self
    so basically the work flow of this script is as follows:

    create ui_class --> draw(ui_class) <-- provide the class and thisBatch ---> will return you the element drawn onto the thisBatch
'''



############################################################################
############################################################################

#Ui_classes

class text_button():

    def __init__(self, name, self_width, self_height, x_position, y_position, z, text, text_size, text_color, font, background_color, border_color, border_width):

        self.name = name

        self.height = self_height
        self.width = self_width
        self.x_position = x_position
        self.y_position = y_position
        self.z = z

        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.font = font

        self.background_color = background_color
        self.border_width = border_width
        self.border_color = border_color

        self.click_function = None
        self.hover_function = None

        self.mouseOver = False

class image_button():

    def __init__(self, name, self_width, self_height, x_position, y_position, image, image_alpha, background_color, border_color, border_width):

        self.name = name

        self.height = self_height
        self.width = self_width
        self.x_position = x_position
        self.y_position = y_position

        self.image = image
        self.image_alpha = image_alpha

        self.background_color = background_color
        self.border_width = border_width
        self.border_color = border_color

        self.click_function = None
        self.hover_function = None

        self.mouseOver = False

class image():

    def __init__(self, name, self_width, self_height, x_position, y_position, z, image, image_alpha):

        self.name = name

        self.height = self_height
        self.width = self_width
        self.x_position = x_position
        self.y_position = y_position
        self.z = z

        self.image = image
        self.image_alpha = image_alpha



############################################################################
############################################################################

#Ui_functions

#draw the elements

def draw_ui_element(uiElement, thisBatch, batchedItems, w, h):

    screen_width = w
    screen_height = h

    #textbuttons
    if isinstance(uiElement, text_button):

        #set the variables
        x_pos = math.floor(uiElement.x_position * screen_width)
        y_pos = math.floor(uiElement.y_position * screen_height)
        x_size = math.floor(uiElement.width * screen_width)
        y_size = math.floor(uiElement.height * screen_height)
        z_button = pyglet.graphics.OrderedGroup(uiElement.z)
        z_text = pyglet.graphics.OrderedGroup(uiElement.z+1)
        #make our rect object
        button = pyglet.shapes.Rectangle(x_pos, y_pos, x_size, y_size, color=(55, 55, 255), batch=thisBatch, group=z_button)
        #draw the rect that is the button
        if uiElement.background_color != None:
            button.color =  uiElement.background_color
        #label the rect
        text = pyglet.text.Label(uiElement.text,
                                 font_name='Times New Roman',
                                 font_size=14,
                                 x=x_pos,y=y_pos,
                                 batch=thisBatch,
                                 group=z_text)
        #add the ui elements to the list of all batched items
        batchedItems[len(batchedItems)+1]=button
        batchedItems[len(batchedItems)+1]=text

    #images
    if isinstance(uiElement, image):

        # calculate the variables
        img = functions.get_image(uiElement.image, True)
        x_pos = math.floor(uiElement.x_position * screen_width)
        y_pos = math.floor(uiElement.y_position * screen_height)
        x_scale = (uiElement.width*screen_width)/img.width
        y_scale = (uiElement.height*screen_height)/img.height
        #create the pyglet sprite image
        z_image = pyglet.graphics.OrderedGroup(uiElement.z)
        imgSpr = pyglet.sprite.Sprite(img, x_pos, y_pos, batch=thisBatch, group=z_image)
        imgSpr.update(scale_x=x_scale, scale_y=y_scale)
        #draw the image, this is stupid and slow but it works
        batchedItems[len(batchedItems)+1] = imgSpr


############################################################################
############################################################################

#This determines if the mouse is over the element

def mouse_hover(uiElement, mouse_position, w, h):

    screen_width = w
    screen_height = h

    mouseX = mouse_position[0]
    mouseY = mouse_position[1]

    if isinstance(uiElement, text_button) or isinstance(uiElement, image_button):

        '''
                 ui.y + ui.height
                /|\
                 |
        ui.x <------->ui.x + ui.width
                 |
                \|/
                 ui.y
        '''

        left_boundry = math.floor(screen_width*uiElement.x_position)
        right_boundry = math.floor(screen_width*uiElement.x_position+uiElement.width*screen_width)
        top_boundry = math.floor(screen_height*uiElement.y_position+uiElement.height*screen_height)
        bottom_boundry = math.floor(screen_height*uiElement.y_position)

        if left_boundry < mouseX < right_boundry and bottom_boundry < mouseY < top_boundry:
            uiElement.mouseOver = True
        else:
            uiElement.mouseOver = False