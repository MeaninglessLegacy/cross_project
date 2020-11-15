import pygame, sys, math, os.path, threading, pyglet, time

#Tkinter stuff
pygame.init()

pygame.mixer.pre_init(44100,-16,8, 4096)

display = pyglet.canvas.get_display()

#screen
#w = 512
#h = 288
#w = 1024
#h = 576
w = 1280
h = 720
#clock
t = pygame.time.Clock()

#At the end replace all file paths with this
filepath = os.path.dirname(__file__)

############################################################################
############################################################################



mousePos = (0,0)

event = "NONE"



############################################################################
############################################################################

#Screens
#Main Screen that the game is drawn on

bgVertexList = {}

combat_UI = pyglet.graphics.Batch()

main_batch = pyglet.graphics.Batch()

background_batch = pyglet.graphics.Batch()

title_screen = pyglet.graphics.Batch()

background_screen = pyglet.graphics.Batch()

loading_screen = pyglet.graphics.Batch()

generic_screen = pyglet.graphics.Batch()

############################################################################
############################################################################

#Importing Other Scripts

import Game_Scripts.functions, Game_Scripts.sprites, Game_Scripts.animations, Game_Scripts.controls, Game_Scripts.renderer, Game_Scripts.tileMap, Game_Scripts.animator, Game_Scripts.combat_UI, Game_Scripts.actions_manager, Game_Scripts.basic_game_mechanics, Game_Scripts.stage_Manager, Game_Scripts.stages, Game_Scripts.ui_elements, Game_Scripts.screen_layouts

#Extraenous functions such as copying arrays
functions = Game_Scripts.functions

#sprites
#sprites.sprite(self, name, x, y, z, w, h, imgUrl, animationSet, animated) is class object of sprite
#sprites.character() is class object of all characters
sprites = Game_Scripts.sprites

#animations list
#animations.animations['key'] is the list of animations
#animations.returnAnimation('string') is used to return an animation and prevent errors if animation doesn't exist
animations = Game_Scripts.animations

#controls
#controls.sC(ch) selected character returns key of the character in the dicitonary so to use, use ch[sC(ch)]
#controls.change_sC(character, ch) change selected character
#controls.keyPress(ch, cam, borders) key press event
controls = Game_Scripts.controls

#renderer
#renderer.camera2D(x,y,z) 2D camera class
#(renderList, cam, screen, borders) - 2D render main function, cam is what cam to render from but most likely going to be flat 2d cam, screen is screen where everything is
renderer = Game_Scripts.renderer

#3dTileMap
tileMapper = Game_Scripts.tileMap

#animate the animations
#animationManager(objects_to_animate, ch)
#animationPlayer(sprite, animation, ch)
#addAnimation(character, animation)
#removeAnimation(character, animation)
animator = Game_Scripts.animator

#ui_elements
ui_elements = Game_Scripts.ui_elements

#combat_UI manager
combat_UI_manager = Game_Scripts.combat_UI

#actions manager
actions_manager = Game_Scripts.actions_manager

#movement mechanics, damage mechanics, knock down, recover mechanics
basic_game_mechanics = Game_Scripts.basic_game_mechanics

#stage manager, set stage, begin battles, end battles, set backgrounds
stage_manager = Game_Scripts.stage_Manager

#stages
stages_list = Game_Scripts.stages

#screen layouts UI related
screen_layouts = Game_Scripts.screen_layouts

############################################################################
############################################################################

#Game Variables

gameStart = True

game_fps = animations.fps

fps = animations.fps

#characters
ch = {}

#players

players = {
    "player_1" : {
        'player' : 'player_1',
        'color' : (255,255,0),
        'sC' : None,
        'control_type' : 'keyboard',
        'ability_cd' : {
            '1' : 0,
            '2' : 0,
            '3' : 0,
            '4' : 0,
            'chr_swap' : 0,
        },
        'abilities_held' : {
            '1' : False,
            '2' : False,
            '3' : False,
            '4' : False,
        },
        'abilities_held_timers' : {
            '1' : 0,
            '2' : 0,
            '3' : 0,
            '4' : 0,
        }
    },
    "player_2" : {
        'player' : 'player_2',
        'color' : (70,255,255),
        'sC' : None,
        'control_type' : 'keyboard',
        'ability_cd' : {
            '1' : 0,
            '2' : 0,
            '3' : 0,
            '4' : 0,
            'chr_swap' : 0,
        },
        'abilities_held' : {
            '1' : False,
            '2' : False,
            '3' : False,
            '4' : False,
        },
        'abilities_held_timers' : {
            '1' : 0,
            '2' : 0,
            '3' : 0,
            '4' : 0,
        }
    },
}

#render type 3d cam can also be used for 2.5D
#cam = renderer.camera2D(550, 100, 0)
cam=renderer.camera3D(20, -20, 15, 0, 0)

#animate objects
objects_to_animate = []

#ojbects to update movement
objects_to_manage = []

#Map-Temporary
#tile_set = tileMapper.tileSet3D(15, 1, 10, 0, 0, -15, 0.5)
tile_set = tileMapper.tileSet2D(20,10,0,0,-15,3)
borders = tileMapper.borders2D(tile_set)

#Stage
#current_stage = stages_list.stages['bridge_1']
current_stage = stages_list.stages['blank']
#current_stage = stages_list.stages['field_day_1']

#ui_elements on screen
ui_elements_list = []

############################################################################
############################################################################

#Game Logic Variables

#what screen we are at
screen = "title"

#the last screen
previous_screen = ""

#change screen
change_screen = ""

#teams
teams = None

############################################################################
############################################################################

ch["tank"] = sprites.character(
    spriteObject=sprites.sprite(
        name = "tank",
        x=1056,
        y=-72,
        z=-14,
        w=400,
        h=300,
        heading="+",
        imgUrl="Sprite_Assets/Sprites/Tank_Sprites/Combat_Walk/Tank_Walk_Combat_Frame_1.png",
        animationSet = animations.animations["tank"],
        animated = True
    ),
    stats = sprites.stats(
        name = "Player_1",
        chrClass = "tank",
        team = '1',
        maxHP = 150,
        lvl= 10,
        weight=150,
        rate = 1,
        walkspeed = 0.55,
        atk = 12,
    ),
    isSelected=False,
    playerCharacter = True,
)

ch["dummy"] = sprites.character(
    spriteObject=sprites.sprite(
        name = "dummy",
        x=72,
        y=-72,
        z=-14,
        w=400,
        h=300,
        heading="-",
        imgUrl="Sprite_Assets/Sprites/Tank_Sprites/Combat_Walk/Tank_Walk_Combat_Frame_1.png",
        animationSet = animations.animations["tank"],
        animated = True
    ),
    stats = sprites.stats(
        name = "Player_2",
        chrClass = "tank",
        team = '2',
        maxHP = 150,
        lvl=10,
        weight=150,
        rate = 1,
        walkspeed = 0.55,
        atk = 12,
    ),
    isSelected=False,
    playerCharacter = True
)

############################################################################
############################################################################

load_screen_elements = []
load_transition = 0
delay = 0

#functions switching between screens

def changeScreen(new_screen):

    global load_transition, change_screen, screen

    change_screen = new_screen

    screen = "load"

def load_animation():

    global load_transition, loading_screen, load_screen_elements, delay, screen, change_screen
    #bgVertexList[len(bgVertexList)+1] = pyglet.shapes.Rectangle(0, 0, w, h, color=(0, 0, 0), batch=loading_screen)

    if len(load_screen_elements) > 0:
        for i in range(0, len(load_screen_elements)):
            if load_screen_elements[i].name == 'loading_label':
                if delay == 0:
                    delay = math.floor(fps / 4)
                    if load_screen_elements[i].text == 'Loading':
                        load_screen_elements[i].text = 'Loading.'
                    elif load_screen_elements[i].text == 'Loading.':
                        load_screen_elements[i].text = 'Loading..'
                    elif load_screen_elements[i].text == 'Loading..':
                        load_screen_elements[i].text = 'Loading...'
                    elif load_screen_elements[i].text == 'Loading...':
                        load_screen_elements[i].text = 'Loading'
                else:
                    delay -= 1

            ui_elements.draw_ui_element(load_screen_elements[i], loading_screen, w, h)

def load_screen():

    global load_transition, loading_screen, load_screen_elements, delay, screen, change_screen

    load_animation()

    if load_transition <= fps:

        load_transition += 1

    elif load_transition > fps:

        load_transition = 0

        screen = change_screen

############################################################################
############################################################################

#Game Logic

#combat win comditions = 1 team has zero participants remains
def returnTeams(list_chrs):
    #first lets make a team dictionary
    teams = {}

    for chr in list_chrs:
        #get team of chr
        team_key = list_chrs[chr].stats.team
        #if the team is already in the list
        if team_key in teams:
            teams[team_key][chr] = list_chrs[chr]
        elif not team_key in teams:
            teams[team_key] = {}
            teams[team_key][chr] = list_chrs[chr]

    return teams

#how many live team members there are
def return_alive_members(teams):

    live_count = {}

    for team in teams:
        live_count[team] = 0
        for chr in teams[team]:
            if teams[team][chr].stats.currentHP > 0:
                live_count[team] += 1

    return  live_count

#win conditions
def win_conditions(win_conditions):

    for i in range(0, len(win_conditions)):
        #the win condition we are checking
        win_condition = win_conditions[i]
        #elimate win condition
        if win_condition == 'eliminate':
            teams = returnTeams(ch)
            alive_members = return_alive_members(teams)
            for team in alive_members:
                if alive_members[team] == 0:
                    return True
    return False

############################################################################
############################################################################

#Title Screen
def title_Screen():

    global  ui_elements_list, title_screen, ch, gameStart, s, mouse_pos

    # we need mouse position
    mouse_pos = mousePos

    # draw animated background and stuff

    # draw ui_stuff
    if len(ui_elements_list) > 0:

        for i in range(0, len(ui_elements_list)):
            ui_elements.draw_ui_element(ui_elements_list[i], title_screen, w, h)
            ui_elements.mouseHover(ui_elements_list[i], title_screen, mouse_pos, w, h)

            # Button Interactivity
            if hasattr(ui_elements_list[i], 'mouseOver'):
                if ui_elements_list[i].mouseOver == True:
                    ui_elements_list[i].text_color = (0, 255, 255)
                    ui_elements_list[i].x_position = 0.8
                    ui_elements_list[i].width = 0.3
                elif ui_elements_list[i].mouseOver == False:
                    ui_elements_list[i].text_color = (255, 255, 255)
                    ui_elements_list[i].x_position = 0.9
                    ui_elements_list[i].width = 0.2
                if ui_elements_list[i].mouseOver == True and event == pyglet.window.mouse.LEFT:
                     if ui_elements_list[i].name == "duel_button":
                         # should bring us to a stage and character selection menu
                         for chr in ch:
                             ch[chr].stats.currentHP = ch[chr].stats.maxHP
                         changeScreen("combat")
                     elif ui_elements_list[i].name == "quit_button":
                         gameStart = False

    title_screen.draw()

############################################################################
############################################################################

drawList = []

#Load Encounter
def load_Encounter():

    global game_fps, objects_to_animate, objects_to_manage, cam, current_stage, ch, tile_set, borders, teams, drawList, ui_elements_list, previous_screen

    animations.update_fps(game_fps)

    # first time we arrive on this screen
    ui_elements_list = []

    # we need to load everything right?
    '''
    1.add characters to ch
    2.load stage
    3.load character animations
    4.add characters to manager and animator
    5.1 load the map <---
    5.move characters to spawn locations
    6.countdown battle
    '''
    # set the proper fps tick
    game_fps = fps
    # clear old slates
    objects_to_manage = []
    objects_to_animate = []
    # center camera
    cam.x = current_stage['camera_spawn'][0]
    cam.y = current_stage['camera_spawn'][1]
    cam.z = current_stage['camera_spawn'][2]
    # loading the characters
    for chr in ch:
        load_thread = functions.loadThread(1, "Load-Thread", animations.animations[ch[chr].stats.chrClass],
                                           current_stage)
        load_thread.start()
        # check to see if our threads have loaded
        while load_thread.loaded == False:
            load_animation()
        objects_to_animate.append(ch[chr])
        objects_to_manage.append(ch[chr])
    screen = "combat"
    previous_screen = "combat"
    # setting up the map
    tile_set = current_stage['map']['tile_set']
    borders = tileMapper.borders2D(tile_set)
    # spawning the characters
    teams = returnTeams(ch)
    spawn_locations = current_stage['spawns']
    # first we need to assign each team a slot for spawning
    slots_assigned = {}
    for team in teams:
        if not team in slots_assigned:
            slots_assigned[team] = None
            i = list(slots_assigned.keys()).index(team)
            try:
                spawn_locations[i]
            except:
                pass
            else:
                slots_assigned[team] = spawn_locations[i]
            for chr in teams[team]:
                ch[chr].spriteObject.x = slots_assigned[team][0]
                ch[chr].spriteObject.y = slots_assigned[team][1]
    # transition into combat
    # functions.updateBorders(borders)
    # Add Stuff to Render
    drawList = []
    drawList.append(ch["tank"].spriteObject)
    drawList.append(ch["dummy"].spriteObject)
    drawList.extend(tile_set)
    combat_UI_manager.battle_Start_Trigger(game_fps*2)


def game_mechanics():
    global tile_set, ch, players, borders, objects_to_manage, objects_to_animate, drawList, cam, borders, s, current_stage,background_screen, combat_UI, w, h, teams, bgVertexList
    # update tiles
    tileMapper.updateTileSet(tile_set)
    # Update Sprite Locations on Grid Pos
    tileMapper.updateSpriteTiles(tile_set, ch, players)
    # Update Tile Effects
    tileMapper.updateTileEffects(tile_set, ch)

    # update borders
    functions.updateBorders(borders)

    # what to update actions for
    actions_manager.action_manager(objects_to_manage, ch)
    # What to animate
    animator.animationManager(objects_to_animate, ch)

    # update the basic mechanics
    basic_game_mechanics.updateBasicMechanics(ch)

    # Render Options
    renderer.flatRender(drawList, cam, borders, main_batch, current_stage, background_batch, ch, w, h, bgVertexList)
    # renderer.render3D(drawList, cam, s)

    #######OVERLAY UIS

    # Draw UIs below renderer because renderer clears our screen
    #combat_UI_manager.draw_combat_UI(s, combat_UI, w, h, ch, players, teams)

############################################################################
############################################################################

#Run Game
def runGame():

    global screen, previous_screen, ui_elements_list, event

    # fps at top of engine
    #pyglet.clock.tick()
    #t.tick(game_fps)
    #print(t.get_fps())
    animations.update_fps(t.get_fps())

    #this handles pygame dying
    #event = pygame.event.poll()
    #if event.type == pygame.QUIT:
    #    run = False

    #What to run on title screen
    if screen == "title":

        if previous_screen != "title":


            #first time we arrive on this screen
            ui_elements_list = []
            previous_screen = "title"

            #add all the buttons and stuff
            ui_elements_list = screen_layouts.return_screen_elements('title_screen')

            stage_manager.set_bgm('Stage_Assets/bgm/The Last Encounter Collection/TLE INTERLUDE A-STANDALONE LOOP.wav')
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)

        else:

            title_Screen()

    #What to run if screen is combat
    if screen == "combat":

        #first time on this screen
        if previous_screen != "combat":
            load_Encounter()

        win_con = win_conditions(['eliminate'])

        if win_con == False:

            #Controls
            #key press events
            #controls.keyPress3D(ch, cam)
            stage_manager.music_stage(current_stage, 0)
            for player in players:
                if players[player]['control_type'] == 'keyboard':
                    controls.keyPress2D(ch, borders, cam, players, player)

        elif win_con == True:
            finish = stage_manager.music_stage(current_stage, 1)
            for player in players:
                if players[player]['control_type'] == 'keyboard':
                    controls.keyPress2D(ch, borders, cam, players, player)
            #battle end animations before leaving
            if finish == False:
                pass
            elif finish == True:
                changeScreen('title')

        # start combat
        game_mechanics()

        if combat_UI_manager.start_trigger == True:
            combat_UI_manager.start_trigger = False
            #combat_UI_manager.battle_Start_Animation(main_batch, generic_screen, "BATTLE START", w, h)
            for chr in ch:
                ch[chr].stats.canMove = True

    elif screen =='load':
        pygame.time.delay(fps)
        if previous_screen != "load":
            previous_screen = "load"
            pygame.mixer.stop()
            functions.clearCaches()
            load_screen_elements = screen_layouts.return_screen_elements('loading_screen')
        elif previous_screen == "load":
            load_screen()
    #failsaif
    elif screen == '' or screen == None:
        screen = 'load'
        change_screen('title')



class main(pyglet.window.Window):
    def __init__ (self):
        super(main, self).__init__(w, h, fullscreen=False, vsync=False)

        self.running = True

    def on_draw(self):
        self.render()

    def render(self):

        # And flip the GL buffer
        if screen == "combat":
            background_batch.draw()
            main_batch.draw()
        else:
            title_screen.draw()
        combat_UI.draw()
        background_screen.draw()
        loading_screen.draw()
        generic_screen.draw()

        self.flip()

        # print(bgVertexList)
        for i in bgVertexList:
            bgVertexList[i].delete()
        bgVertexList.clear()

        self.clear()

    def run(self):
        #time.sleep(1 / (fps + 30))

        #dt = pyglet.clock.tick()
        #print(pyglet.clock.get_fps())

        event = None

        self.render()

        runGame()
        # while self.running is True:
        #
        #     time.sleep(1/(fps+30))
        #
        #     dt = pyglet.clock.tick()
        #     print(pyglet.clock.get_fps())
        #
        #     event = None
        #
        #     self.render()
        #
        #     runGame()
        #
        #     event = self.dispatch_events()
        #     if event and event.type == pygame.QUIT:
        #         self.running = False

    def on_mouse_motion(window, x, y, dx, dy):
        global mousePos, event
        event = None
        mousePos = (x, y)
        pass

    def on_mouse_release(window, x, y, button, modifiers):
        global event
        event = button
        pass

    def on_key_press(window, symbol, modifiers):
        controls.keysPressed[symbol] = True
        pass

    def on_key_release(window, symbol, modifiers):
        controls.keysPressed[symbol] = False
        pass

    def on_draw(window):

        if screen == "combat":
            background_batch.draw()
            main_batch.draw()
        else:
            title_screen.draw()
        combat_UI.draw()
        background_screen.draw()
        loading_screen.draw()
        generic_screen.draw()
        window.flip()


newObj = main()

def update(dt):
    #print(1/dt)
    newObj.run()

pyglet.clock.schedule_interval(update, 1/fps)
pyglet.app.run()