############################################################################
############################################################################

# IMPORTS

import pyglet



############################################################################
############################################################################

# KEYBOARD AND MOUSE

mousePos = (0,0)

event = "NONE"

keysPressed = {
    pyglet.window.key.A : False,
    pyglet.window.key.D : False,
    pyglet.window.key.W : False,
    pyglet.window.key.S : False,
    pyglet.window.key.Q : False,
    pyglet.window.key.J : False,
    pyglet.window.key.K : False,
    pyglet.window.key.L : False,
    pyglet.window.key.U : False,
    pyglet.window.key.LEFT : False,
    pyglet.window.key.RIGHT : False,
    pyglet.window.key.UP : False,
    pyglet.window.key.DOWN : False,
    pyglet.window.key.NUM_7 : False,
    pyglet.window.key.NUM_0 : False,
    pyglet.window.key.NUM_1 : False,
    pyglet.window.key.NUM_2 : False,
    pyglet.window.key.NUM_3 : False
}



############################################################################
############################################################################

# PYGLET RENDERING VARIABLES

batchedItems = {}

uiBatch = pyglet.graphics.Batch()

worldBatch = pyglet.graphics.Batch()

backgroundBatch = pyglet.graphics.Batch()



############################################################################
############################################################################

# GAME VARIABLES

# the main camera object
cam = None

# tileSet are the tiles that are displayed
# borders are the borders of tileSet
tileSet = None
borders = None

# This is the current stage that is displayed
currentStage = None

teams = None


############################################################################
############################################################################

# UI VARIABLES

# which screen is currently displayed
screen = "title"

# which screen was last displayed
previousScreen = ""

# which screen to change the screen to
changeScreen = ""

# transition timers
loadTransition = 0
delay = 0



############################################################################
############################################################################

# CACHES AND DICTIONARIES

# a list of the players in the game
players = {}

# a list of all the current characters in the game
chrList = {}

# a list of the tiles on the field
tile_set = []

# animate objects
objToAnimate = []

# objects to update movement
objToManage = []

# ui_elements on screen
objOfUi = []

# ui_elements on the loading screen
loadScreenElements = []

# list of all ui elements to draw
drawList = []

# cached fonts and ui assets loaded
font_cache = {}

ui_cache = {}

# loaded sprite images
image_cache = {}

# a cache of loaded sounds
sound_cache = {}