########################################################################################################################
########################################################################################################################

import math

from Game_Scripts import functions



########################################################################################################################
########################################################################################################################

# ANIMATIONS

def animationManager(objects_to_animate, ch):
    """
    when this is called it goes through all the objects that need to be animated and decided if the next frame should
    be displayed
    :param objects_to_animate: a list of all objects that need to be animated
    :param ch: a list of all characters
    :return:
    """

    # list of all objects that need to be animated
    objects_to_animate = objects_to_animate

    for i in range(0, len(objects_to_animate)):

        spriteObj = objects_to_animate[i].spriteObject

        if spriteObj.animated == True:

            # list of animations that we want to play
            get_list = spriteObj.animationList

            # if list contains at least one animation
            if len(get_list) > 0:

                sortedObjects = []

                # sorting animations based on priority
                for o in range(0, len(get_list)):

                    if len(sortedObjects) == 0:

                        sortedObjects.append(get_list[o])

                    else:

                        insert_position = 0

                        for s in range(0, len(sortedObjects)):

                            if get_list[o]["animation_priority"] > sortedObjects[s]["animation_priority"]:
                                insert_position += 1

                        sortedObjects.insert(insert_position, get_list[o])

                # invert array
                get_list = list(reversed(sortedObjects))

                # play animation
                animationPlayer(spriteObj, get_list[0], ch)



def animationPlayer(sprite, animation, ch):
    """
    this is the universal function for playing an animation, it advances an animation only after it has reached its
    delay. For example, if an animation has a delay of 5 it will have its animation frame updated every 5 game frames
    :param sprite: the sprite objects that needs to be animated, class is defined in characters_and_sprites.py
    :param animation: the animation that is played for the sprite object, animations can be found in animations.py
    :param ch: a list of characters
    :return:
    """
    # if the character exists
    if not ch[sprite.name] is None:

        chr = ch[sprite.name]
        # make sure that the animation exists
        get_Animation = animation

        if not get_Animation is None:

            get_Frames = get_Animation["frames"]
            looped = get_Animation["looped"]
            name = get_Animation["name"]
            animation_delay = math.ceil(get_Animation["delay"]*math.fabs(1/chr.stats.rate))
            # current delay is how long we have delayed on the character, rate is the speed the chr is at
            current_delay = sprite.animationCounter
            if len(get_Frames) > 1:
                final_frame = (len(get_Frames) - 1)
            else:
                final_frame = 1

            # animate
            if current_delay <= 0:
                # reset delay
                sprite.animationCounter = animation_delay
                # used for picking frame
                frame = 0
                for i in range(0, final_frame):
                    # if the current character's image is the frame then continue animation or we set the animation back to first frame
                    if get_Frames[i] == sprite.imgUrl:
                        frame = i
                        if len(get_Frames) == 1:
                            frame = 0
                        elif frame < (final_frame):
                            # next frame
                            frame += 1
                        # not playing this animation
                        else:
                            frame = 0

                # set frame
                sprite.change_image(get_Frames[frame])

                #play sounds
                sounds = get_Animation['sounds']
                if get_Animation['sounds'] != {}:
                    for sound in sounds:
                        if frame == sounds[sound]['frame']:
                            get_sound = functions.get_sound(sounds[sound]['source'])
                            get_sound.set_volume(sounds[sound]['volume'])
                            get_sound.play()

                # remove animation from list if not looping
                if looped == False and frame == (final_frame):
                    #remove movement commands
                    if name == "meleeAtk" or name == 'dash':
                        chr.stats.queued_actions = [elem for elem in chr.stats.queued_actions if elem.type != 'walk']
                    # remove animation
                    sprite.animationList.remove(animation)
            else:
                # reduce delay
                sprite.animationCounter -= 1



########################################################################################################################
########################################################################################################################

def addAnimation(character, animation):
    """
    adds an animation to the animation queue of a character
    :param character: character object, class defined in characters_and_sprites.py
    :param animation: the animation that is to be added to the queue of the character object
    :return:
    """
    if not animation in character.spriteObject.animationList :
        #add if only not in list
        character.spriteObject.animationList.append(animation)



def removeAnimation(character, animation):
    """
    removes an animation from the queue of a character if it exists in the queue
    :param character: character object, class defined in characters_and_sprites.py
    :param animation: the animation that is to be added to the queue of the character object
    :return:
    """
    if animation in character.spriteObject.animationList :
        #remove if in list
        character.spriteObject.animationList.remove(animation)