############################################################################
############################################################################



import pygame,\
    pyglet

import Game_Scripts.animator,\
    Game_Scripts.actions_manager,\
    Game_Scripts.character_skills

animator = Game_Scripts.animator
action_manager = Game_Scripts.actions_manager
character_skills = Game_Scripts.character_skills



############################################################################
############################################################################



#selected Character
def find_sc(ch):
    for key in ch:
        if ch[key].isSelected:
            return key



def change_sc(players, player_key, o, ch):

    k = ""

    player = players[player_key]

    for key in ch:
        if ch[key] == o:
            k=key
            ch[key].isSelected = True
            player['sC'] = ch[key]

    #get all characters controlled by players
    player_chr = {}
    for ply in players:
        if players[ply]['sC'] != None:
            player_chr[players[ply]['sC']] = players[ply]['sC']

    for key in ch:
        if key != k and not ch[key] in player_chr:
            ch[key].isSelected = False



def find_player(players, chr):

    for ply in players:
        if players[ply]['sC'] != None:
            if players[ply]['sC'] == chr:
                return players[ply]

    return None



############################################################################
############################################################################

#2D Controls

keysPressed = {
    pyglet.window.key.A : False,
    pyglet.window.key.D : False,
    pyglet.window.key.W : False,
    pyglet.window.key.S : False,
    pyglet.window.key.Q : False,
    pyglet.window.key.J : False,
    pyglet.window.key.K : False,
    pyglet.window.key.L : False,
    pyglet.window.key.U : False,
    pyglet.window.key.LEFT : False,
    pyglet.window.key.RIGHT : False,
    pyglet.window.key.UP : False,
    pyglet.window.key.DOWN : False,
    pyglet.window.key.NUM_7 : False,
    pyglet.window.key.NUM_0 : False,
    pyglet.window.key.NUM_1 : False,
    pyglet.window.key.NUM_2 : False,
    pyglet.window.key.NUM_3 : False
}



controls = {
    "player_1" : {
        "left" : pyglet.window.key.A,
        "right" : pyglet.window.key.D,
        "up" : pyglet.window.key.W,
        "down" : pyglet.window.key.S,
        "changeChr" : pyglet.window.key.Q,
        "ability1" : pyglet.window.key.J,
        "ability2" : pyglet.window.key.K,
        "ability3" : pyglet.window.key.L,
        "ability4" : pyglet.window.key.U,
    },
    "player_2" : {
        "left" : pyglet.window.key.LEFT,
        "right" : pyglet.window.key.RIGHT,
        "up" : pyglet.window.key.UP,
        "down" : pyglet.window.key.DOWN,
        "changeChr" : pyglet.window.key.NUM_7,
        "ability1" : pyglet.window.key.NUM_0,
        "ability2" : pyglet.window.key.NUM_1,
        "ability3" : pyglet.window.key.NUM_2,
        "ability4" : pyglet.window.key.NUM_3,
    },
    "controller_1" : {
        "left" : (1,0),
        "right" : (-1,0),
        "up" : (0,1),
        "down" : (0,-1),
        "aleft" : [-1],
        "aright" : [1],
        "aup" : [1],
        "adown" : [-1],
        "changeChr" : pygame.K_y,
        "ability1" : pygame.K_x,
    },
        "cleft" : pygame.K_u,
        "cright" : pygame.K_i,
        "cup" : pygame.K_o,
        "cdown" : pygame.K_p,
        'blank' : (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
}



def keybinding_checker(player):
    try:
        controls[player]
    except:
        return None
    else:
        return controls[player]



############################################################################
############################################################################



#For abilities that are tapped once
def use_ability(p, keyBindings, chr, players, player, ability, cd):
    if not p[keyBindings['left']] and not p[keyBindings['right']] and not p[keyBindings['up']] and not p[keyBindings['down']]:
        for i, o in enumerate(chr.stats.previous_action):
            if isinstance(o, action_manager.walk_action):
                del chr.stats.previous_action[i]
    if p[keyBindings[ability]] and character_skills.check_held_skill(chr, ability)['type'] == False:
        animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_walk'])
        skill = character_skills.use_skill(chr, ability, players[player])
        if skill != False:
            players[player]['ability_cd'][cd] = skill[0]
    # if the ability is a held type ability
    if p[keyBindings[ability]] and character_skills.check_held_skill(chr, ability)['type'] == True:
        if players[player]['abilities_held'][cd] == False:
            animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_walk'])
            players[player]['abilities_held'][cd] = True
            skill = character_skills.use_skill(chr, ability, players[player])



#main control for 2d
def main_controls_2d(ch, borders, cam, players, player):
    #Return keys pressed
    p = keysPressed#pygame.key.get_pressed()

    chr = players[player]['sC']
    keyBindings = keybinding_checker(players[player]['player'])

    #cds
    ability_1_cd = players[player]['ability_cd']['1']
    ability_2_cd = players[player]['ability_cd']['2']
    ability_3_cd = players[player]['ability_cd']['3']
    ability_4_cd = players[player]['ability_cd']['4']
    sdebounce = players[player]['ability_cd']['chr_swap']

    if not chr == None and keyBindings != None:
        # set walkspeed
        walkspeed = chr.stats.walkspeed*chr.stats.rate
        if p[keyBindings['left']] == False and p[keyBindings['right']] == False and p[keyBindings['up']] == False and p[keyBindings['down']] == False and p[keyBindings['ability1']] == False and p[keyBindings['ability2']] == False:
            #Remove Walk Animations
            action = action_manager.idle_action(
                type='idle',
                animation=chr.spriteObject.animationSet['combat_idle'],
                frames=0,
                priority=0,
            )
            has_idle = False
            for test_action in chr.stats.queued_actions:
                if isinstance(test_action, action_manager.idle_action):
                    has_idle = True
            if has_idle == False:
                action_manager.add_action(chr, action)
            animator.addAnimation(chr, chr.spriteObject.animationSet['combat_idle'])
            animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_walk'])

        action = None
        #Walk Key Bindings
        if chr.stats.canMove == True:
            if p[keyBindings['left']] and p[keyBindings['up']] and not p[keyBindings['down']] and not p[keyBindings['right']]:
                animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_recover'])
                action = action_manager.walk_action(
                    type = 'walk',
                    animation = chr.spriteObject.animationSet['combat_walk'],
                    frames = 0,
                    priority = 1,
                    direction = 'northwest',
                    walkspeed = walkspeed,
                    borders = borders,
                )
                action_manager.add_action(chr, action)
            if p[keyBindings['right']] and p[keyBindings['up']] and not p[keyBindings['down']] and not p[keyBindings['left']]:
                animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_recover'])
                action = action_manager.walk_action(
                    type='walk',
                    animation=chr.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='northeast',
                    walkspeed=walkspeed,
                    borders=borders,
                )
                action_manager.add_action(chr,action)
            if p[keyBindings['left']] and p[keyBindings['down']] and not p[keyBindings['up']] and not p[keyBindings['right']]:
                animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_recover'])
                action = action_manager.walk_action(
                    type='walk',
                    animation=chr.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='southwest',
                    walkspeed=walkspeed,
                    borders=borders,
                )
                action_manager.add_action(chr, action)
            if p[keyBindings['right']] and p[keyBindings['down']] and not p[keyBindings['up']] and not p[keyBindings['left']]:
                animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_recover'])
                action = action_manager.walk_action(
                    type='walk',
                    animation=chr.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='southeast',
                    walkspeed=walkspeed,
                    borders=borders,
                )
                action_manager.add_action(chr, action)
            if p[keyBindings['left']] and not p[keyBindings['down']] and not p[keyBindings['up']] and not p[
                    keyBindings['right']]:
                animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_recover'])
                action = action_manager.walk_action(
                    type = 'walk',
                    animation = chr.spriteObject.animationSet['combat_walk'],
                    frames = 0,
                    priority = 1,
                    direction = 'west',
                    walkspeed = walkspeed,
                    borders = borders,
                )
                action_manager.add_action(chr, action)
            if p[keyBindings['right']] and not p[keyBindings['down']] and not p[keyBindings['up']] and not p[
                keyBindings['left']]:
                animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_recover'])
                action = action_manager.walk_action(
                    type='walk',
                    animation=chr.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='east',
                    walkspeed=walkspeed,
                    borders=borders,
                )
                action_manager.add_action(chr,action)
            if p[keyBindings['up']] and not p[keyBindings['down']] and not p[keyBindings['left']] and not p[
                keyBindings['right']]:
                animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_recover'])
                action = action_manager.walk_action(
                    type='walk',
                    animation=chr.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='north',
                    walkspeed=walkspeed,
                    borders=borders,
                )
                action_manager.add_action(chr, action)
            if p[keyBindings['down']] and not p[keyBindings['up']] and not p[keyBindings['left']] and not p[
                keyBindings['right']]:
                animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_recover'])
                action = action_manager.walk_action(
                    type='walk',
                    animation=chr.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='south',
                    walkspeed=walkspeed,
                    borders=borders,
                )
                action_manager.add_action(chr, action)

        #Ability Key Bindings
        #Ability Cooldown worth testing if is better cooling down when the player can't move or not
        #use skills
        if chr.stats.canMove == True and chr.stats.shielding == False and chr.stats.channeling == False:
            #ability 1
            if ability_1_cd == 0:
                #if the ability is a tap type ability
                if (character_skills.check_held_skill(chr, 'ability1')) != False:
                    use_ability(p, keyBindings, chr, players, player, 'ability1', '1')
            #else:
                #players[player]['ability_cd']['1'] -= 1
            #ability_2
            if ability_2_cd == 0:
                #if the ability is a tap type ability
                if (character_skills.check_held_skill(chr, 'ability2')) != False:
                    use_ability(p, keyBindings, chr, players, player, 'ability2', '2')
            #else:
                #players[player]['ability_cd']['2'] -= 1
            # ability_3
            if ability_3_cd == 0:
                if (character_skills.check_held_skill(chr, 'ability3')) != False:
                    use_ability(p, keyBindings, chr, players, player, 'ability3', '3')
            #else:
                #players[player]['ability_cd']['3'] -= 1
            # ability_4
            if ability_4_cd == 0:
                if (character_skills.check_held_skill(chr, 'ability4')) != False:
                    use_ability(p, keyBindings, chr, players, player, 'ability4', '4')
            #else:
                #players[player]['ability_cd']['4'] -= 1

        #cd reduction
        if ability_1_cd != 0:
            players[player]['ability_cd']['1'] -= 1
        if ability_2_cd != 0:
            players[player]['ability_cd']['2'] -= 1
        if ability_3_cd != 0:
            players[player]['ability_cd']['3'] -= 1
        if ability_4_cd != 0:
            players[player]['ability_cd']['4'] -= 1

        #toggle held skills
        if(character_skills.check_held_skill(chr, 'ability1')) != False and (character_skills.check_held_skill(chr, 'ability2')) != False and (character_skills.check_held_skill(chr, 'ability4')) != False and (character_skills.check_held_skill(chr, 'ability4')) != False:
            #check timers
            if players[player]['abilities_held']['1'] == True:
                players[player]['abilities_held_timers']['1'] += 1
            if players[player]['abilities_held']['2'] == True:
                players[player]['abilities_held_timers']['2'] += 1
            if players[player]['abilities_held']['3'] == True:
                players[player]['abilities_held_timers']['3'] += 1
            if players[player]['abilities_held']['4'] == True:
                players[player]['abilities_held_timers']['4'] += 1
            #check release
            if not p[keyBindings['ability1']] and character_skills.check_held_skill(chr, 'ability1')['type'] == True:
                if players[player]['abilities_held']['1'] == True:
                    animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_walk'])
                    players[player]['abilities_held']['1'] = False
                    skill = character_skills.use_skill(chr, 'ability1', players[player])
                    players[player]['ability_cd']['1'] = skill[0]
            if not p[keyBindings['ability2']] and character_skills.check_held_skill(chr, 'ability2')['type'] == True:
                if players[player]['abilities_held']['2'] == True:
                    animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_walk'])
                    players[player]['abilities_held']['2'] = False
                    skill = character_skills.use_skill(chr, 'ability2', players[player])
                    players[player]['ability_cd']['2'] = skill[0]
            if not p[keyBindings['ability3']] and character_skills.check_held_skill(chr, 'ability3')['type'] == True:
                if players[player]['abilities_held']['3'] == True:
                    animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_walk'])
                    players[player]['abilities_held']['3'] = False
                    skill = character_skills.use_skill(chr, 'ability3', players[player])
                    players[player]['ability_cd']['3'] = skill[0]
            if not p[keyBindings['ability4']] and character_skills.check_held_skill(chr, 'ability4')['type'] == True:
                if players[player]['abilities_held']['4'] == True:
                    animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_walk'])
                    players[player]['abilities_held']['4'] = False
                    skill = character_skills.use_skill(chr, 'ability4', players[player])
                    players[player]['ability_cd']['4'] = skill[0]

        #if you get knocked out while shielding or holding an ability down or if the character is not shielding but staggered
        if chr.stats.knockedOut == True or chr.stats.shielding != True and chr.stats.canMove == False:
            if character_skills.check_held_skill(chr, 'ability1')['type'] == True:
                if players[player]['abilities_held']['1'] == True:
                    animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_walk'])
                    players[player]['abilities_held']['1'] = False
                    skill = character_skills.use_skill(chr, 'ability1', players[player])
                    players[player]['ability_cd']['1'] = skill[0]
            if character_skills.check_held_skill(chr, 'ability2')['type'] == True:
                if players[player]['abilities_held']['2'] == True:
                    animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_walk'])
                    players[player]['abilities_held']['2'] = False
                    skill = character_skills.use_skill(chr, 'ability2', players[player])
                    players[player]['ability_cd']['2'] = skill[0]
            if character_skills.check_held_skill(chr, 'ability3')['type'] == True:
                if players[player]['abilities_held']['3'] == True:
                    animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_walk'])
                    players[player]['abilities_held']['3'] = False
                    skill = character_skills.use_skill(chr, 'ability3', players[player])
                    players[player]['ability_cd']['3'] = skill[0]
            if character_skills.check_held_skill(chr, 'ability4')['type'] == True:
                if players[player]['abilities_held']['4'] == True:
                    animator.removeAnimation(chr, chr.spriteObject.animationSet['combat_walk'])
                    players[player]['abilities_held']['4'] = False
                    skill = character_skills.use_skill(chr, 'ability4', players[player])
                    players[player]['ability_cd']['4'] = skill[0]

    # Swap between characters temp
    if sdebounce == 0 and keyBindings != None:
        if p[keyBindings['changeChr']]:
            players[player]['ability_cd']['chr_swap'] = 3
            # first we need to draw the area that each object is going to be
            # no of player character
            player_characters = []
            for key in ch:
                if ch[key].playerCharacter == True:
                    player_characters.append(ch[key])

            # change chr to next chr in dic
            current_chr = chr

            for i in range(0, len(player_characters)):
                if current_chr == None:
                    change_sc(players, player, player_characters[0], ch)
                if player_characters[i] == current_chr and i != len(player_characters) - 1:
                    change_sc(players, player, player_characters[i + 1], ch)
                    break
                elif player_characters[i] == current_chr and i == len(player_characters) - 1:
                    change_sc(players, player, player_characters[0], ch)
                    break
    else:
        players[player]['ability_cd']['chr_swap'] -= 1

############################################################################
############################################################################