########################################################################################################################
########################################################################################################################

import math

import pygame
import configuration

from imports import *
from global_variables import *



########################################################################################################################
########################################################################################################################

# GAME VARIABLES

fps = configuration.gameFps

window_width = configuration.window_width
window_height = configuration.window_height



########################################################################################################################
########################################################################################################################

# INITIALIZE CACHES OF GLOBAL VARIABLES
# python global variables are only global to each module, thus image cache, sound cache, and ui cache are stored in
# functions, while other caches and lists are stored in init's global variables

players["player_1"] = configuration.player_class(name="player_1", color=(255,255,0))
players["player_2"] = configuration.player_class(name="player_2", color=(70,255,255))

chrList["tank"] = characters_and_sprites.character(
    spriteObject=characters_and_sprites.sprite(
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
    stats = characters_and_sprites.stats(
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
chrList["dummy"] = characters_and_sprites.character(
    spriteObject=characters_and_sprites.sprite(
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
    stats = characters_and_sprites.stats(
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

# render type 3d cam can also be used for 2.5D
cam = renderer.camera_3d(20, -20, 15, 0, 0)


# Map - FIX MAP SIDES
#tileSet = tile_system.tileSet3D(15, 1, 10, 0, 0, -15, 0.5)
tileSet = tile_system.tile_set_2d(20,10,0,0,-15,3)
borders = tile_system.borders_2d(tileSet)

# Stage
currentStage = stage_assets.stages['blank']
#currentStage = stages_list.stages['field_day_1']
#currentStage = stages_list.stages

# CLEAN UP THE VARIABLES BELOW THIS LINE
teams = None



########################################################################################################################
########################################################################################################################

# PYGAME INIT

pygame.init()

pygame.mixer.pre_init(configuration.mixerFrequency,
                      configuration.mixerChannels,
                      configuration.mixerSize)

t = pygame.time.Clock()


# PYGLET INIT

display = pyglet.canvas.get_display()



########################################################################################################################
########################################################################################################################

# ALL THE LOADING SCRIPTS NEEDS TO BE REWRITTEN

# functions switching between screens

def change_screen(new_screen):
    """
    sets the changeScreen global variable to the screen that needs to be changed to and changes the current screen to
    the load screen
    :param new_screen: new screen should be a string variable
    :return:
    """

    global loadTransition, changeScreen, screen

    changeScreen = new_screen

    screen = "load"



def load_animation():
    """
    animates the loading screen - CURRENTLY BROKEN
    :return:
    """

    global loadTransition, loadingBatch, loadScreenElements, delay, screen, changeScreen
    # batchedItems[len(batchedItems)+1] = pyglet.shapes.Rectangle(0, 0, window_width, window_height, color=(0, 0, 0), ba
    # tch=loadingBatch)

    if len(loadScreenElements) > 0:
        for i in range(0, len(loadScreenElements)):
            if loadScreenElements[i].name == 'loading_label':
                if delay == 0:
                    delay = 1
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

            ui_elements.draw_ui_element(loadScreenElements[i], loadingBatch, window_width, window_height)



def load_screen():
    """
    increments the animation timer while on the loading screen - broken along with the load_animation function
    :return:
    """

    global loadTransition, loadingBatch, loadScreenElements, delay, screen, changeScreen

    load_animation()

    if loadTransition <= 5:

        loadTransition += 1

    elif loadTransition > 5:

        loadTransition = 0

        screen = changeScreen



########################################################################################################################
########################################################################################################################

# Game Logic

def return_teams(list_chrs):
    """
    uses a list of characters and separates them into teams
    :param list_chrs: list of characters should contains character objects
    :return:
    """

    teams = {}

    for chr in list_chrs:
        # get team of chr
        team_key = list_chrs[chr].stats.team
        # if the team is already in the list
        if team_key in teams:
            teams[team_key][chr] = list_chrs[chr]
        elif not team_key in teams:
            teams[team_key] = {}
            teams[team_key][chr] = list_chrs[chr]

    return teams



def return_alive_members(teams):
    """
    checks a list of teams for how many members are alive on each team
    :param teams: teams is a dictionary, should be obtained first from the return_teams function
    :return:
    """

    live_count = {}

    for team in teams:
        live_count[team] = 0
        for chr in teams[team]:
            if teams[team][chr].stats.currentHP > 0:
                live_count[team] += 1

    return  live_count



def win_conditions(win_conditions):
    """
    determines if combat should end based on win conditions
    1.eliminate - only one or no teams are remaining
    :param win_conditions: win conditions should be a list of strings that represent each win condition
    :return:
    """

    for i in range(0, len(win_conditions)):
        # the win condition we are checking
        win_condition = win_conditions[i]
        # elimate win condition
        if win_condition == 'eliminate':
            teams = return_teams(chrList)
            alive_members = return_alive_members(teams)
            for team in alive_members:
                if alive_members[team] == 0:
                    return True
    return False



########################################################################################################################
########################################################################################################################

def title_screen():
    """
    gives functionality to the title screen, including how to handle mouse click and hover events
    :return:
    """

    global  objOfUi, worldBatch, chrList, gameStart, mouse_pos

    # we need mouse position
    mouse_pos = mousePos

    # draw animated background and stuff

    # draw ui_stuff
    if len(objOfUi) > 0:

        for i in range(0, len(objOfUi)):
            ui_elements.draw_ui_element(objOfUi[i], uiBatch, batchedItems, window_width, window_height)
            ui_elements.mouse_hover(objOfUi[i], mouse_pos, window_width, window_height)

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



########################################################################################################################
########################################################################################################################

#Load Encounter
def load_encounter():
    """
    load encounter executes in the following order:
    1.add characters to chrList
    2.load stage
    3.load character animations
    4.add characters to manager and animator
    5.1 load the map <---
    5.move characters to spawn locations
    6.countdown battle
    :return:
    """

    global fps,\
        objToAnimate,\
        objToManage,\
        cam,\
        currentStage,\
        chrList,\
        tileSet,\
        borders,\
        teams,\
        drawList,\
        objOfUi,\
        previousScreen

    # first time we arrive on this screen
    objOfUi = []

    # clear old caches
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

    #loading the screen
    screen = "combat"
    previousScreen = "combat"

    # setting up the map
    tileSet = currentStage['map']['tile_set']
    borders = tile_system.borders_2d(tileSet)

    #since global variables are seperate across modules, we need to update borders in game_mechanics.py
    game_mechanics.borders = borders

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
    combat_ui.battle_start_trigger(fps*2)



########################################################################################################################
########################################################################################################################



def run_game_mechanics():
    """
    this is the bulk of the game itself:
    1.creates the tile grid environment that the player interacts with
    2.executes actions inputted by the user
    3.executes queued animations
    4.runs through the combat mechanics
    5.renders the game to the pyglet batches
    :return:
    """

    global tileSet,\
        chrList,\
        players,\
        borders,\
        objToManage,\
        objToAnimate,\
        drawList,\
        cam,\
        currentStage,\
        uiBatch,\
        window_width,\
        window_height,\
        teams,\
        batchedItems

    # update tiles
    tile_system.tileSet = tileSet
    # Update Sprite Locations on Grid Pos
    tile_system.update_sprite_tiles(tileSet, chrList, players)
    # Update Tile Effects
    tile_system.update_tile_effects(tileSet, chrList)

    # what to update actions for
    actions_manager.action_manager(objToManage, chrList)
    # What to animate
    animator.animationManager(objToAnimate, chrList)

    # update the basic mechanics
    game_mechanics.update_basic_mechanics(chrList)

    # Render Options
    renderer.flat_render(drawList,
                         cam,
                         borders,
                         currentStage,
                         chrList,
                         worldBatch,
                         backgroundBatch,
                         window_width,
                         window_height,
                         batchedItems)

    #######OVERLAY UIS

    # Draw UIs below renderer because renderer clears our screen
    #combat_ui.draw_combat_UI(s, uiBatch, window_width, window_height, chrList, players, teams)
    # variable s no longer exists



#Main Game Function

def run_game():
    """
    this tells the game what to do on each screen, for example if it is on the title screen it will run the title screen
    interactions

    this function also is in charge of clearing the caches to free memory whenever loading occurs
    :return:
    """

    global screen, previousScreen, objOfUi, event

    # TITLE SCREEN
    if screen == "title":

        if previousScreen != "title":


            # first time we arrive on this screen
            objOfUi = []
            previousScreen = "title"

            # add all the buttons and stuff
            objOfUi = screen_layouts.return_screen_elements('title_screen')

            stage_manager.set_bgm('Stage_Assets/bgm/The Last Encounter Collection/TLE INTERLUDE A-STANDALONE LOOP.wav')
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)

        else:

            title_screen()

    # COMBAT SCREEN
    if screen == "combat":

        # first time on this screen
        if previousScreen != "combat":
            load_encounter()

        win_con = win_conditions(['eliminate'])

        # What to execute before each frame checking if combat ends
        if win_con == False:

            # Controls
            # key press events
            #controls.keyPress3D(chrList, cam)
            stage_manager.music_stage(currentStage, 0)
            for player in players:
                if players[player].control_type == 'keyboard':
                    controls.execute_controls(chrList, players, player)

        elif win_con == True:
            finish = stage_manager.music_stage(currentStage, 1)
            for player in players:
                if players[player].control_type == 'keyboard':
                    controls.execute_controls(chrList, players, player)
            # battle end animations before leaving
            if finish == False:
                pass
            elif finish == True:
                change_screen('title')

        # execute all the game mechanics
        run_game_mechanics()

        # If the combat just started lets everyone move
        if combat_ui.start_trigger == True:
            combat_ui.start_trigger = False
            #combat_ui.battle_Start_Animation(worldBatch, generic_screen, "BATTLE START", window_width, window_height)
            for chr in chrList:
                chrList[chr].stats.canMove = True

    # LOADING SCREEN
    elif screen =='load':
        if previousScreen != "load":
            #clear the caches in functions
            functions.clear_caches()
            #revert from loading-phase out pygame
            previousScreen = "load"
            pygame.mixer.stop()
            loadScreenElements = screen_layouts.return_screen_elements('loadingBatch')

        elif previousScreen == "load":
            load_screen()

    # FALLBACK
    elif screen == '' or screen == None:
        screen = 'load'
        change_screen('title')



########################################################################################################################
########################################################################################################################



class main(pyglet.window.Window):

    def __init__ (self):
        super(main, self).__init__(window_width, window_height, fullscreen=False, vsync=False)

        self.running = True



    def on_draw(self):
        #self.flip()
        pass



    def render(self):
        """
        clears the window then renders each batch in order of z-index, and then clears the batches to free memory
        :return:
        """

        self.clear()

        if screen == "combat":
            backgroundBatch.draw()
            worldBatch.draw()
        else:
            worldBatch.draw()
        uiBatch.draw()

        #self.flip()

        for index in list(batchedItems):
            batchedItems[index].delete()
            del (batchedItems[index])



    def run(self):
        """
        the main game loop, funny it's 3 lines
        :var event is what kind of event is triggered by pyglet event listeners
        :return:
        """

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



########################################################################################################################
########################################################################################################################

#Create Game Object
gameObj = main()

def update(dt):
    """
    the main game loop
    :param dt: the delay since the last frame
    :return:
    """
    #print(1/dt)
    gameObj.run()

# Start the Game
pyglet.clock.schedule_interval(update, 1/fps)
pyglet.app.run()