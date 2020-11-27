############################################################################
############################################################################

#SPRITES
import pygame,\
    math,\
    Game_Scripts.functions

functions = Game_Scripts.functions



############################################################################
############################################################################

#sprite class

class sprite():
    def __init__(self, name, x, y, z, w, h, imgUrl, animationSet, animated, heading):
        #Basic Variables
        self.name = name
        self.x = x
        self.y = y
        self.z = z

        self.w = w
        self.h = h
        self.imgUrl = imgUrl
        self.trueSpr = None

        #Load Image
        self.img = None

        #direction facing left/right
        self.heading = heading
        #direction traveling
        self.direction = "east"

        # sprite_box
        self.sprite_box = sprite_box(self)

        #animations
        self.animationSet = animationSet
        self.animated = animated

        self.animationList = [animationSet["combat_idle"]]
        self.animationCounter = 0

        self.moving = False
        self.combat = True

    def change_image(self, imgUrl):
        self.imgUrl = imgUrl
        self.img = functions.get_image(self.imgUrl, True)

    def reset_dimensions(self, w, h):
        self.w = w
        self.h = h



#Stats
class stats():
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



#character itself
class character():
    #Add other stuff later
    def __init__(self, spriteObject, stats, isSelected, playerCharacter):

        self.spriteObject = spriteObject
        self.stats = stats

        self.isSelected = isSelected
        self.playerCharacter = playerCharacter



############################################################################
############################################################################

#3D Sprites

#Generate A Box For the Sprite for 3D Rendering
class sprite_box(pygame.sprite.Sprite):

    def __init__(self, sprite):

        self.w = sprite.w
        self.h = sprite.h

        self.x = sprite.x
        self.y = sprite.y
        self.z = sprite.z

        self.vertexes = []

    def update_sprite_box(self, sprite, cam, s, w, h):
        """
            Sprite Box
            1-------0
            |       |
            |       |
            |       |
            2-------3
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

            dC.append(functions.distort_point(x, y, z, cam, s, w, h))

        #give the vertexes of the box
        self.vertexes = dC

        #scale of the spritebox to scale sprite
        self.xScale = math.floor(math.fabs(dC[0][0]-dC[1][0]))
        self.yScale = math.floor(math.fabs(dC[1][1]-dC[3][1]))

        self.rect = pygame.Rect(dC[2], (self.xScale, self.yScale))


############################################################################
############################################################################