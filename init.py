############################################################################
############################################################################

import pygame,\
    sys,\
    math,\
    os.path,\
    threading,\
    pyglet,\
    time



############################################################################
############################################################################

#At the end replace all file paths with this
filepath = os.path.dirname(__file__)

mousePos = (0,0)

event = "NONE"



############################################################################
############################################################################

#PYGAME INIT

pygame.init()

pygame.mixer.pre_init(44100,-16,8, 4096)

t = pygame.time.Clock()


#PYGLET INIT

display = pyglet.canvas.get_display()

window_w = 1280
window_h = 720

batchedItems = {}

uiBatch = pyglet.graphics.Batch()

worldBatch = pyglet.graphics.Batch()

backgroundBatch = pyglet.graphics.Batch()



############################################################################
############################################################################

#Importing Scripts

import Game_Scripts.functions,\
    Game_Scripts.sprites,\
    Game_Scripts.animations,\
    Game_Scripts.controls,\
    Game_Scripts.renderer,\
    Game_Scripts.tileMap,\
    Game_Scripts.animator,\
    Game_Scripts.combat_ui,\
    Game_Scripts.actions_manager,\
    Game_Scripts.basic_game_mechanics,\
    Game_Scripts.stage_manager,\
    Game_Scripts.stages,\
    Game_Scripts.ui_elements,\
    Game_Scripts.screen_layouts

#Extraenous functions such as copying arrays
functions = Game_Scripts.functions

#sprites
#sprites.sprite(self, name, x, y, z, window_w, window_h, imgUrl, animationSet, animated) is class object of sprite
#sprites.character() is class object of all characters
sprites = Game_Scripts.sprites

#animations list
#animations.animations['key'] is the list of animations
#animations.returnAnimation('string') is used to return an animation and prevent errors if animation doesn't exist
animations = Game_Scripts.animations

#controls
#controls.sC(chrList) selected character returns key of the character in the dicitonary so to use, use chrList[sC(chrList)]
#controls.change_sC(character, chrList) change selected character
#controls.keyPress(chrList, cam, borders) key press event
controls = Game_Scripts.controls

#renderer
#renderer.camera2D(x,y,z) 2D camera class
#(renderList, cam, screen, borders) - 2D render main function, cam is what cam to render from but most likely going to be flat 2d cam, screen is screen where everything is
renderer = Game_Scripts.renderer

#3dTileMap
tile_map = Game_Scripts.tileMap

#animate the animations
#animationManager(objToAnimate, chrList)
#animationPlayer(sprite, animation, chrList)
#addAnimation(character, animation)
#removeAnimation(character, animation)
animator = Game_Scripts.animator

#ui_elements
ui_elements = Game_Scripts.ui_elements

#ui manager
combat_ui_manager = Game_Scripts.combat_ui

#actions manager
actions_manager = Game_Scripts.actions_manager

#movement mechanics, damage mechanics, knock down, recover mechanics
basic_game_mechanics = Game_Scripts.basic_game_mechanics

#stage manager, set stage, begin battles, end battles, set backgrounds
stage_manager = Game_Scripts.stage_manager

#stages
stages_list = Game_Scripts.stages

#screen layouts UI related
screen_layouts = Game_Scripts.screen_layouts



############################################################################
############################################################################



#Character List
chrList = {}

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



############################################################################
############################################################################



#init of game
gameStart = True

gameFps = animations.fps

fps = animations.fps

#animate objects
objToAnimate = []

#ojbects to update movement
objToManage = []

#ui_elements on screen
objOfUi = []

#render type 3d cam can also be used for 2.5D
#cam = renderer.camera2D(550, 100, 0)
cam=renderer.camera_3d(20, -20, 15, 0, 0)

#Map-Temporary
#tileSet = tile_map.tileSet3D(15, 1, 10, 0, 0, -15, 0.5)
tileSet = tile_map.tile_set_2d(20,10,0,0,-15,3)
borders = tile_map.borders_2d(tileSet)

#Stage
#currentStage = stages_list.stages['bridge_1']
currentStage = stages_list.stages['blank']
#currentStage = stages_list.stages['field_day_1']



############################################################################
############################################################################


#Screen Elements
screen = "title"

#the last screen
previousScreen = ""

#change screen
changeScreen = ""

loadScreenElements = []
loadTransition = 0
delay = 0

drawList = []



############################################################################
############################################################################



#game variables
teams = None



############################################################################
############################################################################

chrList["tank"] = sprites.character(
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

chrList["dummy"] = sprites.character(
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

#functions switching between screens

def change_screen(new_screen):

    global loadTransition, changeScreen, screen

    changeScreen = new_screen

    screen = "load"



def load_animation():

    global loadTransition, loadingBatch, loadScreenElements, delay, screen, changeScreen
    #batchedItems[len(batchedItems)+1] = pyglet.shapes.Rectangle(0, 0, window_w, window_h, color=(0, 0, 0), batch=loadingBatch)

    if len(loadScreenElements) > 0:
        for i in range(0, len(loadScreenElements)):
            if loadScreenElements[i].name == 'loading_label':
                if delay == 0:
                    delay = math.floor(fps / 4)
                    if loadScreenElements[i].text == 'Loading':
                        loadScreenElements[i].text = 'Loading.'
                    elif loadScreenElements[i].text == 'Loading.':
                        loadScreenElements[i].text = 'Loading..'
                    elif loadScreenElements[i].text == 'Loading..':
                        loadScreenElements[i].text = 'Loading...'
                    elif loadScreenElements[i].text == 'Loading...':
                        loadScreenElements[i].text = 'Loading'
                else:
                    delay -= 1

            ui_elements.draw_ui_element(loadScreenElements[i], loadingBatch, window_w, window_h)



def load_screen():

    global loadTransition, loadingBatch, loadScreenElements, delay, screen, changeScreen

    load_animation()

    if loadTransition <= fps:

        loadTransition += 1

    elif loadTransition > fps:

        loadTransition = 0

        screen = changeScreen



############################################################################
############################################################################

#Game Logic

#combat win comditions = 1 team has zero participants remains
def return_teams(list_chrs):
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
            teams = return_teams(chrList)
            alive_members = return_alive_members(teams)
            for team in alive_members:
                if alive_members[team] == 0:
                    return True
    return False



############################################################################
############################################################################

#Title Screen
def title_screen():

    global  objOfUi, worldBatch, chrList, gameStart, s, mouse_pos

    # we need mouse position
    mouse_pos = mousePos

    # draw animated background and stuff

    # draw ui_stuff
    if len(objOfUi) > 0:

        for i in range(0, len(objOfUi)):
            ui_elements.draw_ui_element(objOfUi[i], uiBatch, batchedItems, window_w, window_h)
            ui_elements.mouse_hover(objOfUi[i], mouse_pos, window_w, window_h)

            # Button Interactivity
            if hasattr(objOfUi[i], 'mouseOver'):
                if objOfUi[i].mouseOver == True:
                    objOfUi[i].text_color = (0, 255, 255)
                    objOfUi[i].x_position = 0.85
                    objOfUi[i].width = 0.15
                elif objOfUi[i].mouseOver == False:
                    objOfUi[i].text_color = (255, 255, 255)
                    objOfUi[i].x_position = 0.9
                    objOfUi[i].width = 0.1
                if objOfUi[i].mouseOver == True and event == pyglet.window.mouse.LEFT:
                     if objOfUi[i].name == "duel_button":
                         # should bring us to a stage and character selection menu
                         for chr in chrList:
                             chrList[chr].stats.currentHP = chrList[chr].stats.maxHP
                         change_screen("combat")
                     elif objOfUi[i].name == "quit_button":
                         gameStart = False



############################################################################
############################################################################

#Load Encounter
def load_encounter():

    global gameFps, objToAnimate, objToManage, cam, currentStage, chrList, tileSet, borders, teams, drawList, objOfUi, previousScreen

    animations.update_fps(gameFps)

    # first time we arrive on this screen
    objOfUi = []

    # we need to load everything right?
    '''
    1.add characters to chrList
    2.load stage
    3.load character animations
    4.add characters to manager and animator
    5.1 load the map <---
    5.move characters to spawn locations
    6.countdown battle
    '''
    # set the proper fps tick
    gameFps = fps
    # clear old slates
    objToManage = []
    objToAnimate = []
    # center camera
    cam.x = currentStage['camera_spawn'][0]
    cam.y = currentStage['camera_spawn'][1]
    cam.z = currentStage['camera_spawn'][2]
    # loading the characters
    for chr in chrList:
        load_thread = functions.loadThread(1, "Load-Thread", animations.animations[chrList[chr].stats.chrClass],
                                           currentStage)
        load_thread.start()
        # check to see if our threads have loaded
        while load_thread.loaded == False:
            load_animation()
        objToAnimate.append(chrList[chr])
        objToManage.append(chrList[chr])
    screen = "combat"
    previousScreen = "combat"
    # setting up the map
    tileSet = currentStage['map']['tile_set']
    borders = tile_map.borders_2d(tileSet)
    # spawning the characters
    teams = return_teams(chrList)
    spawn_locations = currentStage['spawns']
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
                chrList[chr].spriteObject.x = slots_assigned[team][0]
                chrList[chr].spriteObject.y = slots_assigned[team][1]
    # transition into combat
    # functions.updateBorders(borders)
    # Add Stuff to Render
    drawList = []
    drawList.append(chrList["tank"].spriteObject)
    drawList.append(chrList["dummy"].spriteObject)
    drawList.extend(tileSet)
    combat_ui_manager.battle_start_trigger(gameFps*2)



############################################################################
############################################################################



def game_mechanics():
    global tileSet, chrList, players, borders, objToManage, objToAnimate, drawList, cam, borders, s, currentStage, uiBatch, window_w, window_h, teams, batchedItems
    # update tiles
    tile_map.update_tile_set(tileSet)
    # Update Sprite Locations on Grid Pos
    tile_map.update_sprite_tiles(tileSet, chrList, players)
    # Update Tile Effects
    tile_map.update_tile_effects(tileSet, chrList)

    # update borders
    functions.updateBorders(borders)

    # what to update actions for
    actions_manager.action_manager(objToManage, chrList)
    # What to animate
    animator.animationManager(objToAnimate, chrList)

    # update the basic mechanics
    basic_game_mechanics.update_basic_mechanics(chrList)

    # Render Options
    renderer.flat_render(drawList, cam, borders, currentStage, chrList, worldBatch, backgroundBatch, window_w, window_h, batchedItems)
    # renderer.render3D(drawList, cam, s)

    #######OVERLAY UIS

    # Draw UIs below renderer because renderer clears our screen
    #combat_ui_manager.draw_combat_UI(s, uiBatch, window_w, window_h, chrList, players, teams)



#Main Game Function

def run_game():

    global screen, previousScreen, objOfUi, event

    # fps at top of engine
    #pyglet.clock.tick()
    #t.tick(gameFps)
    #print(t.get_fps())
    animations.update_fps(t.get_fps())

    #this handles pygame dying
    #event = pygame.event.poll()
    #if event.type == pygame.QUIT:
    #    run = False

    #What to run on title screen
    if screen == "title":

        if previousScreen != "title":


            #first time we arrive on this screen
            objOfUi = []
            previousScreen = "title"

            #add all the buttons and stuff
            objOfUi = screen_layouts.return_screen_elements('title_screen')

            stage_manager.set_bgm('Stage_Assets/bgm/The Last Encounter Collection/TLE INTERLUDE A-STANDALONE LOOP.wav')
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)

        else:

            title_screen()

    #What to run if screen is combat
    if screen == "combat":

        #first time on this screen
        if previousScreen != "combat":
            load_encounter()

        win_con = win_conditions(['eliminate'])

        if win_con == False:

            #Controls
            #key press events
            #controls.keyPress3D(chrList, cam)
            stage_manager.music_stage(currentStage, 0)
            for player in players:
                if players[player]['control_type'] == 'keyboard':
                    controls.main_controls_2d(chrList, borders, cam, players, player)

        elif win_con == True:
            finish = stage_manager.music_stage(currentStage, 1)
            for player in players:
                if players[player]['control_type'] == 'keyboard':
                    controls.main_controls_2d(chrList, borders, cam, players, player)
            #battle end animations before leaving
            if finish == False:
                pass
            elif finish == True:
                change_screen('title')

        # start combat
        game_mechanics()

        if combat_ui_manager.start_trigger == True:
            combat_ui_manager.start_trigger = False
            #combat_ui_manager.battle_Start_Animation(worldBatch, generic_screen, "BATTLE START", window_w, window_h)
            for chr in chrList:
                chrList[chr].stats.canMove = True

    elif screen =='load':
        pygame.time.delay(fps)
        if previousScreen != "load":
            previousScreen = "load"
            pygame.mixer.stop()
            functions.clear_caches()
            loadScreenElements = screen_layouts.return_screen_elements('loadingBatch')
        elif previousScreen == "load":
            load_screen()
    #failsaif
    elif screen == '' or screen == None:
        screen = 'load'
        change_screen('title')



############################################################################
############################################################################



class main(pyglet.window.Window):

    def __init__ (self):
        super(main, self).__init__(window_w, window_h, fullscreen=False, vsync=False)

        self.running = True



    def on_draw(self):
        self.flip()
        pass



    def render(self):

        self.clear()

        if screen == "combat":
            backgroundBatch.draw()
            worldBatch.draw()
        else:
            worldBatch.draw()
        uiBatch.draw()

        self.flip()

        for index in list(batchedItems):
            batchedItems[index].delete()
            del (batchedItems[index])



    def run(self):
        #time.sleep(1 / (fps + 30))

        #dt = pyglet.clock.tick()
        #print(pyglet.clock.get_fps())

        event = None

        self.render()

        run_game()



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



############################################################################
############################################################################

#Create Game Object
gameObj = main()



#Start the Game
def update(dt):
    #print(1/dt)
    gameObj.run()


    
pyglet.clock.schedule_interval(update, 1/fps)
pyglet.app.run()