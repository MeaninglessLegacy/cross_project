############################################################################
############################################################################

#Basic Game Mechanics

import Game_Scripts.animator, math, Game_Scripts.functions, random

functions = Game_Scripts.functions
animator = Game_Scripts.animator


############################################################################
############################################################################

block_sounds = [
    'Sound_Assets/block_1.wav',
    'Sound_Assets/block_2.wav',
    'Sound_Assets/block_3.wav',
]

############################################################################
############################################################################

#Movement
def moveChr(ch):
    #get momementum
    spr_momentum = ch.stats.momentum
    spr = ch.spriteObject
    #get borders
    border = functions.get_Borders()
    #if we have borders
    if border != [] and spr_momentum != (0,0):

        topCorner = border[0]
        bottomCorner = border[1]

        xMomentum = spr_momentum[0]
        yMomentum = spr_momentum[1]

        #for knockdowns so this doesn't impede on movespeed
        if ch.stats.canMove == False:
            if xMomentum > 1:
                xMomentum = 1
            if yMomentum> 1:
                yMomentum = 1
            if xMomentum < -1:
                xMomentum = -1
            if yMomentum < -1:
                yMomentum = -1
        if len(ch.stats.previous_action) > 0:
            if ch.stats.previous_action[0].type == "meleeAtk":
                if xMomentum > 1.4:
                    xMomentum = 1.4
                if yMomentum > 1.4:
                    yMomentum = 1.4
                if xMomentum < -1.4:
                    xMomentum = -1.4
                if yMomentum < -1.4:
                    yMomentum = -1.4

        #change in pos
        xChange = spr.x + xMomentum
        yChange = spr.y + yMomentum

        if xChange > spr.x:
            if xChange < bottomCorner[0]:
                spr.x += xMomentum
            elif xChange >= bottomCorner[0]:
                spr.x = bottomCorner[0]
        elif xChange < spr.x:
            if xChange > topCorner[0]:
                spr.x += xMomentum
            elif xChange <= topCorner[0]:
                spr.x = topCorner[0]

        if yChange > spr.y:
            if yChange < bottomCorner[1]:
                spr.y += yMomentum
            else:
                spr.y = bottomCorner[1]
        elif yChange < spr.y:
            if yChange > topCorner[1]:
                spr.y += yMomentum
            else:
                spr.y = topCorner[1]

        ch.stats.momentum = (spr_momentum[0]-xMomentum, spr_momentum[1] - yMomentum)

#Damage target
def damageTarget(initiator, target, attack):

    #Attack Stats
    damage = attack.damage
    knockback = attack.knockback

    #targets
    initSpr = initiator.spriteObject
    tarSpr = target.spriteObject
    initStats = initiator.stats
    tarStats = target.stats

    if tarStats.currentHP <= 0:
        return False

    #target stats
    tar_shield = tarStats.shield_strength

    if attack.breakShields == False:
        damage = damage-(damage*tar_shield)

    hit_sound = None

    #return false if target is invincible and don't do anything
    if tarStats.invincible == True:
        return False

    if tarStats.shielding == True:
        hit_sound = functions.get_sound(random.choice(block_sounds))
    else:
        hit_sound = functions.get_sound("Sound_Assets/light_hit_2.wav")


    knockback_modifier = 1

    #damage target
    if tarStats.currentHP - damage < 0: #and tarStats.knockedOut == False:
        knockback_modifier = (80*tarStats.weight/2)/knockback
        tarStats.currentHP = 0
    elif tarStats.knockedOut == False:
        tarStats.currentHP -= damage



    #back to damage mechanics
    knockbackStrength = 0

    #knockback formula 10 is the scaling ratio, so this formula returns pixel / frame knocked back
    if 2*(knockback*knockback_modifier)/tarStats.weight > 0:
        knockbackStrength = math.sqrt(2*(knockback*knockback_modifier)/tarStats.weight)

    #knockback
    if tarStats.current_Tile[0] > initStats.current_Tile[0]:
        #tarSpr.heading = '+'
        #tarSpr.direction = 'east'
        tarStats.momentum = (knockbackStrength, 0)
    elif tarStats.current_Tile[0] < initStats.current_Tile[0]:
        #tarSpr.heading = '-'
        #tarSpr.direction = 'west'
        tarStats.momentum = (-knockbackStrength, 0)
    elif tarStats.current_Tile[0] == initStats.current_Tile[0]:
        if initSpr.heading == '-':
            #tarSpr.heading = '+'
            #tarSpr.direction = 'east'
            tarStats.momentum = (knockbackStrength, 0)
        else:
            #tarSpr.heading = '-'
            #tarSpr.direction = 'west'
            tarStats.momentum = (-knockbackStrength, 0)

    #stagger or knockdown
    #the threshhold force is the force need to knock a unit back 6 units
    #since -> 8^2*mass/2 = threshhold force
    threshhold_force = 64*tarStats.weight/2
    if (knockback*knockback_modifier) > threshhold_force:
        tarStats.canMove = False
        if tarStats.knockedOut == False:
            tarStats.knockedOut = True
            tarStats.stunTimer = math.ceil(knockbackStrength*2.5)
            animator.addAnimation(target, tarSpr.animationSet['combat_knocked_down'])
            if tarStats.current_Tile[0] > initStats.current_Tile[0]:
                tarSpr.heading = '+'
                tarSpr.direction = 'east'
            elif tarStats.current_Tile[0] < initStats.current_Tile[0]:
                tarSpr.heading = '-'
                tarSpr.direction = 'west'
            elif tarStats.current_Tile[0] == initStats.current_Tile[0]:
                if initSpr.heading == '-':
                    tarSpr.heading = '+'
                    tarSpr.direction = 'east'
                else:
                    tarSpr.heading = '-'
                    tarSpr.direction = 'west'
        pass
    else:
        #play sound
        hit_sound.set_volume(0.8)
        hit_sound.play()

        tarStats.canMove = False
        if tarStats.knockedOut == False:
            tarStats.stunTimer = math.ceil(knockbackStrength*2.7)
            if tarStats.shield_strength == 0:
                animator.addAnimation(target, tarSpr.animationSet['combat_stagger'])
            else:
                tarStats.stunTimer = math.ceil(knockbackStrength*2.7)/4

#Stuns
def manageStun(ch):
    #character
    chr = ch
    stats = chr.stats
    spr = chr.spriteObject

    #if is knocked out on the ground
    if stats.knockedOut == True or stats.currentHP <= 0:
        animator.addAnimation(chr, spr.animationSet['combat_knocked_out'])
        animator.removeAnimation(chr, spr.animationSet['combat_recover'])
    else:
        animator.removeAnimation(chr, spr.animationSet['combat_knocked_out'])

    #Very sketchy
    if stats.stunTimer > 0:
        #reduce stun tiemr by one
        stats.stunTimer -= 1
    #zero stun timer
    elif stats.stunTimer <= 0:
        #check if knocked out
        if stats.knockedOut == True and stats.currentHP != 0:
            #if knocked out recover
            stats.knockedOut = False
            stats.stunTimer = math.ceil(((len(spr.animationSet['combat_recover']['frames'])*2))*(spr.animationSet['combat_recover']['delay']*math.fabs(1/chr.stats.rate)))
            if spr.animationSet['combat_stagger'] in spr.animationList or spr.animationSet['combat_knocked_out'] in spr.animationList or spr.animationSet['combat_knocked_down'] in spr.animationList:
                animator.removeAnimation(chr, spr.animationSet['combat_stagger'])
                animator.removeAnimation(chr, spr.animationSet['combat_knocked_out'])
                #clear character
                spr.animationList = []
                stats.previous_action = []
            animator.addAnimation(chr, spr.animationSet['combat_recover'])
        elif stats.knockedOut == True and stats.currentHP == 0:
            stats.knockedOut = True
        #if not knocked out
        elif stats.knockedOut == False:
            #resume normal control
            stats.canMove = True
            if spr.animationSet['combat_stagger'] in spr.animationList or spr.animationSet['combat_knocked_out'] in spr.animationList or spr.animationSet['combat_knocked_down'] in spr.animationList:
                animator.removeAnimation(chr, spr.animationSet['combat_stagger'])
                animator.removeAnimation(chr, spr.animationSet['combat_knocked_out'])
                #clear character
                spr.animationList = []
                stats.previous_action = []


############################################################################
############################################################################

def invincibleFrames(chr):

    stats = chr.stats

    #if invincible frames > 0 or if invincible frames is -1 then the character is invincible
    if stats.invincible_frames > 0 or stats.invincible_frames == -1:
        stats.invincible = True
        #greater than zero remove an invinciblity frame
        if stats.invincible_frames > 0:
            stats.invincible_frames -= 1
    elif stats.invincible_frames == 0:
        stats.invincible = False


############################################################################
############################################################################

#update all the basic mechanics
def updateBasicMechanics(ch):
    for key in ch:
        moveChr(ch[key])
        invincibleFrames(ch[key])
        manageStun(ch[key])
    pass