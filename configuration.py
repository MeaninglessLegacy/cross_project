############################################################################
############################################################################

#IMPORTS

import os

import pyglet

############################################################################
############################################################################

#FILE SETTINGS



filepath = os.path.dirname(__file__)



############################################################################
############################################################################

#WINDOW CONFIGURATION



window_width = 1280
window_height = 720



############################################################################
############################################################################

#PYGAME CONFIGURATION

mixerFrequency = 44100
mixerSize = -16
mixerChannels = 2


############################################################################
############################################################################

#PYGLET CONFIGURATION



############################################################################
############################################################################

#GAME CONFIGURATION

gameFps = 60



############################################################################
############################################################################

#CONTROLS

controls = {
    "player_1" : {
        "left" : pyglet.window.key.A,
        "right" : pyglet.window.key.D,
        "up" : pyglet.window.key.W,
        "down" : pyglet.window.key.S,
        "changeChr" : pyglet.window.key.Q,
        "ability1" : pyglet.window.key.J,
        "ability2" : pyglet.window.key.K,
        "ability3" : pyglet.window.key.L,
        "ability4" : pyglet.window.key.U,
    },
    "player_2" : {
        "left" : pyglet.window.key.LEFT,
        "right" : pyglet.window.key.RIGHT,
        "up" : pyglet.window.key.UP,
        "down" : pyglet.window.key.DOWN,
        "changeChr" : pyglet.window.key.NUM_7,
        "ability1" : pyglet.window.key.NUM_0,
        "ability2" : pyglet.window.key.NUM_1,
        "ability3" : pyglet.window.key.NUM_2,
        "ability4" : pyglet.window.key.NUM_3,
    }
}



############################################################################
############################################################################

#GAME CLASSES

class player_class():
    def __init__(self, name, color):
        self.player = name
        self.color = color
        self.control_type = "keyboard"
        self.sC = None

        self.ability_cd = {
            '1' : 0,
            '2' : 0,
            '3' : 0,
            '4' : 0,
            'chr_swap' : 0,
        }

        self.abilities_held = {
            '1' : False,
            '2' : False,
            '3' : False,
            '4' : False,
        }

        self.abilities_held_timers = {
            '1' : 0,
            '2' : 0,
            '3' : 0,
            '4' : 0
        }