############################################################################
############################################################################



#action manager
#This script queues actions into characters and executes actions



import Game_Scripts.animator,\
    Game_Scripts.tileMap,\
    Game_Scripts.functions,\
    Game_Scripts.attack_mapper,\
    Game_Scripts.basic_game_mechanics,\
    math

animator = Game_Scripts.animator
tile_map = Game_Scripts.tileMap
functions = Game_Scripts.functions
attack_mapper = Game_Scripts.attack_mapper
basic_game_mechanics = Game_Scripts.basic_game_mechanics


############################################################################
############################################################################


#actions

#each action has it's own class and variables


class idle_action():
    def __init__(self, type, animation, frames, priority):
        self.type = type
        self.animation = animation
        self.frames = frames
        self.current_frame = 1
        self.priority = priority

class walk_action():
    def __init__(self, type, animation, frames, priority, direction, walkspeed, borders):
        self.type = type
        self.animation = animation
        self.frames = frames
        self.current_frame = 1
        self.priority = priority
        self.direction = direction
        self.walkspeed = walkspeed
        self.borders = borders

class dash_action():
    def __init__(self, type, animation, frames, priority, direction, speed, moveFrames):
        self.type = type
        self.animation = animation
        self.frames = frames
        self.current_frame = 1
        self.priority = priority
        self.direction = direction
        self.speed = speed
        self.moveFrames = moveFrames

class melee_action():
    def __init__(self, type, animation, frames, priority, hitframe, initiator, damage, momentum, ticks, attack_map, knockback, moveframe, shieldBreaker):
        self.type = type
        self.animation = animation
        self.frames = frames
        self.current_frame = 1
        self.priority = priority
        self.hitframe = hitframe
        self.moveframe = moveframe
        self.initiator = initiator
        self.damage = damage
        self.momentum = momentum
        self.ticks = ticks
        self.attack_map = attack_map
        self.knockback = knockback
        self.shieldBreaker = shieldBreaker

############################################################################
############################################################################


#Add action to list
def add_action(chr, action):

    #Chr exists
    if not chr is None:
        chr.stats.queued_actions.append(action)



#execute actions
def action_player(action, chr, ch):
    #Precaution
    if chr != None:

        if action != None:

            # remove if frames is 0
            if action.current_frame < action.frames:
                action.current_frame  += 1
            elif action.current_frame  >= action.frames:
                if action in chr.stats.queued_actions:
                    chr.stats.queued_actions.remove(action)
                #clear all movementcommands if last command was an attack
            #Walk Action
            if action.type == 'walk' and chr.stats.canMove == True and chr.stats.shielding == False and chr.stats.channeling == False:
                #chr spr
                spr = chr.spriteObject
                #set walkspeed
                walkspeed = action.walkspeed
                #map borders
                borders = action.borders
                topCorner = borders[0]
                bottomCorner = borders[1]
                #Directions
                if action.direction == 'east':
                    chr.stats.momentum = (chr.stats.momentum[0]-walkspeed, chr.stats.momentum[1])
                    spr.heading = "+"
                    spr.direction = "east"
                elif action.direction == 'west':
                    chr.stats.momentum = (chr.stats.momentum[0]+walkspeed, chr.stats.momentum[1])
                    spr.heading = "-"
                    spr.direction = "west"
                elif action.direction == 'north':
                    chr.stats.momentum  = (chr.stats.momentum[0], chr.stats.momentum[1]-walkspeed)
                    spr.direction = "north"
                elif action.direction == 'south':
                    chr.stats.momentum  = (chr.stats.momentum[0], chr.stats.momentum[1]+walkspeed)
                    spr.direction = "south"
                elif action.direction == 'northwest':
                    chr.stats.momentum  = (chr.stats.momentum[0]+walkspeed/math.sqrt(2), chr.stats.momentum[1]-walkspeed/math.sqrt(2))
                    spr.heading = "-"
                    spr.direction = "west"
                elif action.direction == 'northeast':
                    chr.stats.momentum  = (chr.stats.momentum[0]-walkspeed/math.sqrt(2), chr.stats.momentum[1]-walkspeed/math.sqrt(2))
                    spr.heading = "+"
                    spr.direction = "east"
                elif action.direction == 'southwest':
                    chr.stats.momentum  = (chr.stats.momentum[0]+walkspeed/math.sqrt(2), chr.stats.momentum[1]+walkspeed/math.sqrt(2))
                    spr.heading = "-"
                    spr.direction = "west"
                elif action.direction == 'southeast':
                    chr.stats.momentum  = (chr.stats.momentum[0]-walkspeed/math.sqrt(2), chr.stats.momentum[1]+walkspeed/math.sqrt(2))
                    spr.heading = "+"
                    spr.direction = "east"
                #animate
                animator.addAnimation(chr, action.animation)
            #Dash action
            #if stunned out of dash
            if action.type == 'dash' and chr.stats.canMove == False:
                action.current_frame = action.frames
            #if dash is okay
            if action.type == 'dash' and chr.stats.canMove == True and chr.stats.shielding == False and chr.stats.channeling == False:
                #chr spr
                spr = chr.spriteObject
                #set dash speed
                speed = action.speed
                #move frames
                moveFrames = action.moveFrames
                if action.current_frame <= 2:
                    animator.addAnimation(chr, action.animation)

                if action.current_frame in moveFrames or moveFrames == [0]:
                    #Directions
                    if action.direction == 'east':
                        chr.stats.momentum = (chr.stats.momentum[0]-speed, chr.stats.momentum[1])
                        spr.heading = "+"
                        spr.direction = "east"
                    elif action.direction == 'west':
                        chr.stats.momentum = (chr.stats.momentum[0]+speed, chr.stats.momentum[1])
                        spr.heading = "-"
                        spr.direction = "west"
                    elif action.direction == 'north':
                        chr.stats.momentum  = (chr.stats.momentum[0], chr.stats.momentum[1]-speed)
                        spr.direction = "north"
                    elif action.direction == 'south':
                        chr.stats.momentum  = (chr.stats.momentum[0], chr.stats.momentum[1]+speed)
                        spr.direction = "south"
                    elif action.direction == 'northwest':
                        chr.stats.momentum  = (chr.stats.momentum[0]+speed/math.sqrt(2), chr.stats.momentum[1]+speed/math.sqrt(2))
                        spr.heading = "-"
                        spr.direction = "west"
                    elif action.direction == 'northeast':
                        chr.stats.momentum  = (chr.stats.momentum[0]-speed/math.sqrt(2), chr.stats.momentum[1]+speed/math.sqrt(2))
                        spr.heading = "+"
                        spr.direction = "east"
                    elif action.direction == 'southwest':
                        chr.stats.momentum  = (chr.stats.momentum[0]+speed/math.sqrt(2), chr.stats.momentum[1]-speed/math.sqrt(2))
                        spr.heading = "-"
                        spr.direction = "west"
                    elif action.direction == 'southeast':
                        chr.stats.momentum  = (chr.stats.momentum[0]-speed/math.sqrt(2), chr.stats.momentum[1]-speed/math.sqrt(2))
                        spr.heading = "+"
                        spr.direction = "east"
                # previous action
                chr.stats.previous_action = []
                chr.stats.previous_action.append(action)
            #melee attack action test
            if action.type == 'meleeAtk' and chr.stats.canMove == True:

                #stats
                spr = chr.spriteObject
                hitframe = action.hitframe
                moveframe = action.moveframe
                forward_momentum = action.momentum

                #moveforward
                if action.current_frame <= 2:
                    animator.addAnimation(chr, action.animation)
                if action.current_frame == hitframe:
                    if spr.heading == '-':
                        hitTiles = attack_mapper.returnTilesHit(chr, action.attack_map)
                        #create tiles
                        atk = tile_map.attack(
                            initiator=chr,
                            damage=action.damage,
                            ticks=action.ticks,
                            knockback=action.knockback,
                            breakShields=action.shieldBreaker,
                        )
                        for hitTile in hitTiles:
                            tile_map.create_tile_effect(atk, hitTile)
                    elif spr.heading == '+':
                        hitTiles = attack_mapper.returnTilesHit(chr, action.attack_map)
                        # create tiles
                        atk = tile_map.attack(
                            initiator=chr,
                            damage=action.damage,
                            ticks=action.ticks,
                            knockback=action.knockback,
                            breakShields = action.shieldBreaker,
                        )
                        for hitTile in hitTiles:
                            tile_map.create_tile_effect(atk, hitTile)
                if action.current_frame in moveframe:
                    if spr.heading == '-':
                        chr.stats.momentum = (chr.stats.momentum[0] + forward_momentum, chr.stats.momentum[1])
                    elif spr.heading == '+':
                        chr.stats.momentum = (chr.stats.momentum[0] - forward_momentum, chr.stats.momentum[1])
            #previous action
            #chr.stats.previous_action = []
            #chr.stats.previous_action.append(action)
            chr.stats.previous_action.insert(0, action)



#Execute Actions For all Chrs
def action_manager(objects_to_manage, ch):
    # list of all objects that need to be managed
    objects_to_manage = objects_to_manage

    for objt in objects_to_manage:

        objStats = objt.stats

        # list of actions that we want to play
        get_list = objStats.queued_actions

        # if list contains at least one action
        if len(get_list) > 0:

            sortedObjects = []

            # sorting actions based on priority
            for o in range(0, len(get_list)):

                if len(sortedObjects) == 0:

                    sortedObjects.append(get_list[o])

                else:

                    insert_position = 0

                    for s in range(0, len(sortedObjects)):

                        if get_list[o].priority > sortedObjects[s].priority:
                            insert_position += 1

                    sortedObjects.insert(insert_position, get_list[o])

            # invert array
            get_list = list(reversed(sortedObjects))

        #move highest priority object to current action if priority is greater or current_action is blank
        if len(get_list) > 0:
            #special case for movement
            all_movement_commands = []
            for s in range(0, len(get_list)):
                if hasattr(get_list[s], 'type') == True:
                    if get_list[s].type == 'walk':
                        all_movement_commands.append(get_list[s])
            #execute movement command simultaneously if movemment command is first
            '''if len(all_movement_commands) > 0 and get_list[0].type == 'walk':
                #north,south,east,west
                movement = []
                #make sure that only two movement commands can be executed at once
                for b in range(0, len(all_movement_commands)-1):
                    if all_movement_commands[b].direction == 'north':
                            movement.insert(0, all_movement_commands[b])
                    elif all_movement_commands[b].direction == 'south':
                        if not all_movement_commands[b] in movement:
                            movement.insert(0, all_movement_commands[b])
                    elif all_movement_commands[b].direction == 'east':
                        if not all_movement_commands[b] in movement:
                            movement.insert(1, all_movement_commands[b])
                    elif all_movement_commands[b].direction == 'west':
                        if not all_movement_commands[b] in movement:
                            movement.insert(1, all_movement_commands[b])
                #two movement commands
                if len(movement) > 1:
                    for a in (0, len(movement)-1):
                        action_player(movement[a], objects_to_manage[i], ch)
                #one movement command
                elif len(movement) > 0:
                    action_player(movement[0], objects_to_manage[i], ch)
                #zero movement commands
                elif len(movement) <= 0:
                    action_player(get_list[0], objects_to_manage[i], ch)
            #no movement commands to begin with
            else:'''
            action_player(get_list[0], objt, ch)

            #This section was to enable diagonally moving