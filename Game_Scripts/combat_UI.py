############################################################################
############################################################################

#Combat_UI

import pygame,\
    math,\
    pyglet

from pygame import font

import Game_Scripts.controls,\
    Game_Scripts.ui_assets,\
    Game_Scripts.functions

functions = Game_Scripts.functions
controls = Game_Scripts.controls
ui_assets = Game_Scripts.ui_assets



############################################################################
############################################################################

font_cache = {}

ui_cache = {}



############################################################################
############################################################################

#Draw the health bar of the selected character

def draw_health_bar(UI_surface, w, h, ch):

    #Size of Health Bar
    sizeX = math.floor(w*0.45)
    sizeY = h

    #Position of Health Bar
    positionX = math.floor(w*0.15)
    positionY = 0

    #Set Character
    character = ch
    #Get HP Stats
    maxHP = character.stats.maxHP
    currentHP = character.stats.currentHP

    #HpBar filled percent
    filledPercent = currentHP/maxHP

    #final size, floored because it takes an interger value
    fSizeX = math.floor(sizeX*filledPercent)

    #Draw rect on UI_Surface
    pygame.draw.rect(UI_surface, (53, 61, 22), (positionX, positionY, sizeX, sizeY), 0)
    #color of hp bar
    hp_color = (183, 255-(255*(1-filledPercent)), 151-(151*(1-filledPercent)))
    #Health bar
    if currentHP > 0:
        pygame.draw.rect(UI_surface, hp_color, (positionX, positionY, fSizeX, sizeY), 0)

    #text surface
    f = font.Font(None, math.ceil(sizeY*1.5))
    #hp text littearly just HP
    hp_text = f.render("HP", True, [255, 255, 255])
    hp_text_rect = hp_text.get_rect(center=(math.ceil(w * 0.075), math.ceil(h * 0.55)))
    UI_surface.blit(hp_text, hp_text_rect)
    #hp label text
    text_Surface = f.render((str(int(math.ceil(currentHP)))+"/"+str(maxHP)), True, [255, 255, 255])
    text_rect = text_Surface.get_rect(center=(math.ceil(w*0.8), math.ceil(h*0.55)))
    UI_surface.blit(text_Surface, text_rect)



#the ui along the bottom

def draw_character_boxes(primaryScreen, UI_surface, w, h, ch, players):
    #character boxes along the bottom
    #top half is character image/portrait sprite

    #first we need to draw the area that each object is going to be
    #no of player character
    player_characters = {}
    for key in ch:
        if ch[key].playerCharacter == True:
            player_characters[key] = ch[key]

    no_characters = len(player_characters)

    ui_elements = {}

    #for each character create a box
    for chr in player_characters:
        #size of the gui
        i = list(player_characters.keys()).index(chr)
        #how many indents there are each indent is 0.05 of the screen width, the number of indents is always one more than the no of characters
        indents_size = 0.05*(no_characters+1)
        #therefore the size of each character box should be the remaining width/no_characters
        char_guiX = (1-indents_size)/no_characters
        #we will scale down the char_guiX if it is greater than a portion of the screen
        if char_guiX > 0.14:
            char_guiX = 0.14
        #now we need to determine an indentation size
        indent_size = (1-(char_guiX*no_characters))/(no_characters+1)
        #y scale is arbituary
        char_guiY = 0.175
        #screen that is the box
        gui_main = pygame.Surface((math.floor(char_guiX*w),math.floor(char_guiY*h)), pygame.SRCALPHA)
        #debug
        #gui_main.fill((255,255,255))
        #final step blit the gui onto the game
        #x pos is the indents + previous guis so
        char_guiX_pos = char_guiX*i*w + indent_size*(i+1)*w
        char_guiY_pos = h*0.95 - char_guiY*h
        # Now we need to to draw the gui itself onto our surface



        # first thing we need to do is draw the character portrait
        ui_chr = player_characters[chr]
        #the entire background will be the portrait we will draw ontop of it
        ui_portrait = ui_assets.return_asset(ui_chr.stats.chrClass)["portrait"]
        #we have a portrait
        if not ui_portrait is None:
            #Return the asset in image
            key = ui_portrait["image"]
            asset = functions.get_image(key, True)
            #asset = pygame.transform.scale(asset, (math.floor(char_guiX*w), math.floor(char_guiY*h)))
            asset = functions.get_image(ui_portrait["image"], True)
            gui_main.blit(asset, (0, 0))

        #now that the portrait is drawn if it is selected draw selected box
        if ui_chr.isSelected == True:
            ui_selected = ui_assets.return_asset("universal")["portrait_select"]
            asset = functions.get_image(ui_selected["image"], True)
            asset = pygame.transform.scale(asset, (math.floor(char_guiX * w), math.floor(char_guiY * h)))
            #asset = functions.get_scaled_image(asset, ui_selected["image"], (math.floor(char_guiX * w), math.floor(char_guiY * h)))
            ply = controls.find_player(players, player_characters[chr])
            if ply != None:
                # reset RGB
                asset.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
                # add in new RGB values
                asset.fill(ply['color'][0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
            gui_main.blit(asset, (0, 0))

        #define a region for the rest of the ui to be drawn on

        stat_displaysX = math.floor(char_guiX*w)
        stat_displaysY = math.floor(char_guiY*h*0.33)

        stat_displaysX_pos = 0
        stat_displaysY_pos = char_guiY*h-stat_displaysY-char_guiY*h*0.1

        stat_displays = pygame.Surface((stat_displaysX,stat_displaysY))
        stat_displays.fill((50,50,50, 150))

        #draw the health bar
        hpBarX=math.floor(stat_displaysX)
        hpBarY=math.floor(stat_displaysY*0.3)
        hp_bar = pygame.Surface((hpBarX,hpBarY), pygame.SRCALPHA)
        draw_health_bar(hp_bar, hpBarX, hpBarY, ui_chr)
        #primaryScreen.blit(hp_bar, (ui_chr.spriteObject.spriteBox.rect.midbottom))
        stat_displays.blit(hp_bar, (0, stat_displaysY-hpBarY-stat_displaysY*0.1))

        #name label and level and stuff
        f = font.Font(None, math.ceil(stat_displaysY * 0.5))
        # name label
        name_text = f.render(ui_chr.stats.name, True, [255, 255, 255])
        name_text_rect = name_text.get_rect(center=(math.ceil(stat_displaysX * 0.2), math.ceil(stat_displaysY * 0.3)))
        stat_displays.blit(name_text, name_text_rect)
        # level label
        '''level_text = f.render((str(ui_chr.stats.lvl)), True, [255, 255, 255])
        level_rect = level_text.get_rect(center=(math.ceil(stat_displaysX * 0.8), math.ceil(stat_displaysY * 0.3)))
        stat_displays.blit(level_text, level_rect)'''



        #The next thing we need to be able to draw is the top left and top right sections for currently playing music and entering map

        #blit statdisplays
        gui_main.blit(stat_displays, (stat_displaysX_pos, stat_displaysY_pos))
        UI_surface.blit(gui_main, (char_guiX_pos, char_guiY_pos))

    #blit entire gui onto screen
    primaryScreen.blit(UI_surface, (0, 0))



############################################################################
############################################################################



start_trigger = False
duration_frames = 0
trigger_frames = 0



############################################################################
############################################################################



def battle_start_animation(primaryScreen, UI_surface, text, w, h):

    global start_trigger, trigger_frames, duration_frames

    battle_text = text

    if trigger_frames > 0:
        trigger_frames -= 1

        #screen_size
        s_x = w
        s_y = math.floor(h/2)
        #the primary layer that the thing is drawn on
        main_display = UI_surface
        interval = (duration_frames/4)
        #intervals
        i1 = interval
        i2 = interval/2+i1
        i3 = interval+i1+i2
        i4 = interval*5/8+i1+i2+i3
        #used interval for timeframes
        I1 = duration_frames-i1
        I2 = duration_frames-i2
        I3= duration_frames-i3
        I4 = duration_frames-i4
        #animation
        if trigger_frames >= I1:
            #sides come in
            t = (duration_frames-trigger_frames)/i1
            left_rect_x = math.floor(-s_x + t*s_x)
            right_rect_x = math.floor(s_x - t*s_x)
            #left_rect = pygame.Rect((left_rect_x, 0, s_x, s_y))
            #right_rect = pygame.Rect((right_rect_x, 0, s_x, s_y))
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [0, 0, left_rect_x, 0, left_rect_x, 150, 0, 150]))
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [0, 0, right_rect_x, 0, right_rect_x, 150, 0, 150]))
            #pygame.draw.rect(main_display, (0,0,0,150), left_rect, 0)
            #pygame.draw.rect(main_display, (0,0,0, 150), right_rect, 0)
        if I1 > trigger_frames >= I2:
            #the rect
            #rect = pygame.Rect((0, 0, s_x, s_y))
            #pygame.draw.rect(main_display, (0, 0, 0, 150), rect, 0)
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [0, 0, 0, 150, s_x, s_y, s_x, s_y]))
            #the text
            #interval 1-4 thus 3 intervals
            tinterval = (I1-I2)/len(battle_text)
            #how many multiples of trigger_frames lies in tinterval, how many intervals have passed
            m_interval = math.ceil((trigger_frames-I2)/tinterval)
            #letter to spell
            letters = len(battle_text)-m_interval
            list_of_output = []
            for i in range(0,letters):
                list_of_output.append(battle_text[i])
            output_string = "".join(list_of_output)

            f = font.Font(None, math.ceil(s_y * 0.25))
            name_text = f.render(output_string, True, [255, 255, 255])
            name_text_rect = name_text.get_rect(
            center=(math.ceil(s_x * 0.5), math.ceil(s_y * 0.5)))
            #main_display.blit(name_text, name_text_rect)
        if I2 > trigger_frames >= I3:
            # the rect
            #rect = pygame.Rect((0, 0, s_x, s_y))
            #pygame.draw.rect(main_display, (0, 0, 0, 150), rect, 0)
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [0, 0, 0, 150, s_x, s_y, s_x, s_y]))
            #the front
            f = font.Font(None, math.ceil(s_y * 0.25))
            name_text = f.render(battle_text, True, [255, 255, 255])
            name_text_rect = name_text.get_rect(
                center=(math.ceil(s_x * 0.5), math.ceil(s_y * 0.5)))
            #main_display.blit(name_text, name_text_rect)
        if I2 > trigger_frames >= I3:
            int = (I2-I3)/4
            m = math.ceil((I2-trigger_frames)/int)
            if (m % 2) == 0:
                battle_text = ''.join(['>', battle_text, '<'])
            #rect = pygame.Rect((0, 0, s_x, s_y))
            #pygame.draw.rect(main_display, (0, 0, 0, 150), rect, 0)
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [0, 0, 0, 150, s_x, s_y, s_x, s_y]))
            #the front
            f = font.Font(None, math.ceil(s_y * 0.25))
            name_text = f.render(battle_text, True, [255, 255, 255])
            name_text_rect = name_text.get_rect(
                center=(math.ceil(s_x * 0.5), math.ceil(s_y * 0.5)))
            #main_display.blit(name_text, name_text_rect)
        if I3 > trigger_frames >= I4:
            # sides leave in
            t = (I3 - trigger_frames) / (i4-i3-i2-i1)
            left_rect_x = math.floor(0 + t * s_x)
            right_rect_x = math.floor(0 - t * s_x)
            #left_rect = pygame.Rect((left_rect_x, 0, s_x, s_y))
            #right_rect = pygame.Rect((right_rect_x, 0, s_x, s_y))
            #pygame.draw.rect(main_display, (0, 0, 0, 150), left_rect, 0)
            #pygame.draw.rect(main_display, (0, 0, 0, 150), right_rect, 0)
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [0, 0, left_rect_x, 0, left_rect_x, 150, 0, 150]))
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [0, 0, right_rect_x, 0, right_rect_x, 150, 0, 150]))
        #blit
        #primaryScreen.blit(main_display, (0,s_y/2))
    elif trigger_frames <= 0:
        start_trigger = False



#Battle start
def battle_start_trigger(duration):
    global start_trigger, trigger_frames, duration_frames
    duration_frames = duration
    trigger_frames = duration
    start_trigger = True



############################################################################
############################################################################



blankSurface = None

#Main function
def draw_combat_ui(primaryScreen, UI_surface, w, h, ch, players, teams):

    global start_trigger, c_Text, c_text_cache

    #Blank Surface/Redraw the UI
    '''if globals()['blankSurface'] is None:
        globals()['blankSurface'] = pygame.Surface((w, h), pygame.SRCALPHA)
    elif UI_surface is not blankSurface:
        UI_surface = pygame.Surface((w, h), pygame.SRCALPHA)'''
    #draw Ui
    draw_character_boxes(primaryScreen, UI_surface, w, h, ch, players)



############################################################################
############################################################################