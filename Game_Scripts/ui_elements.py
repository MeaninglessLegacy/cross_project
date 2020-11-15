############################################################################
############################################################################

#Ui elements

import pygame, math, Game_Scripts.ui_assets, Game_Scripts.functions, pyglet

from pygame import font

ui_assets = Game_Scripts.ui_assets
functions = Game_Scripts.functions

'''
    this script is basically what you call when you want to draw various ui_elements except the combat_ui because that boi is a special boi in it's self
    so basically the work flow of this script is as follows:

    create ui_class --> draw(ui_class) <-- provide the class and screen ---> will return you the element drawn onto the screen
'''

############################################################################
############################################################################

#Ui_classes
class text_button():

    def __init__(self, name, self_width, self_height, x_position, y_position, text, text_size, text_color, font, background_color, border_color, border_width):

        self.name = name

        self.height = self_height
        self.width = self_width
        self.x_position = x_position
        self.y_position = y_position

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

    def __init__(self, name, self_width, self_height, x_position, y_position, image, image_alpha):

        self.name = name

        self.height = self_height
        self.width = self_width
        self.x_position = x_position
        self.y_position = y_position

        self.image = image
        self.image_alpha = image_alpha

############################################################################
############################################################################

#Ui_functions
'''
    okay so this boi is kind of special too, i'll add functions such as ui_move or tween which will be able to animate ui elements along with the draw(ui_class) funciton as well
'''

#draw the elements
def draw_ui_element(ui_element, screen, w, h):

    screen_width = w
    screen_height = h

    #draw the ui element onto the screen
    if isinstance(ui_element, text_button):
        #set the variables
        x_pos = math.floor(ui_element.x_position * screen_width)
        y_pos = math.floor(ui_element.y_position * screen_height)
        x_size = math.floor(ui_element.width * screen_width)
        y_size = math.floor(ui_element.height * screen_height)
        #make our rect object
        button = pyglet.shapes.Rectangle(x_pos, y_pos, x_size, y_size, color=(55, 55, 255), batch=screen)
        button.center = (x_pos, y_pos)
        #draw the rect that is the button
        if ui_element.background_color != None:
            button = pyglet.shapes.Rectangle(x_pos, y_pos, x_size, y_size, color=ui_element.background_color, batch=screen)
        #label the rect
        text = pyglet.text.Label(ui_element.text,
                          font_name='Times New Roman',
                          font_size=14,
                          x=x_pos, y=y_pos)
        #text.color = ui_element.text_color
        text.draw()
    #images
    if isinstance(ui_element, image):
        # set the variables
        x_pos = math.floor(ui_element.x_position * screen_width)
        y_pos = math.floor(ui_element.y_position * screen_height)
        x_size = math.floor(ui_element.width * screen_width)
        y_size = math.floor(ui_element.height * screen_height)
        img = functions.get_image(ui_element.image, True)
        texture = img.get_texture()
        texture.width = x_size
        texture.height = y_size
        #img = pygame.transform.scale(img, (x_size, y_size))
        #blit
        img.blit(x_pos, y_pos)


    #This determines if the mouse is over the element
def mouseHover(ui_element, screen, mouse_position, w, h):

    screen_width = w
    screen_height = h

    mouseX = mouse_position[0]
    mouseY = mouse_position[1]

    if isinstance(ui_element, text_button) or isinstance(ui_element, image_button):

        '''
                    ui.y + ui.height/2
                            |
        ui.x - ui.width/2 <-----------> ui.x + ui.width/2
                            |
                    ui.y - ui.height/2
        '''
        left_boundry = math.floor((screen_width*ui_element.x_position)-(ui_element.width*screen_width)/2)
        right_boundry = math.floor((screen_width*ui_element.x_position)+(ui_element.width*screen_width)/2)
        top_boundry = math.floor((screen_height*ui_element.y_position)+(ui_element.height*screen_height)/2)
        bottom_boundry = math.floor((screen_height*ui_element.y_position)-(ui_element.height*screen_height)/2)

        if left_boundry < mouseX < right_boundry and bottom_boundry < mouseY < top_boundry:
            ui_element.mouseOver = True
        else:
            ui_element.mouseOver = False