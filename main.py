########################################################################################################################
########################################################################################################################


# MAIN FILE


########################################################################################################################
########################################################################################################################


# OUTLINE

# Gameplay:
# 1.Create character classes
# 2.Create sprite classes
# 3.Create player classes
# 4.Add player controls
# 5.Add character skills
# 6.Add screens to game
# 7.Add ability to move between screens
# 8.Create map loading
# 9.Add execution of controls
# 10.Add animations
# 11.Add game win conditions

# Rendering:
# 1.Open a opengl context window
# 2.Create a world space and a camera to view the game through
# 3.Render the game through the camera on specific screens

# Startup:
# 1.Load a configuration file
# 2.Load all of the imports
# 3.Create all of the player objects
# 4.Create all the character objects


########################################################################################################################
########################################################################################################################


import pyglet

import global_variables
import configuration
import imports


########################################################################################################################
########################################################################################################################


# INITIALIZE CACHES


# add player objects to the player list
global_variables.players["player_1"] = configuration.PlayerClass(name="player_1", color=(255,255,0))
global_variables.players["player_2"] = configuration.PlayerClass(name="player_2", color=(70,255,255))


# add character objects to the character list
global_variables.character_list["tank"] = imports.characters_and_sprites.Character(
    stat_object=imports.characters_and_sprites.Stats(
        name="tank",
        character_class="tank"
    ),
    sprite_data_object=imports.characters_and_sprites.SpriteData(),
    is_player_character=True
)

tank = global_variables.character_list["tank"]
tank.stats.attributes.max_hp = 150
tank.stats.attributes.base_weight=150
tank.stats.attributes.walk_speed=0.55
tank.stats.attributes.attack=12


########################################################################################################################
########################################################################################################################


# INITIALIZE OBJECTS


# create a camera object
global_variables.camera_object = imports.camera.Camera(
    position=(0, 0, 0),
    rotation=(0, 0))


########################################################################################################################
########################################################################################################################


# FIRST TIME LAUNCH MOVE LATER

# create a tile set from a predefined map
global_variables.world_tiles = imports.tile_system.generate_tile_set(
    path=imports.stage_list.stored_stages["stage_0"]["layout"]["tile_set"],
    anchor_point=(0, 0, 0),
    tile_size=50)


########################################################################################################################
########################################################################################################################


# DEFINITIONS

class GameWindow(pyglet.window.Window):

    def __init__ (self):
        """
        Creates a new pyglet window

        Creates a window with the dimension defined in the configuration
        """
        super(GameWindow, self).__init__(configuration.window_width, configuration.window_height, fullscreen=False)
        self.running = True

    def render(self):
        """

        :return:
        """
        pass

    # abstract methods are from the superclass in pyglet, check the pyglet files for more documentation

    def on_mouse_motion(self, x, y, dx, dy):
        """

        :param x: int
            distance from left edge in pixels
        :param y: int
            distance from bottom edge in pixels
        :param dx: int
            relative x position from previous mouse position
        :param dy: int
            relative y position form previous mouse position
        :event:
        """
        global_variables.event = None
        global_variables.mouse_pos = (x, y)
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        """
        A mouse button was released, the button is assigned to event

        :param x: int
            distance from left edge in pixels
        :param y: int
            distance from bottom edge in pixels
        :param button: int
            the mouse button that was released
        :param modifiers: int
            bitwise combination of keyboard modifiers currently active
        :event:
        """
        global_variables.event = button

    def on_key_press(self, symbol, modifiers):
        """
        A key is pressed and held down, the keys_pressed dictionary is updated

        :param symbol: int
            the key symbol that is pressed
        :param modifiers: int
            bitwise combination of key modifiers
        :event:
        """
        global_variables.keys_pressed[symbol] = True
        pass

    def on_key_release(self, symbol, modifiers):
        """
        A key is released, the keys_pressed dictionary is updated

         :param symbol: int
            the key symbol that is pressed
        :param modifiers: int
            bitwise combination of key modifiers
        :event:
        """
        global_variables.keys_pressed[symbol] = False
        pass


########################################################################################################################
########################################################################################################################


# MAIN FUNCTION


def main():
    """
    Starts the game

    Creates a new game window and schedules the pyglet clock to try to refresh the game at the defined refreshed rate

    :return:
    """
    new_window = GameWindow()

    def update_display(dt):
        """
        Refreshes the display

        Refreshes the window of the game every time this is called

        :param dt: double
            the delay since the last frame
        :return:
        """
        pass

    pyglet.clock.schedule_interval(update_display, 1 / configuration.render_fps)
    pyglet.app.run()


########################################################################################################################
########################################################################################################################


if __name__ == "__main__":
    main()
