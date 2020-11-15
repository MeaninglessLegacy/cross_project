############################################################################
############################################################################


import pygame, math

import Game_Scripts.basic_game_mechanics, Game_Scripts.functions

functions = Game_Scripts.functions
basic_game_mechanics = Game_Scripts.basic_game_mechanics


############################################################################
############################################################################

tile_set = []

############################################################################
############################################################################

class tile():
    def __init__(self, x, y, z, fillColor, gridTile, tileSize):
        #Coordinate, Width, Height
        self.x = x
        self.y = y
        self.z = z
        self.w = tileSize
        self.h = tileSize
        self.fillColor = fillColor
        self.gridPos = gridTile
        self.occupied = False
        self.tileEffects = []

############################################################################
############################################################################

#tile effects

class attack():
    def __init__(self, initiator, damage, ticks, knockback, breakShields):
        self.initiator = initiator
        self.damage = damage
        self.ticks = ticks
        self.knockback = knockback
        self.breakShields = breakShields


############################################################################
############################################################################

#2D Tile Map Generation

def updateTileEffects(tileset, ch):
    #get all tiles
    effect_tiles = []
    for i in range(0,len(tileset)):
        #if there is a tile effect
        if tileset[i].tileEffects != []:
            effect_tiles.append(tileset[i])

    for i in range(0, len(effect_tiles)):
        # dead tile effects
        dead_tile_effects = []
        # tile position
        tile_pos = effect_tiles[i].gridPos
        tile = effect_tiles[i]
        for tileEffect in range(0, len(tile.tileEffects)):
            #effect duration
            if tile.tileEffects[tileEffect].ticks < 1:
                dead_tile_effects.append(tile.tileEffects[tileEffect])
            elif tile.tileEffects[tileEffect].ticks >= 1:
                #if the tile is an attack tile
                if isinstance(tile.tileEffects[tileEffect], attack) == True:
                    #if the tile has a attack value
                    #for all characters standing on tile damage if not in same team
                    init_team = tile.tileEffects[tileEffect].initiator.stats.team
                    for key in ch:
                        #chr in the ch
                        chr = ch[key]
                        if chr.stats.current_Tile == tile_pos and chr.stats.team != init_team:
                            basic_game_mechanics.damageTarget(tile.tileEffects[tileEffect].initiator, chr, tile.tileEffects[tileEffect])
        # remove dead tile effects
        for d in dead_tile_effects:
            effect_tiles[i].tileEffects.remove(d)


    #it really do be like this sometimes
    for i in range(0, len(tileset)):
            tile = tileset[i]
            for tileEffect in range(0, len(tile.tileEffects)):
                if tile.tileEffects[tileEffect].ticks > 0:
                    tile.tileEffects[tileEffect].ticks -= 1

def updateTileSet(new_tile_set):

    global tile_set

    tile_set = new_tile_set

def createTileEffect(effect, tile):

    global tile_set

    tileset = tile_set

    #create a tile effect
    if len(tileset) > 0:
        for each_tile in tile_set:
            if each_tile.gridPos == tile:
                each_tile.tileEffects.append(effect)

def tileSet2D(a, b, x, y, z, size):

    tiles = []

    #a is horizontal
    #b is vertical
    for iA in range(0, a):
        for iB in range(0, b):
                bX = x + iA*size
                bY = y + iB*size
                new_tile = tile(bX, bY, z, (223, 248, 255), (iA+1,iB+1), size)
                tiles.append(new_tile)

    return  tiles

def borders2D(tileset):

    tileset = tileset

    firstTile = tileset[0]
    finalTile = tileset[len(tileset)-1]

    z = firstTile.z

    bordercorners = [(firstTile.x-firstTile.w/2,firstTile.y-firstTile.h/2),(finalTile.x+finalTile.w/2,finalTile.y+finalTile.h/2), z]
    #print(bordercorners)

    return bordercorners

def updateSpriteTiles(tileset, ch, players):

    #Reset All Tiles
    for tile in tile_set:
        tile.fillColor = (223, 248, 255)
        tile.occupied = False

    for key in ch:

        d=[]

        #Find the tile closest to character
        for tile in tile_set:

            x = tile.x-ch[key].spriteObject.x
            y = tile.y-ch[key].spriteObject.y

            d.append(math.sqrt(x*x+y*y))

        sD = functions.copyArray(d)
        sD.sort()

        fKey = []

        #Match the nearest tile
        for i in range(0, len(d)):
            if (sD[0] == d[i]):
                fKey.append(tileset[i])
                tileset[i].occupied = True
                #set tile color
                for ply in players:
                    if players[ply]['sC'] == ch[key]:
                        tileset[i].fillColor = players[ply]['color']
                break

        ch[key].stats.current_Tile = tileset[i].gridPos


############################################################################
############################################################################

#3D Tile Map Generation

def tileSet3D(a, b, c, x, y, z, tileSize):
    #Input Coords = (Top Left Block Coords (Centre))

    #A = HOR, B = VERT, C = DEPTH
    #Array: [horizontal][vertical][depth]

    tiles = []

    for iA in range(0, a):
        for iB in range(0, b):
            for iC in range(0, c):
                #print(blockWidth)
                bX = x + iA*tileSize
                bY = y - iB*tileSize
                bZ = z + iC*tileSize
                #newtile
                new_tile = tile(bX, bY, bZ, (0, 0, 0), [iA,iC], tileSize)
                tiles.append(new_tile)


    return tiles