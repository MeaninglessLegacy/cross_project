########################################################################################################################
########################################################################################################################


# CONFIGURATION FILE


########################################################################################################################
########################################################################################################################


import pyglet


########################################################################################################################
########################################################################################################################


# DEFINITIONS


class PlayerClass:
    """
    the basic player class contains a reference to the character the player is controlling, the control scheme and what
    the player's color is.
    """
    def __init__(self,
                 name=None,
                 color=(0,0,0)):
        """
        Creates a new player object

        when creating a new player object the player's name needs to be given and the player's color.

        player: a string the name of the player, the name of the player is used to find what controls to use.
        color: a rgb value of the color of the player
        control_type: a string that defines the control method
        selected_character: a reference to the character object that the player is controlling
        ability_cd: integer cooldown values of the player's keypress
        abilities_held: boolean values of which ability keys are held down by the player
        abilities_held_timers: integer values of how long a player has been holding down a button

        :param name: string
            the name of the player as a string
        :param color: tuple
            rgb value of the player's color
        """
        self.player = name
        self.color = color
        self.control_type = "keyboard"
        self.selected_character = None

        self.ability_cd = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            'chr_swap': 0,
        }

        self.abilities_held = {
            '1': False,
            '2': False,
            '3': False,
            '4': False,
        }

        self.abilities_held_timers = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0
        }


########################################################################################################################
########################################################################################################################


# WINDOW CONFIGURATION
# the width and height of the window in pixels


window_width = 1280
window_height = 720


########################################################################################################################
########################################################################################################################


# GAME CONFIGURATION
# the maximum refresh rate of rendering


render_fps = 60


########################################################################################################################
########################################################################################################################


# CONTROLS
# keyboard controls, this can be changed to a class later


controls = {
    "player_1": {
        "left": pyglet.window.key.A,
        "right": pyglet.window.key.D,
        "up": pyglet.window.key.W,
        "down": pyglet.window.key.S,
        "changeChr": pyglet.window.key.Q,
        "ability1": pyglet.window.key.J,
        "ability2": pyglet.window.key.K,
        "ability3": pyglet.window.key.L,
        "ability4": pyglet.window.key.U,
    },
    "player_2": {
        "left": pyglet.window.key.LEFT,
        "right": pyglet.window.key.RIGHT,
        "up": pyglet.window.key.UP,
        "down": pyglet.window.key.DOWN,
        "changeChr": pyglet.window.key.NUM_7,
        "ability1": pyglet.window.key.NUM_0,
        "ability2": pyglet.window.key.NUM_1,
        "ability3": pyglet.window.key.NUM_2,
        "ability4": pyglet.window.key.NUM_3,
    }
}