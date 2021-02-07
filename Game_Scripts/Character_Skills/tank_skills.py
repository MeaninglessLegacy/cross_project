############################################################################
############################################################################


#Tank Skills
#Skills are called from control no need to call control from here

import math

from Game_Scripts import animator, actions_manager, attack_mapper



############################################################################
############################################################################

#Skills

held_skills = {
    'ability1' : {
        'type' : False,
    },
    'ability2' : {
        'type' : True,
    },
    'ability3' : {
        'type' : False,
    },
    'ability4' : {
        'type' : True,
    },
}



############################################################################
#Tank ability 1#############################################################
############################################################################

#8 frames 2 hits
#hits on frame 2 and 6
#light strike + medium strike


def ability1(chr, player):

    #spr obj
    spr = chr.spriteObject

    #actions
    pAction = None
    action = chr.stats.previous_action
    sprAnimationSet = chr.spriteObject.animationSet
    pAnimation = chr.spriteObject.animationList
    if not action == []:
        pAction = action[0]

    #queue
    qAction = chr.stats.queued_actions



    ####stats
    knB_mod = 1

    # damage
    damage = chr.stats.atk * 0.5

    knockback = 250 * 1 * knB_mod

    #cooldown
    cooldown = math.ceil(((spr.animationSet['combat_basic_attack_1']['delay']+1)*math.fabs(1/chr.stats.rate))*(len(spr.animationSet['combat_basic_attack_1']['frames'])))-1#+(math.fabs(1/chr.stats.rate)))

    # animation to play
    animation = spr.animationSet['combat_basic_attack_1']



    #setting up the attack
    # tiles that are hit
    attack_map = attack_mapper.attack_map(
        center=(1, 0),
        forward=3,
        backwards=1,
        up=3,
        down=3,
        up_forward=2,
        up_backwards=2,
        down_forward=2,
        down_backwards=2,
    )

    #attack action here is changed if is dash attack
    atk_action = actions_manager.melee_action(
        type='meleeAtk',
        animation=animation,
        # total amount of frames is delay frame of each frame * total number of frames
        frames=math.ceil((animation['delay']+1) * math.fabs(1 / chr.stats.rate)) * (len(animation['frames'])),
        priority=2,
        hitframe=6 * math.ceil(animation['delay'] * math.fabs(1 / chr.stats.rate)),
        moveframe=[6 * math.ceil(animation['delay'] * math.fabs(1 / chr.stats.rate))],
        initiator=chr,
        damage=damage,
        momentum=1.5,
        ticks=1,
        attack_map=attack_map,
        knockback=knockback,
        shieldBreaker = False,
    )


    #Logic, first determine if dash attack.
	#dash attack
    if not pAction == None:
        #print(pAction)
        if pAction.type == 'walk':
            knB_mod = 15
            knockback = 250 * 1 * knB_mod #3750N of force
            damage = chr.stats.atk * 0.75
            cooldown = math.ceil((spr.animationSet['combat_basic_attack_dash']['delay']+1) * (2 * math.fabs(1 / chr.stats.rate))) * (len(spr.animationSet['combat_basic_attack_dash']['frames'])) + 8
            animation = spr.animationSet['combat_basic_attack_dash']
            attack_map = attack_mapper.attack_map(
                center=(1, 0),
                forward=4,
                backwards=1,
                up=2,
                down=2,
                up_forward=2,
                up_backwards=2,
                down_forward=2,
                down_backwards=2,
            )
            atk_action = actions_manager.melee_action(
                type='meleeAtk',
                animation=animation,
                # total amount of frames is delay frame of each frame * total number of frames
                frames=math.ceil((animation['delay']+1) * math.fabs(1 / chr.stats.rate)) * (len(animation['frames'])),
                priority=2,
                hitframe=2 * math.ceil((animation['delay']+1) * math.fabs(1 / chr.stats.rate)),
                moveframe=[1 * math.ceil((animation['delay']+1) * math.fabs(1 / chr.stats.rate)), 2 * math.ceil((animation['delay']+1) * math.fabs(1 / chr.stats.rate))],
                initiator=chr,
                damage=damage,
                momentum=4,
                ticks=1,
                attack_map=attack_map,
                knockback=knockback,
                shieldBreaker=False,
            )



    #Determines what the last attack was and continues combo
    #determine animation
    animations = {
        str(spr.animationSet['combat_basic_attack_1']) : 0,
        str(spr.animationSet['combat_basic_attack_2']) : 1,
        str(spr.animationSet['combat_basic_attack_3']): 2,
        str(spr.animationSet['combat_basic_attack_4']): 3,
    }

    #if previous action was a melee attack
    if isinstance(pAction, actions_manager.melee_action) == True:
        #if previous action was one of the basic melee attacks
        if str(pAction.animation) in animations:
            if len(pAnimation) != 0:
                if pAnimation[0] == sprAnimationSet["combat_stagger"]:
                    return cooldown
            key = animations[str(pAction.animation)]
            if key == 0:
                animation = spr.animationSet['combat_basic_attack_2']
                damage = chr.stats.atk*1
                knockback = 250 * 1.25 * knB_mod #312.5N of force
                cooldown = math.ceil(((animation['delay']+1)*math.fabs(1/chr.stats.rate))*(len(animation['frames'])))-1#+(math.fabs(1/chr.stats.rate)))
                #different tiles hit
                attack_map = attack_mapper.attack_map(
                    center=(1, 0),
                    forward=3,
                    backwards=2,
                    up=2,
                    down=2,
                    up_forward=2,
                    up_backwards=1,
                    down_forward=2,
                    down_backwards=1,
                )
            elif key == 1:
                animation = spr.animationSet['combat_basic_attack_3']
                damage = chr.stats.atk * 1.05
                knockback = 250 * 1.25 * knB_mod #312.5N of force
                cooldown = math.ceil(((animation['delay']+1)*math.fabs(1/chr.stats.rate))*(len(animation['frames'])))-1#+(math.fabs(1/chr.stats.rate)))
                # different tiles hit
                attack_map = attack_mapper.attack_map(
                    center=(1, 0),
                    forward=4,
                    backwards=2,
                    up=1,
                    down=1,
                    up_forward=1,
                    up_backwards=1,
                    down_forward=1,
                    down_backwards=1,
                )
            elif key == 2:
                animation = spr.animationSet['combat_basic_attack_4']
                damage = chr.stats.atk * 1.1
                knockback = 7500 * knB_mod #5000N of force
                cooldown = math.ceil(((animation['delay']+1)*math.fabs(1/chr.stats.rate))*(len(animation['frames'])))+14#+(math.fabs(1/chr.stats.rate)))
                # different tiles hit
                attack_map = attack_mapper.attack_map(
                    center=(0, 0),
                    forward=4,
                    backwards=2,
                    up=1,
                    down=1,
                    up_forward=1,
                    up_backwards=1,
                    down_forward=1,
                    down_backwards=1,
                )
                atk_action = actions_manager.melee_action(
                    type='meleeAtk',
                    animation=animation,
                    # total amount of frames is delay frame of each frame * total number of frames
                    frames=math.ceil((animation['delay']+1) * math.fabs(1 / chr.stats.rate)) * (
                            len(animation['frames'])),
                    priority=2,
                    hitframe=3 * math.ceil(animation['delay'] * math.fabs(1 / chr.stats.rate)),
                    moveframe=[4 * math.ceil(animation['delay'] * math.fabs(1 / chr.stats.rate))],
                    initiator=chr,
                    damage=damage,
                    momentum=1.5,
                    ticks=1,
                    attack_map=attack_map,
                    knockback=knockback,
                    shieldBreaker=True,
                )
            elif key == 3:
                animation = spr.animationSet['combat_basic_attack_1']
                cooldown = math.ceil(((animation['delay']+1)*math.fabs(1/chr.stats.rate))*(len(animation['frames'])))-1
                knockback = 250 * 1.5 * knB_mod #312.5N of force
                damage = chr.stats.atk * 0.5
                atk_action = actions_manager.melee_action(
                    type='meleeAtk',
                    animation=animation,
                    # total amount of frames is delay frame of each frame * total number of frames
                    frames=math.ceil((animation['delay']+1) * math.fabs(1 / chr.stats.rate)) * (len(animation['frames'])),
                    priority=2,
                    hitframe=6 * math.ceil(animation['delay'] * math.fabs(1 / chr.stats.rate)),
                    moveframe=[6 * math.ceil(animation['delay'] * math.fabs(1 / chr.stats.rate))],
                    initiator=chr,
                    damage=damage,
                    momentum=1.25,
                    ticks=1,
                    attack_map=attack_map,
                    knockback=knockback,
                    shieldBreaker=False,
                )
            # Remap attack
            if key != 2 and key != 3:
                atk_action = actions_manager.melee_action(
                    type='meleeAtk',
                    animation=animation,
                    # total amount of frames is delay frame of each frame * total number of frames
                    frames=math.ceil((animation['delay']+1) * math.fabs(1 / chr.stats.rate)) * (len(animation['frames'])),
                    priority=2,
                    hitframe=2 * math.ceil(animation['delay'] * math.fabs(1 / chr.stats.rate)),
                    moveframe=[1 * math.ceil(animation['delay'] * math.fabs(1 / chr.stats.rate))],
                    initiator=chr,
                    damage=damage,
                    momentum=1.5,
                    ticks=1,
                    attack_map=attack_map,
                    knockback=knockback,
                    shieldBreaker=False,
                )


    #Is there already an attack action
    #check if there is a melee action
    atkAction = False

    for i in range(0, len(qAction)):
        if qAction[i].type == 'meleeAtk':
            atkAction = True
            return cooldown
            break



    #No attack action then add attack
    #print(pAction)
    #Create a melee attack
    if atkAction == False:
        action = atk_action
        #add action
        actions_manager.add_action(chr, action)

        return cooldown
    
    
    
############################################################################
#Tank ability 1#############################################################
############################################################################


############################################################################
#Tank ability 2#############################################################
############################################################################


#90% block

#10000N Force Threshold


def ability2(chr, player):

    spr = chr.spriteObject

    exempt_actions = []
    for i, o in enumerate(chr.stats.queued_actions):
        if not isinstance(o, actions_manager.walk_action) and not isinstance(o, actions_manager.idle_action):
            exempt_actions.append(o)

    #toggle
    if player.abilities_held['2'] == True and exempt_actions == []:
        spr.animationList = []
        stats = chr.stats
        stats.shield_strength = 0.90
        stats.shielding = True
        stats.weight += 162.5#makes heavy boi hard to knock down --> 64(4 meters^2)*(150kg+162.5kg)/2 --> 10000N Threshold

        animator.addAnimation(chr, spr.animationSet['combat_shield'])

    elif player.abilities_held['2'] == False:
        # this chr's stats
        stats = chr.stats
        stats.shielding = False
        stats.shield_strength = 0
        stats.weight = stats.base_weight

        animator.removeAnimation(chr, spr.animationSet['combat_shield'])

        #held timers
        player.abilities_held_timers['2'] = 0


    return 6 *math.fabs(1/chr.stats.rate)



############################################################################
#Tank ability 2#############################################################
############################################################################



############################################################################
#Tank ability 3#############################################################
############################################################################


#dodge roll

def ability3(chr, player):

    spr = chr.spriteObject
    stats = chr.stats
    direction = chr.spriteObject.direction
    speed = chr.stats.walkspeed

    # queue
    qAction = chr.stats.queued_actions

    animation = spr.animationSet['combat_roll']

    cooldown = math.ceil((animation['delay']+1) * math.fabs(1 / chr.stats.rate)) * len(animation['frames']) + 15

    invince_frames = math.ceil((animation['delay']+1) * math.fabs(1 / chr.stats.rate)) * len(animation['frames'])-8

    dash_action = actions_manager.dash_action(
        type = "dash",
        animation = animation,
        frames = math.ceil((animation['delay']+1) * math.fabs(1 / chr.stats.rate)) * len(animation['frames']),
        priority = 4,
        direction = direction,
        speed = speed,
        moveFrames= [0]
    )
    # Is there already an dash action
    dashAction = False

    for i in range(0, len(qAction)):
        if qAction[i].type == 'dash' or qAction[i].type == 'meleeAtk':
            dashAction = True
            return 1
            break
    if spr.animationSet['combat_basic_attack_1'] in spr.animationList:
        dashAction = True
        return 1

    # No dash action then add dash
    if dashAction == False:
        # add action
        actions_manager.add_action(chr, dash_action)
        #Add invinciblity frames
        stats.invincible_frames += invince_frames
        return cooldown
    
    
    
############################################################################
#Tank ability 3#############################################################
############################################################################



############################################################################
#Tank ability 4#############################################################
############################################################################

#heavy attack

#1-second charge time

#max charge 3-second 300% damage modifier

#Shieldbreaker + Heavyforce


def ability4(chr, player):

    spr = chr.spriteObject
    stats = chr.stats
    cooldown = 1

    exempt_actions = []
    for i, o in enumerate(chr.stats.queued_actions):
        if not isinstance(o, actions_manager.walk_action) and not isinstance(o, actions_manager.idle_action) and not isinstance(o, actions_manager.melee_action):
            exempt_actions.append(o)

    pAction = None
    action = chr.stats.previous_action
    if not action == []:
        pAction = action[0]

    #charge
    if player.abilities_held['4'] == True and exempt_actions == []:

        stats.channeling = True
        #check if skill still needs to be charged
        #timer time is done in frames so make sure to change this if framerate is changed
        animator.addAnimation(chr, spr.animationSet['combat_heavy_charge'])
        animator.addAnimation(chr, spr.animationSet['combat_heavy_charged_0'])

    #strike
    if player.abilities_held['4'] == False:

        stats.channeling = False
        #remove charge animations
        animator.removeAnimation(chr, spr.animationSet['combat_heavy_charge'])
        animator.removeAnimation(chr, spr.animationSet['combat_heavy_charged_0'])
        #release charge
        charge_modifier = (3*player.abilities_held_timers['4']/48)

        #attack based on time charged
        animation = spr.animationSet['combat_heavy_hit_0']
        #if charged more than 1 second do heavy hit
        if player.abilities_held_timers['4'] < 12:
            animation = spr.animationSet['combat_heavy_hit_1']
        elif player.abilities_held_timers['4'] > 48:
            charge_modifier = 3

        #attack stats
        cooldown = math.ceil(
            ((animation['delay'] + 1) * math.fabs(1 / chr.stats.rate)) * (len(animation['frames']))) - 1
        knockback = 250 * 26 * charge_modifier  # 6700N * charge time of force
        damage = chr.stats.atk * charge_modifier
        attack_map = attack_mapper.attack_map(
            center=(1, 0),
            forward=4,
            backwards=1,
            up=2,
            down=2,
            up_forward=2,
            up_backwards=1,
            down_forward=2,
            down_backwards=1,
        )
        atk_action = actions_manager.melee_action(
            type='meleeAtk',
            animation=animation,
            # total amount of frames is delay frame of each frame * total number of frames
            frames=math.ceil((animation['delay'] + 1) * math.fabs(1 / chr.stats.rate)) * (len(animation['frames'])),
            priority=2,
            hitframe=2 * math.ceil(animation['delay'] * math.fabs(1 / chr.stats.rate)),
            moveframe=[2 * math.ceil(animation['delay'] * math.fabs(1 / chr.stats.rate))],
            initiator=chr,
            damage=damage,
            momentum=1.25,
            ticks=1,
            attack_map=attack_map,
            knockback=knockback,
            shieldBreaker=False,
        )

        #case shield break if > 24
        if player.abilities_held_timers['4'] >= 24:
            atk_action.shieldBreaker = True

        #on release we need to stop charge
        if isinstance(pAction, actions_manager.melee_action) == False:
            actions_manager.add_action(chr, atk_action)

        #reset charge timer
        player.abilities_held_timers['4'] = 0

    return cooldown


############################################################################
#Tank ability 1#############################################################
############################################################################