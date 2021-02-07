########################################################################################################################
########################################################################################################################

# SPRITES
import math

from Game_Scripts import functions


########################################################################################################################
########################################################################################################################

class character():
    """
    This is the character object, it contains the sprite object, the stat object and whether or not this
    character can be controlled by the player
    """
    def __init__(self, spriteObject, stats, isSelected, playerCharacter):

        self.spriteObject = spriteObject
        self.stats = stats

        self.isSelected = isSelected
        self.playerCharacter = playerCharacter

class stats():
    """
    This is the stat object and is a work in progress
    """
    def __init__(self, name, chrClass, lvl, team, maxHP, rate, weight, walkspeed, atk):
        self.name = name
        self.lvl = lvl
        self.xp = 0
        self.chrClass = chrClass
        self.team = team
        self.rate = rate

        self.atk = atk
        self.shield_strength = 0
        self.shielding = False
        self.channeling = False
        self.invincible = False
        self.invincible_frames = 0


        self.maxHP = maxHP
        self.currentHP = maxHP

        self.walkspeed = walkspeed
        self.base_weight = weight
        self.weight = weight
        self.momentum = (0,0)
        self.current_Tile = (0,0)

        self.queued_actions = []
        self.previous_action = []

        self.canMove = True
        self.knockedOut = False
        self.stunTimer = 0



########################################################################################################################
########################################################################################################################

class sprite():
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
    def __init__(self, name, x, y, z, w, h, imgUrl, animationSet, animated, heading):
        # sprite position and orientation variables
        self.name = name
        self.x = x
        self.y = y
        self.z = z

        self.w = w
        self.h = h
        self.imgUrl = imgUrl
        self.trueSpr = None

        # self displayed image
        self.img = None

        # direction facing left/right
        self.heading = heading
        # direction traveling
        self.direction = "east"

        # sprite_box
        self.sprite_box = sprite_box(self)

        # animations
        self.animationSet = animationSet
        self.animated = animated

        self.animationList = [animationSet["combat_idle"]]
        self.animationCounter = 0

        self.moving = False
        self.combat = True

    def change_image(self, imgUrl):
        self.imgUrl = imgUrl
        self.img = functions.get_image(self.imgUrl)

    def reset_dimensions(self, w, h):
        self.w = w
        self.h = h

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