########################################################################################################################
########################################################################################################################

# action manager
# This script queues actions into characters and executes actions

import math

from Game_Scripts import animator, tile_system, attack_mapper



########################################################################################################################
########################################################################################################################

# actions

# each action has it's own class and variables


class idle_action():
    def __init__(self, type, animation, frames, priority):
        self.type = type
        self.animation = animation
        self.frames = frames
        self.current_frame = 1
        self.priority = priority

class walk_action():
    def __init__(self, type, animation, frames, priority, direction, walkspeed):
        self.type = type
        self.animation = animation
        self.frames = frames
        self.current_frame = 1
        self.priority = priority
        self.direction = direction
        self.walkspeed = walkspeed

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



########################################################################################################################
########################################################################################################################

def add_action(character, action):
    """
    adds an action action which are defined in actions_manager.py
    :param character: character should be a character object defined in characters_and_sprites.py
    :param action: any action defined in actions_manager.py
    :return:
    """

    # Chr exists
    if not character is None:
        character.stats.queued_actions.append(action)



def action_player(action, character):
    """
    executes an action for a character, actions are defined in actions_manager.py, contains the logic for each of the 
    actions defined in actions_manager.py
    :param action: action object, class defined in actions_manager.py
    :param character: character object, class defined in characters_and_sprites.py
    :return:
    """

    # Precaution
    if character != None:

        if action != None:

            # remove if frames is 0
            if action.current_frame < action.frames:
                action.current_frame  += 1
            elif action.current_frame  >= action.frames:
                if action in character.stats.queued_actions:
                    character.stats.queued_actions.remove(action)
                # clear all movementcommands if last command was an attack
            # Walk Action
            if action.type == 'walk' and character.stats.canMove == True and character.stats.shielding == False and character.stats.channeling == False:
                # character spr
                spr = character.spriteObject
                # set walkspeed
                walkspeed = action.walkspeed
                # Directions
                if action.direction == 'east':
                    character.stats.momentum = (character.stats.momentum[0]-walkspeed, character.stats.momentum[1])
                    spr.heading = "+"
                    spr.direction = "east"
                elif action.direction == 'west':
                    character.stats.momentum = (character.stats.momentum[0]+walkspeed, character.stats.momentum[1])
                    spr.heading = "-"
                    spr.direction = "west"
                elif action.direction == 'north':
                    character.stats.momentum  = (character.stats.momentum[0], character.stats.momentum[1]-walkspeed)
                    spr.direction = "north"
                elif action.direction == 'south':
                    character.stats.momentum  = (character.stats.momentum[0], character.stats.momentum[1]+walkspeed)
                    spr.direction = "south"
                elif action.direction == 'northwest':
                    character.stats.momentum  = (character.stats.momentum[0]+walkspeed/math.sqrt(2), character.stats.momentum[1]-walkspeed/math.sqrt(2))
                    spr.heading = "-"
                    spr.direction = "west"
                elif action.direction == 'northeast':
                    character.stats.momentum  = (character.stats.momentum[0]-walkspeed/math.sqrt(2), character.stats.momentum[1]-walkspeed/math.sqrt(2))
                    spr.heading = "+"
                    spr.direction = "east"
                elif action.direction == 'southwest':
                    character.stats.momentum  = (character.stats.momentum[0]+walkspeed/math.sqrt(2), character.stats.momentum[1]+walkspeed/math.sqrt(2))
                    spr.heading = "-"
                    spr.direction = "west"
                elif action.direction == 'southeast':
                    character.stats.momentum  = (character.stats.momentum[0]-walkspeed/math.sqrt(2), character.stats.momentum[1]+walkspeed/math.sqrt(2))
                    spr.heading = "+"
                    spr.direction = "east"
                # animate
                animator.addAnimation(character, action.animation)
            # Dash action
            # if stunned out of dash
            if action.type == 'dash' and character.stats.canMove == False:
                action.current_frame = action.frames
            # if dash is okay
            if action.type == 'dash' and character.stats.canMove == True and character.stats.shielding == False and character.stats.channeling == False:
                # character spr
                spr = character.spriteObject
                # set dash speed
                speed = action.speed
                # move frames
                moveFrames = action.moveFrames
                if action.current_frame <= 2:
                    animator.addAnimation(character, action.animation)

                if action.current_frame in moveFrames or moveFrames == [0]:
                    # Directions
                    if action.direction == 'east':
                        character.stats.momentum = (character.stats.momentum[0]-speed, character.stats.momentum[1])
                        spr.heading = "+"
                        spr.direction = "east"
                    elif action.direction == 'west':
                        character.stats.momentum = (character.stats.momentum[0]+speed, character.stats.momentum[1])
                        spr.heading = "-"
                        spr.direction = "west"
                    elif action.direction == 'north':
                        character.stats.momentum  = (character.stats.momentum[0], character.stats.momentum[1]-speed)
                        spr.direction = "north"
                    elif action.direction == 'south':
                        character.stats.momentum  = (character.stats.momentum[0], character.stats.momentum[1]+speed)
                        spr.direction = "south"
                    elif action.direction == 'northwest':
                        character.stats.momentum  = (character.stats.momentum[0]+speed/math.sqrt(2), character.stats.momentum[1]+speed/math.sqrt(2))
                        spr.heading = "-"
                        spr.direction = "west"
                    elif action.direction == 'northeast':
                        character.stats.momentum  = (character.stats.momentum[0]-speed/math.sqrt(2), character.stats.momentum[1]+speed/math.sqrt(2))
                        spr.heading = "+"
                        spr.direction = "east"
                    elif action.direction == 'southwest':
                        character.stats.momentum  = (character.stats.momentum[0]+speed/math.sqrt(2), character.stats.momentum[1]-speed/math.sqrt(2))
                        spr.heading = "-"
                        spr.direction = "west"
                    elif action.direction == 'southeast':
                        character.stats.momentum  = (character.stats.momentum[0]-speed/math.sqrt(2), character.stats.momentum[1]-speed/math.sqrt(2))
                        spr.heading = "+"
                        spr.direction = "east"
                # previous action
                character.stats.previous_action = []
                character.stats.previous_action.append(action)
            # melee attack action test
            if action.type == 'meleeAtk' and character.stats.canMove == True:

                # stats
                spr = character.spriteObject
                hitframe = action.hitframe
                moveframe = action.moveframe
                forward_momentum = action.momentum

                # moveforward
                if action.current_frame <= 2:
                    animator.addAnimation(character, action.animation)
                if action.current_frame == hitframe:
                    if spr.heading == '-':
                        hitTiles = attack_mapper.returnTilesHit(character, action.attack_map)
                        #create tiles
                        atk = tile_system.attack(
                            initiator=character,
                            damage=action.damage,
                            ticks=action.ticks,
                            knockback=action.knockback,
                            breakShields=action.shieldBreaker,
                        )
                        for hitTile in hitTiles:
                            tile_system.create_tile_effect(atk, hitTile)
                    elif spr.heading == '+':
                        hitTiles = attack_mapper.returnTilesHit(character, action.attack_map)
                        # create tiles
                        atk = tile_system.attack(
                            initiator=character,
                            damage=action.damage,
                            ticks=action.ticks,
                            knockback=action.knockback,
                            breakShields = action.shieldBreaker,
                        )
                        for hitTile in hitTiles:
                            tile_system.create_tile_effect(atk, hitTile)
                if action.current_frame in moveframe:
                    if spr.heading == '-':
                        character.stats.momentum = (character.stats.momentum[0] + forward_momentum, character.stats.momentum[1])
                    elif spr.heading == '+':
                        character.stats.momentum = (character.stats.momentum[0] - forward_momentum, character.stats.momentum[1])
            # previous action
            #character.stats.previous_action = []
            #character.stats.previous_action.append(action)
            character.stats.previous_action.insert(0, action)



def action_manager(objects_to_manage, ch):
    """
    whenever this is called this executes the logic related to all queued actions for objects, this can be anything
    from running to a barrel exploding
    :param objects_to_manage: this should be an array of all in game objects, for now only characters
    :param ch: this is a list of characters
    :return:
    """

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

        # move highest priority object to current action if priority is greater or current_action is blank
        if len(get_list) > 0:
            # special case for movement
            all_movement_commands = []
            for s in range(0, len(get_list)):
                if hasattr(get_list[s], 'type') == True:
                    if get_list[s].type == 'walk':
                        all_movement_commands.append(get_list[s])
            # execute movement command simultaneously if movemment command is first
            # if len(all_movement_commands) > 0 and get_list[0].type == 'walk':
            #     #north,south,east,west
            #     movement = []
            #     #make sure that only two movement commands can be executed at once
            #     for b in range(0, len(all_movement_commands)-1):
            #         if all_movement_commands[b].direction == 'north':
            #                 movement.insert(0, all_movement_commands[b])
            #         elif all_movement_commands[b].direction == 'south':
            #             if not all_movement_commands[b] in movement:
            #                 movement.insert(0, all_movement_commands[b])
            #         elif all_movement_commands[b].direction == 'east':
            #             if not all_movement_commands[b] in movement:
            #                 movement.insert(1, all_movement_commands[b])
            #         elif all_movement_commands[b].direction == 'west':
            #             if not all_movement_commands[b] in movement:
            #                 movement.insert(1, all_movement_commands[b])
            #     #two movement commands
            #     if len(movement) > 1:
            #         for a in (0, len(movement)-1):
            #             action_player(movement[a], objects_to_manage[i], ch)
            #     #one movement command
            #     elif len(movement) > 0:
            #         action_player(movement[0], objects_to_manage[i], ch)
            #     #zero movement commands
            #     elif len(movement) <= 0:
            #         action_player(get_list[0], objects_to_manage[i], ch)
            # #no movement commands to begin with
            # else:
            action_player(get_list[0], objt)

            # This section was to enable diagonally moving