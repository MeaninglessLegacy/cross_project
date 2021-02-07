########################################################################################################################
########################################################################################################################

# Stage Manager set stage backgrounds, music etc.
import pygame

from Game_Scripts import functions

########################################################################################################################
########################################################################################################################

stage_bgm = None

music_inc = 0



########################################################################################################################
########################################################################################################################

def draw_background(background_img, screen, cam, w, h):
    """
    draws the background image - not in use
    :param background_img:
    :param screen:
    :param cam:
    :param w:
    :param h:
    :return:
    """
    # Load the image
    img = functions.get_image(background_img['img'])
    img_pos = background_img['position']
    screen.blit(img, img_pos)
    # If a position is specified otherwise it is fixed
    # if img_pos != None:
    #     xPos = cam.x*10 - img_pos[0]
    #     yPos = cam.y - img_pos[1]
    #     screen.blit(img, (xPos, 0))
    # else:
    #     screen.blit(img, (0, 0))



def determine_regions(layer, cam, s):
    """
    finds out the size of the background, foreground and other stage elements - not in use
    :param layer:
    :param cam:
    :param s:
    :return:
    """

    start_pos = layer['position']
    scale = layer['scale']
    image = layer['img']

    '''
    start_pos --------------------------------------- start_pos x - scale x
    |                                                                   |
    |                                                                   |
    |                                                                   |
    start_pos y - scale y --start_pos x - scale x , start_pos y - scale y
    '''

    vt = []
    vt.append([start_pos[0], start_pos[1], -15])
    vt.append([start_pos[0] - scale[0], start_pos[1], -15])
    vt.append([start_pos[0], start_pos[1] - scale[1], -15])
    vt.append([start_pos[0] - scale[0], start_pos[1] - scale[1], -15])

    segments = [[0, 3], [2, 1], [0, 2], [3, 1]]
    edges = []
    dC = []

    for i in range(0, len(vt)):
        x = vt[i][0]
        y = vt[i][1]
        z = vt[i][2]

        # dC.append(distort2DCamera(x,y,cam,s))
        dC.append(functions.distort_point(x, y, z, cam, s))

    #pygame.draw.polygon(s, (25, 25, 25), [dC[1], dC[3], dC[2], dC[0]], 0)

    space = pygame.Rect(dC[0], (dC[1][0]-dC[0][0], dC[2][1]-dC[0][1]))

    if image != None:

        image = functions.get_image(layer['img'])

        if space.width < 5000 or space.height < 5000:

            #image = pygame.transform.scale(image, (space.width, space.height))
            image = functions.get_image(layer['img'])

        s.blit(image, space)



# main function
def render_stage(stage, screen, cam, layer, w, h):
    """
    tries to render the current stage - not in use
    :param stage:
    :param screen:
    :param cam:
    :param layer:
    :param w:
    :param h:
    :return:
    """

    background_screen = screen
    # Background
    if stage['background']['visible'] != False and layer == 2:
        draw_background(stage['background'], background_screen, cam, w, h)
    # Mid ground
    if stage['middle_ground']['visible'] != False and layer == 2:
        determine_regions(stage['middle_ground'], cam, screen)
    # Floor- stage floor is special but it is behind yet still needs alpha
    if stage['stage_floor']['visible'] != False and layer == 2:
        determine_regions(stage['stage_floor'], cam, screen)
    # On Floor
    if stage['on_floor']['visible'] != False and layer == 1:
        determine_regions(stage['on_floor'], cam, screen) 
    # Foreground
    if stage['foreground']['visible'] != False and layer == 1:
        determine_regions(stage['foreground'], cam, screen)

    return background_screen



def music_stage(stage, level):
    """
    uses pygame to play music for each stage
    :param stage: a stage object
    :param level: an integer value that is either 0 or 1, depending on if music should fade in
    :return:
    """

    global stage_bgm, music_inc

    # Background music
    if stage['bgm']['source'] != None and level == 0:
        get_bgm = stage['bgm']['source']
        #if the stage bgm is not the current bgm
        if stage_bgm != get_bgm:
            stage_bgm = get_bgm
            pygame.mixer.music.stop()
            pygame.mixer.music.load(stage['bgm']['source'])
            pygame.mixer.music.set_volume(0)
            music_inc = 1
            pygame.mixer.music.play(-1)

    if stage['bgm']['source'] != None and level == 0:
        if music_inc < stage['bgm']['fade_in_time']:
            music_inc += 1
            pygame.mixer.music.set_volume(stage['bgm']['volume']*(music_inc/stage['bgm']['fade_in_time']))

    if stage['bgm']['source'] != None and level == 1:
        if music_inc > 0:
            music_inc -= 1
            if (music_inc/stage['bgm']['fade_in_time']) >= 0:
                pygame.mixer.music.set_volume(stage['bgm']['volume'] * (music_inc/stage['bgm']['fade_in_time']))
        if music_inc <= 0:
            if stage_bgm != None:
                stage_bgm = None
                pygame.mixer.music.stop()
            return True

    return False



def set_bgm(bgm):
    """
    sets the pygame.mixer with new music to play
    :param bgm: a pygame.mixer sound object should be returned from the get_sound function in functions.py
    :return:
    """

    global stage_bgm

    if stage_bgm != bgm:
        stage_bgm = bgm
        pygame.mixer.music.stop()
        pygame.mixer.music.load(bgm)