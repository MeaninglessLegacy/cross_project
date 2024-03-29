########################################################################################################################
########################################################################################################################

# class to help generate a map of which tiles to hit
class attack_map():
    def __init__(self, center, forward, backwards, up, down, up_forward, up_backwards, down_forward, down_backwards):
        self.center = center
        self.forward = forward
        self.backwards = backwards
        self.up = up
        self.down = down
        self.up_forward = up_forward
        self.up_backwards = up_backwards
        self.down_forward = down_forward
        self.down_backwards = down_backwards



########################################################################################################################
########################################################################################################################

def Remove(duplicate):
    """
    removes duplicate tiles from the tile list
    :param duplicate: a list of all current tiles
    :return: returns the list of tiles with duplicates removed
    """
    final_list = []
    for item in duplicate:
            if item not in final_list:
                final_list.append(item)
    return final_list



def returnTilesHit(chr, map):
    """
    using the attack map class defined in attack_mapper.py, generates a list of tiles that are affected by the attack
    map
    :param chr: the character objects that the attack map is anchored to
    :param map: the attack map object that is provided
    :return:
    """

    # check if we were passed a map

    if isinstance(map, attack_map) == True:

        # chr position
        chr_pos = chr.stats.current_Tile

        # chr direction
        chr_heading = chr.spriteObject.heading

        # tiles hit
        tiles = []

        # determined based on facing direction
        if chr_heading == "-":
            # determine center tile
            centerTile = (chr.stats.current_Tile[0]+map.center[0], chr.stats.current_Tile[1]+map.center[1])

            tiles.append(centerTile)

            for attr, value in map.__dict__.items():
                if value != 0:
                    if attr == 'forward':
                        # forward
                        for i in range(0, map.forward):
                            tiles.append((centerTile[0] + i, centerTile[1]))
                    if attr == 'backwards':
                        # backwards
                        for i in range(0, map.backwards):
                            tiles.append((centerTile[0] - i, centerTile[1]))
                    if attr == 'up':
                        # up
                        for i in range(0, map.up):
                            tiles.append((centerTile[0], centerTile[1] + i))
                    if attr == 'down':
                        # down
                        for i in range(0, map.down):
                            tiles.append((centerTile[0], centerTile[1] - i))
                    if attr == 'up_forward':
                        # up_forward
                        for i in range(0, map.up_forward):
                            tiles.append((centerTile[0] + i, centerTile[1] + i))
                    if attr == 'up_backwards':
                        # up_backwards
                        for i in range(0, map.up_backwards):
                            tiles.append((centerTile[0] - i, centerTile[1] + i))
                    if attr == 'down_forward':
                        # down_forward
                        for i in range(0, map.down_forward):
                            tiles.append((centerTile[0] + i, centerTile[1] - i))
                    if attr == 'down_backwards':
                        # down_backwards
                        for i in range(0, map.down_backwards):
                            tiles.append((centerTile[0] - i, centerTile[1] - i))

        elif chr_heading == "+":
            # determine center tile
            centerTile = (chr.stats.current_Tile[0]-map.center[0], chr.stats.current_Tile[1]+map.center[1])

            tiles.append(centerTile)

            for attr, value in map.__dict__.items():
                if value != 0:
                    if attr == 'forward':
                        # forward
                        for i in range(0, map.forward):
                            tiles.append((centerTile[0] - i, centerTile[1]))
                    if attr == 'backwards':
                        # backwards
                        for i in range(0, map.backwards):
                            tiles.append((centerTile[0] + i, centerTile[1]))
                    if attr == 'up':
                        # up
                        for i in range(0, map.up):
                            tiles.append((centerTile[0], centerTile[1] + i))
                    if attr == 'down':
                        # down
                        for i in range(0, map.down):
                            tiles.append((centerTile[0], centerTile[1] - i))
                    if attr == 'up_forward':
                        # up_forward
                        for i in range(0, map.up_forward):
                            tiles.append((centerTile[0] - i, centerTile[1] + i))
                    if attr == 'up_backwards':
                        # up_backwards
                        for i in range(0, map.up_backwards):
                            tiles.append((centerTile[0] + i, centerTile[1] + i))
                    if attr == 'down_forward':
                        # down_forward
                        for i in range(0, map.down_forward):
                            tiles.append((centerTile[0] - i, centerTile[1] - i))
                    if attr == 'down_backwards':
                        # down_backwards
                        for i in range(0, map.down_backwards):
                            tiles.append((centerTile[0] + i, centerTile[1] - i))

        f_tiles = Remove(tiles)

        return  f_tiles