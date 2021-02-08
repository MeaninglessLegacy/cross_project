########################################################################################################################
########################################################################################################################


# SPRITES AND CHARACTER OBJECTS


########################################################################################################################
########################################################################################################################


# DEFINITIONS


class Character:
    """
    The character object contains three child objects and two settings.
    """
    def __init__(self,
                 stat_object=None,
                 sprite_data_object=None,
                 is_player_character=None):
        """
        Create a new character object

        stats: a object of the class Stats
        sprite_data: a object of the class SpriteData
        sprite: a pyglet sprite object
        is_selected: a boolean value of whether this character is selected by a character or not
        is_player_character: a boolean value of whether this character is selectable by players

        :param stat_object: Stats object
            a object of the class Stats
        :param sprite_data_object: SpriteData object
            a object of the class SpriteData
        :param is_player_character: boolean
            a boolean value of whether this character is selectable by players
        """

        self.stats = stat_object
        self.sprite_data = sprite_data_object
        self.sprite = None

        self.is_selected = False
        self.is_player_character = is_player_character


class Stats:
    """
    the stat object has several child classes which stats are organized into
    """
    def __init__(self,
                 name=None,
                 character_class=None):
        """
        Create a stat object

        The Stats class is made of five inner classes can the values within each inner class should be set manually
        before a character is used. For more information on the values within each inner class check the documentation
        for each inner class

        bio: the inner Bio class object
        attributes: the inner Attribute class object
        position: the inner Position class object
        actions: the inner Actions class object
        paramters: the inner Parameters class object

        :param name: string
            a string that is the character's name
        :param character_class: string
            a string that is the character's class
        """
        self.bio = self.Bio(name=name, character_class=character_class)
        self.attributes = self.Attributes()
        self.position = self.Position()
        self.actions = self.Actions()
        self.parameters = self.Parameters()

    class Bio:
        def __init__(self,
                     name=None,
                     character_class=None):
            """
            Create a bio object

            This class under the Stats class includes the name of the character as a string, the class of the character
            as a string as well as how much xp this character has accumulated.

            name: the name of the character
            character_class: the class of the character
            xp: the total experience accumulated
            lvl: the level of the character

            :param name: string
                a string of the character's name
            :param character_class: string
                a string of the character's class
            """
            self.name = name
            self.character_class = character_class

            self.xp = 0
            self.lvl = 0

    class Attributes:
        def __init__(self):
            """
            Create an attribute object

            This class under the Stats Class includes the combat attributes of character

            max_hp: the total health points of the character
            current_hp: the current health points of the character
            base_weight: how heavy the character normally is
            effective_weight: what the character actually weights, this is used in knockback calculations
            walk_speed: how fast the character can move in the world space
            attack: how much damage a character is able to deal
            shield_strength: this value is usually only changed by skills, it is a measure of how much damage reduction
            a character has while blocking
            """
            self.max_hp = 0
            self.current_hp = 0

            self.base_weight = 0
            self.effective_weight = 0

            self.walk_speed = 0

            self.attack = 0

            self.shield_strength = 0

    class Position:
        def __init__(self):
            """
            Create a position object

            This class under Stats Class measures where in the world space the character currently is

            momentum: a x,y vector indicating the character's momentum in 2D space
            current_tile: a x,y coordinate pair indicating the position of the character in world space
            """
            self.momentum = (0, 0)
            self.current_tile = (0, 0)

    class Actions:
        def __init__(self):
            """
            Create an action object

            This class under Stats Class contains two lists of actions to be executed by the character.

            queued_actions: a list of actions that are to be executed by the character
            previous_action: a list that should only have one entry of what the previous action executed by the
            character was
            """
            self.queued_actions = []
            self.previous_action = []

    class Parameters:
        def __init__(self):
            """
            Create a parameter object

            This class under Stats Class are boolean flags which represent the state the character is in

            shielding: if the character is shielding or not
            channeling: if the character is channeling or not
            invincible: if the character currently is not affected by all other sources in the world space
            can_move: if the character can move or not, unrelated to momentum and more related to if the character has
            the capacity to perform an action
            knocked_out: if the character is knocked_out or not, usually used in tandem with can_move to determine
            if a character can perform an action or not
            """
            self.shielding = False
            self.channeling = False
            self.invincible = False
            self.can_move = True
            self.knocked_out = False

class SpriteData:
    """
    the sprite object of the character contains information on where it is positioned, which direction it is facing,
    the animations that are used with the character and if it is animated or not
    :var x,y,z are the position of the anchor point of the sprite
    :var imgUrl is the path to the image of the sprite
    :var trueSpr is the pyglet sprite object used for rendering
    :var img is the loaded image of the sprite and should be a reference to the image in the cache
    :var sprite_box is a rectangular box that is used to determine how to render the sprite based on the space it takes
    in the game world
    """
    def __init__(self):
        pass
    #     # sprite position and orientation variables
    #     self.name = name
    #     self.x = x
    #     self.y = y
    #     self.z = z
    #
    #     self.w = w
    #     self.h = h
    #     self.imgUrl = imgUrl
    #
    #     # self displayed image
    #     self.img = None
    #
    #     # direction facing left/right
    #     self.heading = heading
    #     # direction traveling
    #     self.direction = "east"
    #
    #     # sprite_box
    #     self.sprite_box = None#sprite_box(self)
    #
    #     # animations
    #     self.animationSet = animationSet
    #     self.animated = animated
    #
    #     self.animationList = [animationSet["combat_idle"]]
    #     self.animationCounter = 0
    #
    #     self.moving = False
    #     self.combat = True
    #
    # def change_image(self, imgUrl):
    #     self.imgUrl = imgUrl
    #     self.img = functions.get_image(self.imgUrl)
    #
    # def reset_dimensions(self, w, h):
    #     self.w = w
    #     self.h = h



class sprite_box():
    """
    a rectangular plane that is projected into the game world to return information on the size of the sprite to render
    and where to render it
    :var w,h the default width and height of the sprite'renderTo image
    :var x,y,z the anchor point of the sprite from the sprite object
    """
    def __init__(self, sprite):

        self.w = sprite.w
        self.h = sprite.h

        self.x = sprite.x
        self.y = sprite.y
        self.z = sprite.z

        self.vertexes = []

    def update_sprite_box(self, sprite, cam, renderTo, w, h):
        """
        The list of vertices of the sprite box are as follows
        1-------0
        |       |
        |       |
        |       |
        2-------3
        :param sprite: the sprite object
        :param cam: the camera object that is viewing the sprite box
        :param renderTo: the space that the sprite box should be rendered to
        :param w: the width of the sprite box
        :param h: the height of the sprite box
        :return:
        """

        self.w = sprite.w
        self.h = sprite.h

        self.x = sprite.x
        self.y = sprite.y
        self.z = sprite.z

        # vt vertices of the sprite box
        vt = []

        vt.append([self.x - 5, self.y-10, self.z])
        vt.append([self.x + 5, self.y-10, self.z])
        vt.append([self.x + 5, self.y, self.z])
        vt.append([self.x - 5, self.y, self.z])

        dC = []
        # Draw Coordinates = dt

        for i in range(0, len(vt)):
            x = vt[i][0]
            y = vt[i][1]
            z = vt[i][2]

            dC.append(functions.distort_point(x, y, z, cam, renderTo, w, h))

        # give the vertexes of the box
        self.vertexes = dC

        # scale of the spritebox to scale sprite
        self.xScale = math.floor(math.fabs(dC[0][0]-dC[1][0]))
        self.yScale = math.floor(math.fabs(dC[1][1]-dC[3][1]))

        #self.rect = pygame.Rect(dC[2], (self.xScale, self.yScale))