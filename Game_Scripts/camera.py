########################################################################################################################
########################################################################################################################

#Camera purpose is to keep camera centered on subjects

import math

from Game_Scripts import functions

cam_to_pos = None



########################################################################################################################
########################################################################################################################

def tween_camera(cam, new_position):
    """
    moves a camera more smoothly between two points - THIS SOLUTION SUCKS NEEDS TO BE FIXED
    :param cam: the camera object to tween
    :param new_position: the new position for the camera object
    :return:
    """

    x_dist = new_position[0] - cam.x
    y_dist = new_position[1] - cam.y
    z_dist = new_position[2] - cam.z

    dist = math.sqrt((x_dist*x_dist+y_dist*y_dist)+z_dist*z_dist)

    if dist > 1:
        if math.fabs(x_dist) > 0.5:
            cam.x += x_dist/10
        if math.fabs(y_dist) > 0.5:
            cam.y += y_dist/10
        if math.fabs(z_dist) > 0.5:
            cam.z += z_dist/10



def determine_camera_position(characters, cam):
    """
    using all the characters on the stage, this determines the position the camera needs to be in to be able to view
    all the characters at once
    :param characters: the list of all characters objects, class is defined in characters_and_sprites.py
    :param cam: the camera object to calculate the position for
    :return:
    """

    global cam_to_pos, cam_old_pos

    distances = []
    points = []
    farthest_pair = None

    min_z = 2

    for chr in characters:

        spr = characters[chr].spriteObject
        self_distances = []

        chrs = []
        flist = []

        for other_chr in characters:

            x = characters[other_chr].spriteObject.x - spr.x
            y = characters[other_chr].spriteObject.y - spr.y
            self_distances.append(math.sqrt(x * x + y * y ))
            chrs.append(characters[other_chr])

        sorted_distances = functions.copy_array(self_distances)
        sorted_distances.sort()
        sorted_distances.reverse()

        # Match Each Sorted Value to actual Object
        for i in range(0, len(sorted_distances)):
            for i1 in range(0, len(self_distances)):
                if (sorted_distances[i] == self_distances[i1]):
                    flist.append([chrs[i1], self_distances[i1]])

        points.append([spr, flist[0][0].spriteObject, flist[0][1]])

        distances.append(self_distances[0])

    distances.sort()
    distances.reverse()

    for i in range(0, len(points)):
        if distances[0] == points[i][2]:
            farthest_pair = points[i]

    point_1 = (farthest_pair[0].x,farthest_pair[0].y)
    point_2 = (farthest_pair[1].x,farthest_pair[1].y)

    midpoint = ((point_1[0]+point_2[0])/2,(point_1[1]+point_2[1])/2)

    x = midpoint[0]
    y = midpoint[1]-4
    new_z = 0.3*distances[0]
    if new_z < min_z:
        new_z = min_z

    if cam_to_pos != (x, y, new_z):
        cam_to_pos = (x, y, new_z)

    tween_camera(cam, cam_to_pos)