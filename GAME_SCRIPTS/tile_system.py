########################################################################################################################
########################################################################################################################


# TILE SYSTEM
# This scripts is for generating and using the map system of the game


########################################################################################################################
########################################################################################################################


# DEFINITIONS


class Tile():
    def __init__(self,
                 position=(0,0,0),
                 fill_color=(0,0,0),
                 grid_position=(0,0),
                 tile_size=50):
        """
        Creates a new tile object

        The tile object is used to create map layouts

        position: the world position of the tile
        grid_position: the relative grid position of a tile  in relationt
        width: the width of the tile in world units
        height: the height of the tile in world units
        fill_color: the rgb color of the tile
        occupied: if a character in on the grid tile in the world space
        tile_effects: an array of all effects that can affect players if they are position on this tile

        :param position:
        :param fill_color:
        :param grid_position:
        :param tile_size:
        """
        self.position = position
        self.grid_position = grid_position

        self.width = tile_size
        self.height = tile_size
        self.fill_color = fill_color

        self.occupied = False
        self.tile_effects = []


########################################################################################################################
########################################################################################################################


# FUNCTIONS


def generate_tile_set(
        path=None,
        anchor_point=(0,0,0),
        tile_size=50):
    """
    Returns an array of tile objects when provided with a layout

    This function reads a text file of zeros and ones in a grid and generates an array of tiles to match the grid
    arrangement provided. 1's represent a solid tile while 0's represent a blank space. The optional parameters of this
    function are the anchor point, where the tiles are tiled from in the world space. And the tile_size, how many world
    units each tile occupies.

    There are two error returns for this function, -1 represents that the file url was not provided, -2 represents that
    the file could not be read.

    :param path: string
        the path to the file containing the arrangement for the tile set
    :param anchor_point: tuple
        a three parameter tuple of integers represents where in the world space to begin tiling from
    :param tile_size: int
        the amount of world space units that a tile occupies
    :return: array
        on success returns an array of Tile objects in the arrangement provided
    :return error: int
        returns a -1 on having no file path provided and returns -2 when reading the file fails
    """
    if path is not None:
        tile_set = []
        with open(path, 'r') as layout_file:
            try:
                a = 0
                for line in layout_file:
                    a += 1
                    b = 0
                    for character in line:
                        b += 1
                        if character == "1":
                            new_tile = Tile(
                                position=(
                                    anchor_point[0] + a * tile_size,
                                    anchor_point[1] + b * tile_size,
                                    anchor_point[2]),
                                grid_position=(a,b),
                                tile_size=tile_size
                            )
                            tile_set.append(new_tile)
            except IOError:
                print("Failed to read file:", path)
                return -2
        return tile_set
    else:
        return -1
