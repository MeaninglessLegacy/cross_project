############################################################################
############################################################################

import math,\
    Game_Scripts.functions

functions = Game_Scripts.functions

############################################################################
############################################################################

# ANIMATIONS

"""

        Example of Sprite and Animation

        self.animationSet = animationSet
        self.animationCounter = 0
        self.animationList = []
        self.moving = False
        self.combat = True

        "combat_idle" : {
            "animation_priority": 0,
            "looped" : True,
            "delay" : fps/10,
            "frames" : [
                "../Sprite_Assets/Sprites/Tank_Sprites/Combat_Idle/Tank_Idle_Frame_1.png",
            ]
        }
"""


def animationManager(objects_to_animate, ch):
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


# universal Play Animation
def animationPlayer(sprite, animation, ch):
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


############################################################################
############################################################################



#temp adding and removing animations
def addAnimation(character, animation):

    if not animation in character.spriteObject.animationList :
        #add if only not in list
        character.spriteObject.animationList.append(animation)



def removeAnimation(character, animation):

    if animation in character.spriteObject.animationList :
        #remove if in list
        character.spriteObject.animationList.remove(animation)



############################################################################
############################################################################