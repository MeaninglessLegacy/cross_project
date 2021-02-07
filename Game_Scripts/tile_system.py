########################################################################################################################
########################################################################################################################

import math

from Game_Scripts import functions, game_mechanics
# tileSet global variable is already imported from functions


########################################################################################################################
########################################################################################################################

class tile():
    def __init__(self, x, y, z, fillColor, gridTile, tileSize):
        # Coordinate, Width, Height
        self.x = x
        self.y = y
        self.z = z
        self.w = tileSize
        self.h = tileSize
        self.fillColor = fillColor
        self.gridPos = gridTile
        self.occupied = False
        self.tileEffects = []



########################################################################################################################
########################################################################################################################

#TILE EFFECTS

class attack():
    """
    an effect for a tile that can be added to it's tileEffects property. this property causes characters or objects on
    the tile to take damage
    """
    def __init__(self, initiator, damage, ticks, knockback, breakShields):
        self.initiator = initiator
        self.damage = damage
        self.ticks = ticks
        self.knockback = knockback
        self.breakShields = breakShields



########################################################################################################################
########################################################################################################################

# CREATE TILE EFFECTS

def create_tile_effect(effect, tile):
    """
    adds tile effects to a tile
    :param effect: the effect that needs to be added to the tile
    :param tile: the position of the tile that the effect needs to be added to
    :return:
    """
    global tileSet

    # create a tile effect
    if len(tileSet) > 0:
        for each_tile in tileSet:
            if each_tile.gridPos == tile:
                each_tile.tileEffects.append(effect)



########################################################################################################################
########################################################################################################################

# 2D TILE GENERATION

def tile_set_2d(a, b, x, y, z, size):
    """
    creates a list of tiles based on the input parameter in a grid
    :param a: horizontal tile distance
    :param b: vertical tile distance
    :param x,y,z: the anchor point of the set of tiles
    :param size: the size of each tile
    :return:
    """
    tiles = []

    # a is horizontal
    # b is vertical
    for iA in range(0, a):
        for iB in range(0, b):
                bX = x + iA*size
                bY = y + iB*size
                new_tile = tile(bX, bY, z, (223, 248, 255), (iA+1,iB+1), size)
                tiles.append(new_tile)

    return tiles



def borders_2d(tileset):
    """
    generates the outmost borders of the list of tiles

    1. needs to be redone using a convex hull algorithm

    :param tileset:
    :return:
    """
    firstTile = tileset[0]
    finalTile = tileset[len(tileset)-1]

    z = firstTile.z

    bordercorners = [(firstTile.x-firstTile.w/2,firstTile.y-firstTile.h/2),(finalTile.x+finalTile.w/2,finalTile.y+finalTile.h/2), z]
    #print(bordercorners)

    return bordercorners



########################################################################################################################
########################################################################################################################

# UPDATING TILE EFFECTS

def update_tile_effects(tileset, ch):
    """
    counts down the timers on all tile effects and removes tile effects that have expired from tiles
    :param tileset: a list of tiles
    :param ch: a list of characters
    :return:
    """
    # get all tiles
    effect_tiles = []
    for i in range(0,len(tileset)):
        # if there is a tile effect
        if tileset[i].tileEffects != []:
            effect_tiles.append(tileset[i])

    for i in range(0, len(effect_tiles)):
        # dead tile effects
        dead_tile_effects = []
        # tile position
        tile_pos = effect_tiles[i].gridPos
        tile = effect_tiles[i]
        for tileEffect in range(0, len(tile.tileEffects)):
            # effect duration
            if tile.tileEffects[tileEffect].ticks < 1:
                dead_tile_effects.append(tile.tileEffects[tileEffect])
            elif tile.tileEffects[tileEffect].ticks >= 1:
                # if the tile is an attack tile
                if isinstance(tile.tileEffects[tileEffect], attack) == True:
                    # if the tile has a attack value
                    # for all characters standing on tile damage if not in same team
                    init_team = tile.tileEffects[tileEffect].initiator.stats.team
                    for key in ch:
                        # chr in the ch
                        chr = ch[key]
                        if chr.stats.current_Tile == tile_pos and chr.stats.team != init_team:
                            game_mechanics.damage_target(tile.tileEffects[tileEffect].initiator, chr, tile.tileEffects[tileEffect])
        # remove dead tile effects
        for d in dead_tile_effects:
            effect_tiles[i].tileEffects.remove(d)


    # it really do be like this sometimes
    for i in range(0, len(tileset)):
            tile = tileset[i]
            for tileEffect in range(0, len(tile.tileEffects)):
                if tile.tileEffects[tileEffect].ticks > 0:
                    tile.tileEffects[tileEffect].ticks -= 1



def update_sprite_tiles(tileset, ch, players):
    """
    finds the tiles that sprites and objects are on and assigns the tile position to the sprite's tile position
    1. needs a better algorithm for finding the nearest tile to the character
    :param tileset:
    :param ch:
    :param players:
    :return:
    """
    # Reset All Tiles
    for tile in tileset:
        tile.fillColor = (223, 248, 255)
        tile.occupied = False

    for key in ch:

        d=[]

        # Find the tile closest to character
        for tile in tileset:

            x = tile.x-ch[key].spriteObject.x
            y = tile.y-ch[key].spriteObject.y

            d.append(math.sqrt(x*x+y*y))

        sD = functions.copy_array(d)
        sD.sort()

        fKey = []

        # Match the nearest tile
        for i in range(0, len(d)):
            if (sD[0] == d[i]):
                fKey.append(tileset[i])
                tileset[i].occupied = True
                # set tile color
                for ply in players:
                    if players[ply].sC == ch[key]:
                        tileset[i].fillColor = players[ply].color
                break

        ch[key].stats.current_Tile = tileset[i].gridPos



########################################################################################################################
########################################################################################################################

#3D Tile Map Generation

# def tileSet3D(a, b, c, x, y, z, tileSize):
#     #Input Coords = (Top Left Block Coords (Centre))
#
#     #A = HOR, B = VERT, C = DEPTH
#     #Array: [horizontal][vertical][depth]
#
#     tiles = []
#
#     for iA in range(0, a):
#         for iB in range(0, b):
#             for iC in range(0, c):
#                 #print(blockWidth)
#                 bX = x + iA*tileSize
#                 bY = y - iB*tileSize
#                 bZ = z + iC*tileSize
#                 #newtile
#                 new_tile = tile(bX, bY, bZ, (0, 0, 0), [iA,iC], tileSize)
#                 tiles.append(new_tile)
#
#
#     return tiles