########################################################################################################################
########################################################################################################################

import math
import threading
import time
import pygame

from global_variables import *

########################################################################################################################
########################################################################################################################

#these things are stupid and needs to be fixed or removed

class loadThread(threading.Thread):
    """
    the functions preload_animation_set and preload_stage, take all the files in the characters that need to be
    displayed and loads them once to the caches, it does this on a separate thread
    -this current causes the game to freeze whenever this thread is running
    """
    def __init__(self, threadID, name, load, stage):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.load = load
        self.stage = stage
        self.loaded = False
    def run(self):
        start_time = time.time()
        print("STARTING " + self.name + " " + str(time.ctime(start_time)))
        preload_animation_set(self.load)
        preload_stage(self.stage)
        self.loaded = True
        print("EXITING " + self.name + " " + str(time.ctime(time.time())) + " TIME TAKEN " + str(time.time()-start_time))

def copy_array(input):
    """
    copies and returns a new array - this is pointless and should be removed
    :param input: old array that you want copied
    :return:
    """
    returnArray = []

    for i in range(0, len(input)):
        returnArray.append(input[i])

    return returnArray


########################################################################################################################
########################################################################################################################

# IMAGE LOADING AND DELETING

def get_image(key):
    """
    loads an image with pyglet and stores it in the image cache if it has not already been loaded. Once the image is
    loaded or the image has been loaded before it returns the image
    :param key: this is the url of the image and the key of the image in the cache
    :return: returns the image from the cache
    """
    # if loaded image is not in the cache then load the image once
    if not key in image_cache:
        # error handling
        try:
            fh = open(key, 'r')
        except FileNotFoundError:
            print('ERROR missing image:'+key)
            pass
        else:
            image_cache[key] = pyglet.image.load(key)
    # return the image in cache
    return image_cache[key]



def get_sound(key):
    """
    check if a sound is loaded, less will loaded the sound with pygame and return the loaded sound for use
    -phase out the use of pygame
    :param key: the url of the sound file
    :return: the sound object from pygame
    """
    if not key in sound_cache:
        try:
            fh = open(key, 'r')
        except FileNotFoundError:
            print('missing sprite:'+key)
            pass
        else:
            sound_cache[key] = pygame.mixer.Sound(key)
    # return the image in cache
    return sound_cache[key]



def clear_caches():
    """
    this function frees the space taken up by the caches and should be called whenever loading occurs
    :return:
    """

    global image_cache, sound_cache

    image_cache.clear()
    sound_cache.clear()

########################################################################################################################
########################################################################################################################

# 3D Functions

# rotatees a point
def rotate_point(x, y, theta):
    si = math.sin(theta)
    co = math.cos(theta)

    # 0,1  - 1,0 +cos +sin
    # 1,0  -  0,-1 +cos -sin
    # 0,-1  -  -1,0 -cos -sin
    # -1,0 - 0,1 -cos +sin

    # x = y*si + x*co
    # y = y*co - x*si
    # Reverse Because ccs,sin graph is counter clockwise invert sin
    x = x*co-y*si
    y = y*co+x*si

    return [x,y]



def distort_point(x,y,z, cam, s, w, h):
    """
        Distorts a singular point. Useful for drawing images
        xr = cam.xRot
        yr = cam.yRot

        si = math.sin(xr)
        co = math.cos(xr)

        x = x * co - z * si
        z = z * co - x * si
    """
    x -= cam.x
    y -= cam.y
    z -= cam.z

    xzR = rotate_point(x, z, cam.xRot)
    x = xzR[0]
    z = xzR[1]
    yzR = rotate_point(y, z, cam.yRot)
    y = yzR[0]
    z = yzR[1]

    # Distort XY by INV Z DIFFERENCE
    # LARGER DIFFERENCE = SMALLER
    # SMALLER DIFFERENCE = BIGGER

    if (z == 0):
        z = 0.00000000001

    zDistort = (w / 2) / z

    x *= zDistort
    y *= zDistort

    x += w / 2
    y += h / 2

    return [x,y]



########################################################################################################################
########################################################################################################################


# preloader give animations as a array of the url
def preload(animations):
    for i in range(0, len(animations)):
        for o in range(0, len(animations[i]["frames"])):
            if not animations[i]["frames"][o] in image_cache:
                # This makes sure even if we can't find the file it does not crash the engine.
                try:
                    fh = open(animations[i]["frames"][o], 'r')
                except FileNotFoundError:
                    print('missing sprite' + animations[i]["frames"][o])
                    pass
                else:
                    image_cache[animations[i]["frames"][o]] = pygame.image.load(animations[i]["frames"][o]).convert_alpha()
                    #print(str("loaded "+animations[i]["frames"][o]))
                    if animations[i]['sounds'] != {}:
                        for sound in animations[i]['sounds']:
                            get_sound(animations[i]['sounds'][sound]['source'])



# preloader feed this a set of animations eg animations.animations['tank']
def preload_animation_set(animation_set):
    for key in animation_set:
        for o in range(0, len(animation_set[key]["frames"])):
            if not animation_set[key]["frames"][o] in image_cache:
                # This makes sure even if we can't find the file it does not crash the engine.
                try:
                    fh = open(animation_set[key]["frames"][o], 'r')
                except FileNotFoundError:
                    print('missing sprite' + animation_set[key]["frames"][o])
                    pass
                else:
                    image_cache[animation_set[key]["frames"][o]] = pyglet.image.load(animation_set[key]["frames"][o])#pygame.image.load(animation_set[key]["frames"][o]).convert_alpha()
                    #print(str("loaded " + animation_set[key]["frames"][o]))
                    if animation_set[key]['sounds'] != {}:
                        for sound in animation_set[key]['sounds']:
                            get_sound(animation_set[key]['sounds'][sound]['source'])
                            #print(str("loaded" + animation_set[key]['sounds'][sound]['source']))



def try_file(file):
    try:
        fh = open(file, 'r')
    except FileNotFoundError:
        print('missing file' + file)
        return False
    else:
        return True



def preload_stage(stage):
    if stage['background']['img'] != None:
        if try_file(stage['background']['img']) == True:
            get_image(stage['background']['img'])
    if stage['middle_ground']['img'] != None:
        if try_file(stage['middle_ground']['img']) == True:
            get_image(stage['middle_ground']['img'])
    if stage['stage_floor']['img'] != None:
        if try_file(stage['stage_floor']['img']) == True:
            get_image(stage['stage_floor']['img'])
    if stage['on_floor']['img'] != None:
        if try_file(stage['on_floor']['img']) == True:
            get_image(stage['on_floor']['img'])
    if stage['foreground']['img'] != None:
        if try_file(stage['foreground']['img']) == True:
            get_image(stage['foreground']['img'])
    if stage['bgm']['source'] != None:
        if try_file(stage['bgm']['source']) == True:
            pygame.mixer.music.load(stage['bgm']['source'])



########################################################################################################################
########################################################################################################################

# def round_near(x, base):
#     return base * round(x/base)
# 
# 
# 
# #get scaled images, bascially what we need to do to not kill ram but keep it smooth is to find sizes around this things range and delete those not within this range
# def get_scaled_image(image, url, size, threshold):
#     global scaled_image_cache
#     #Fall back
#     this_size = (1,1)
#     this_size = (round_near(size[0],threshold), round_near(size[1],threshold))
#     #make the key value of the image
#     key = url + str(this_size[0]) + str(this_size[1])
#     rangeUrls = []
#     deleteUrls = []
#     #keeps 10 items range
#     for i in range(-5,5):
#         for z in range(-5,5):
#             new_url = url + str(this_size[0]+threshold*z) + str(this_size[1]+threshold*i)
#             rangeUrls.append(new_url)
#     for old_key in scaled_image_cache:
#         if not old_key in rangeUrls:
#             deleteUrls.append(old_key)
#     for rangeKey in rangeUrls:
#         scaled_image_cache.pop(rangeKey, None)
#     if not key in scaled_image_cache:
#         texture = image.get_texture()
#         texture.width = image
#         texture.height = image
#         scaled_image_cache[key] = image
#     return scaled_image_cache[key]