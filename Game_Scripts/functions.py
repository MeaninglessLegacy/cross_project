############################################################################
############################################################################

import threading, pygame, math, time, pyglet

#Loaded Images
image_cache = {}

#scaled image cache, this one is gonna take alot of ram omega oof
scaled_image_cache = {}

#loaded sounds
sound_cache = {}

#global borders
borders = []

#image scaling threshold
#threshold = 100

############################################################################
############################################################################

class loadThread(threading.Thread):
    def __init__(self, threadID, name, load, stage):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.load = load
        self.stage = stage
        self.loaded = False
    def run(self):
        start_time = time.time()
        print("Starting " + self.name + " " + str(time.ctime(start_time)))
        preloadAnimationSet(self.load)
        preloadStage(self.stage)
        self.loaded = True
        print("Exiting " + self.name + " " + str(time.ctime(time.time())) + " Time taken " + str(time.time()-start_time))

############################################################################
############################################################################

#copies and returns an array
def copyArray(input):
    returnArray = []

    for i in range(0, len(input)):
        returnArray.append(input[i])

    return returnArray

def roundNear(x, base):
    return base * round(x/base)

#get scaled images, bascially what we need to do to not kill ram but keep it smooth is to find sizes around this things range and delete those not within this range
def get_scaled_image(image, url, size, threshold):
    global scaled_image_cache
    #Fall back
    this_size = (1,1)
    this_size = (roundNear(size[0],threshold), roundNear(size[1],threshold))
    #make the key value of the image
    key = url + str(this_size[0]) + str(this_size[1])
    rangeUrls = []
    deleteUrls = []
    #keeps 10 items range
    for i in range(-5,5):
        for z in range(-5,5):
            new_url = url + str(this_size[0]+threshold*z) + str(this_size[1]+threshold*i)
            rangeUrls.append(new_url)
    for old_key in scaled_image_cache:
        if not old_key in rangeUrls:
            deleteUrls.append(old_key)
    for rangeKey in rangeUrls:
        scaled_image_cache.pop(rangeKey, None)
    if not key in scaled_image_cache:
        texture = image.get_texture()
        texture.width = image
        texture.height = image
        scaled_image_cache[key] = image
    return scaled_image_cache[key]

#Checking if image is loaded and loading images that need to be loaded
def get_image(key, save_alpha):
    #if loaded image is not in the cache then load the image once
    if not key in image_cache:
        # This makes sure even if we can't find the file it does not crash the engine.
        try:
            fh = open(key, 'r')
        except FileNotFoundError:
            print('missing sprite:'+key)
            pass
        else:
            #change back to .convert_alpha() later
            image_cache[key] = pyglet.image.load(key)
    #return the image in cache
    return image_cache[key]

#clear loaded images
def clearCaches():

    global image_cache
    global sound_cache

    image_cache = {}
    sound_cache = {}

#update global borders
def updateBorders(newBorders):

    global borders

    borders = newBorders

#return borders
def get_Borders():

    return  borders

#Checking if sound is loaded and loading sound that need to be loaded
def get_sound(key):
    if not key in sound_cache:
        try:
            fh = open(key, 'r')
        except FileNotFoundError:
            print('missing sprite:'+key)
            pass
        else:
            sound_cache[key] = pygame.mixer.Sound(key)
    #return the image in cache
    return sound_cache[key]

############################################################################
############################################################################

#3D Functions

#rotatees a point
def rotatePoint(x, y, theta):
    si = math.sin(theta)
    co = math.cos(theta)

    #0,1  - 1,0 +cos +sin
    #1,0  -  0,-1 +cos -sin
    #0,-1  -  -1,0 -cos -sin
    #-1,0 - 0,1 -cos +sin

    #x = y*si + x*co
    #y = y*co - x*si
    #Reverse Because ccs,sin graph is counter clockwise invert sin
    x = x*co-y*si
    y = y*co+x*si

    return [x,y]

#Description: Distorts a singular point. Useful for drawing images
def distortPoint(x,y,z, cam, s, w, h):
    x -= cam.x
    y -= cam.y
    z -= cam.z

    xzR = rotatePoint(x, z, cam.xRot)
    x = xzR[0]
    z = xzR[1]
    yzR = rotatePoint(y, z, cam.yRot)
    y = yzR[0]
    z = yzR[1]

    """
    xr = cam.xRot
    yr = cam.yRot

    si = math.sin(xr)
    co = math.cos(xr)

    x = x * co - z * si
    z = z * co - x * si
    """

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



############################################################################
############################################################################


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
def preloadAnimationSet(animation_set):
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

def preloadStage(stage):
    if stage['background']['img'] != None:
        if try_file(stage['background']['img']) == True:
            get_image(stage['background']['img'], False)
    if stage['middle_ground']['img'] != None:
        if try_file(stage['middle_ground']['img']) == True:
            get_image(stage['middle_ground']['img'], False)
    if stage['stage_floor']['img'] != None:
        if try_file(stage['stage_floor']['img']) == True:
            get_image(stage['stage_floor']['img'], True)
    if stage['on_floor']['img'] != None:
        if try_file(stage['on_floor']['img']) == True:
            get_image(stage['on_floor']['img'], True)
    if stage['foreground']['img'] != None:
        if try_file(stage['foreground']['img']) == True:
            get_image(stage['foreground']['img'], True)
    if stage['bgm']['source'] != None:
        if try_file(stage['bgm']['source']) == True:
            pygame.mixer.music.load(stage['bgm']['source'])


############################################################################
############################################################################