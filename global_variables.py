########################################################################################################################
########################################################################################################################


# GLOBAL VARIABLES FILE


########################################################################################################################
########################################################################################################################


import os
import pyglet


########################################################################################################################
########################################################################################################################


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


########################################################################################################################
########################################################################################################################


# KEYBOARD AND MOUSE
# mouse_pos: the x,y coordinate pair of the mouse's position on the window
# event: a string value that is set whenever an event has been triggered in the window such as a mouse click
# keys_pressed: a dictionary made of key values of key codes from pyglet and boolean values representing if they have
# been pressed down or not

mouse_pos = (0, 0)

event = "NONE"

keys_pressed = {
    pyglet.window.key.A: False,
    pyglet.window.key.D: False,
    pyglet.window.key.W: False,
    pyglet.window.key.S: False,
    pyglet.window.key.Q: False,
    pyglet.window.key.J: False,
    pyglet.window.key.K: False,
    pyglet.window.key.L: False,
    pyglet.window.key.U: False,
    pyglet.window.key.LEFT: False,
    pyglet.window.key.RIGHT: False,
    pyglet.window.key.UP: False,
    pyglet.window.key.DOWN: False,
    pyglet.window.key.NUM_7: False,
    pyglet.window.key.NUM_0: False,
    pyglet.window.key.NUM_1: False,
    pyglet.window.key.NUM_2: False,
    pyglet.window.key.NUM_3: False
}


########################################################################################################################
########################################################################################################################


# PYGLET RENDERING VARIABLES
# batched_items: a dictionary of all items that are currently being batched by pyglet, deleting items from this
# dictionary should also delete them from the batch they exist in
# world_batch: a pyglet batch object that is used for rendering objects in the world space

batched_items = {}

world_batch = pyglet.graphics.Batch()


########################################################################################################################
########################################################################################################################


# WORLD SPACE VARIABLES
# camera_object: a Camera object that includes the camera's position and rotation
# world_tiles: an array of Tile objects that represent the map in world space

camera_object = None

world_tiles = None


########################################################################################################################
########################################################################################################################

# CACHES

# a list of the players in the game
players = {}

# a list of all the current characters in the game
character_list = {}
