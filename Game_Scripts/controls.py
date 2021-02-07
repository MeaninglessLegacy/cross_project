########################################################################################################################
########################################################################################################################

from configuration import controls
from global_variables import keysPressed
from Game_Scripts import animator, character_skills, actions_manager


########################################################################################################################
########################################################################################################################


def find_sc(chrList):
    """
    finds the first instance of a selected character from the character list
    -why does this exist?
    :param chrList:
    :return:
    """
    for key in chrList:
        if chrList[key].isSelected:
            return key



def change_sc(players, player_key, o, chrList):
    """
    changes the selected character of a player to the parameter o

    change this - currently sets selected character then retroactively goes through all characters and ones that are
    not selected are set not selected by players. watch out because two players can select the same character at once
    so we can't just deselect the character first since it might affect any player

    :param players: the dictionary containing all players
    :param player_key: the key of the player changing their selected character
    :param o: the key of the player character to change to
    :param chrList: the dictionary of all characters
    :return:
    """

    k = ""

    player = players[player_key]

    for key in chrList:
        if chrList[key] == o:
            k=key
            chrList[key].isSelected = True
            player.sC = chrList[key]
            break

    #set all characters not selected by players to not selected
    player_chr = {}
    for ply in players:
        if players[ply].sC != None:
            player_chr[players[ply].sC] = players[ply].sC

    for key in chrList:
        if key != k and not chrList[key] in player_chr:
            chrList[key].isSelected = False



def find_player(players, character):
    """
    returns the player object from the player list based on a character
    :param players: the list of players
    :param character: the character we want to find the player of
    :return:
    """
    for ply in players:
        if players[ply].sC != None:
            if players[ply].sC == character:
                return players[ply]

    return None



########################################################################################################################
########################################################################################################################

def keybinding_checker(player):
    try:
        controls[player]
    except:
        return None
    else:
        return controls[player]



########################################################################################################################
########################################################################################################################

def use_ability(p, keyBindings, character, players, player, ability, cd):
    """
    when called this attempts to execute the ability for a player's selected character based on the keys that are
    pressed and the keybindings
    :param p: a dictionary containing all the keys pressed
    :param keyBindings: a dictionary of keybindings
    :param character: a character object defined in characters_and_sprites.py
    :param players: a list of players
    :param player: a key of the player in players should be a string
    :param ability: a key that identifies which ability to use
    :param cd: a key that identifies which cooldown to use
    :return:
    """
    if not p[keyBindings['left']] and not p[keyBindings['right']] and not p[keyBindings['up']] and not p[keyBindings['down']]:
        for i, o in enumerate(character.stats.previous_action):
            if isinstance(o, actions_manager.walk_action):
                del character.stats.previous_action[i]
    if p[keyBindings[ability]] and character_skills.check_held_skill(character, ability)['type'] == False:
        animator.removeAnimation(character, character.spriteObject.animationSet['combat_walk'])
        skill = character_skills.use_skill(character, ability, players[player])
        if skill != False:
            players[player].ability_cd[cd] = skill[0]
    # if the ability is a held type ability
    if p[keyBindings[ability]] and character_skills.check_held_skill(character, ability)['type'] == True:
        if players[player].abilities_held[cd] == False:
            animator.removeAnimation(character, character.spriteObject.animationSet['combat_walk'])
            players[player].abilities_held[cd] = True
            skill = character_skills.use_skill(character, ability, players[player])



def execute_controls(chrList, players, player):
    """
    the logic that should be run each frame whenever buttons are pressed
    :param chrList: a dictionary of all characters
    :param borders: the borders of the
    :param cam:
    :param players:
    :param player:
    :return:
    """
    # Return keys pressed
    p = keysPressed

    character = players[player].sC
    keyBindings = keybinding_checker(players[player].player)

    # cds
    ability_1_cd = players[player].ability_cd['1']
    ability_2_cd = players[player].ability_cd['2']
    ability_3_cd = players[player].ability_cd['3']
    ability_4_cd = players[player].ability_cd['4']
    sdebounce = players[player].ability_cd['chr_swap']

    if not character == None and keyBindings != None:

        # set walkspeed
        walkspeed = character.stats.walkspeed*character.stats.rate
        if p[keyBindings['left']] == False and p[keyBindings['right']] == False and p[keyBindings['up']] == False and p[keyBindings['down']] == False and p[keyBindings['ability1']] == False and p[keyBindings['ability2']] == False:
            # Remove Walk Animations
            action = actions_manager.idle_action(
                type='idle',
                animation=character.spriteObject.animationSet['combat_idle'],
                frames=0,
                priority=0,
            )
            has_idle = False
            for test_action in character.stats.queued_actions:
                if isinstance(test_action, actions_manager.idle_action):
                    has_idle = True
            if has_idle == False:
                actions_manager.add_action(character, action)
            animator.addAnimation(character, character.spriteObject.animationSet['combat_idle'])
            animator.removeAnimation(character, character.spriteObject.animationSet['combat_walk'])

        action = None
        # Walk Key Bindings
        if character.stats.canMove == True:
            if p[keyBindings['left']] and p[keyBindings['up']] and not p[keyBindings['down']] and not p[keyBindings['right']]:
                animator.removeAnimation(character, character.spriteObject.animationSet['combat_recover'])
                action = actions_manager.walk_action(
                    type = 'walk',
                    animation = character.spriteObject.animationSet['combat_walk'],
                    frames = 0,
                    priority = 1,
                    direction = 'northwest',
                    walkspeed = walkspeed,
                )
                actions_manager.add_action(character, action)
            if p[keyBindings['right']] and p[keyBindings['up']] and not p[keyBindings['down']] and not p[keyBindings['left']]:
                animator.removeAnimation(character, character.spriteObject.animationSet['combat_recover'])
                action = actions_manager.walk_action(
                    type='walk',
                    animation=character.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='northeast',
                    walkspeed=walkspeed,
                )
                actions_manager.add_action(character,action)
            if p[keyBindings['left']] and p[keyBindings['down']] and not p[keyBindings['up']] and not p[keyBindings['right']]:
                animator.removeAnimation(character, character.spriteObject.animationSet['combat_recover'])
                action = actions_manager.walk_action(
                    type='walk',
                    animation=character.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='southwest',
                    walkspeed=walkspeed,
                )
                actions_manager.add_action(character, action)
            if p[keyBindings['right']] and p[keyBindings['down']] and not p[keyBindings['up']] and not p[keyBindings['left']]:
                animator.removeAnimation(character, character.spriteObject.animationSet['combat_recover'])
                action = actions_manager.walk_action(
                    type='walk',
                    animation=character.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='southeast',
                    walkspeed=walkspeed,
                )
                actions_manager.add_action(character, action)
            if p[keyBindings['left']] and not p[keyBindings['down']] and not p[keyBindings['up']] and not p[
                    keyBindings['right']]:
                animator.removeAnimation(character, character.spriteObject.animationSet['combat_recover'])
                action = actions_manager.walk_action(
                    type = 'walk',
                    animation = character.spriteObject.animationSet['combat_walk'],
                    frames = 0,
                    priority = 1,
                    direction = 'west',
                    walkspeed = walkspeed,
                )
                actions_manager.add_action(character, action)
            if p[keyBindings['right']] and not p[keyBindings['down']] and not p[keyBindings['up']] and not p[
                keyBindings['left']]:
                animator.removeAnimation(character, character.spriteObject.animationSet['combat_recover'])
                action = actions_manager.walk_action(
                    type='walk',
                    animation=character.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='east',
                    walkspeed=walkspeed,
                )
                actions_manager.add_action(character,action)
            if p[keyBindings['up']] and not p[keyBindings['down']] and not p[keyBindings['left']] and not p[
                keyBindings['right']]:
                animator.removeAnimation(character, character.spriteObject.animationSet['combat_recover'])
                action = actions_manager.walk_action(
                    type='walk',
                    animation=character.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='north',
                    walkspeed=walkspeed,
                )
                actions_manager.add_action(character, action)
            if p[keyBindings['down']] and not p[keyBindings['up']] and not p[keyBindings['left']] and not p[
                keyBindings['right']]:
                animator.removeAnimation(character, character.spriteObject.animationSet['combat_recover'])
                action = actions_manager.walk_action(
                    type='walk',
                    animation=character.spriteObject.animationSet['combat_walk'],
                    frames=0,
                    priority=1,
                    direction='south',
                    walkspeed=walkspeed,
                )
                actions_manager.add_action(character, action)

        # Ability Key Bindings
        # Ability Cooldown worth testing if is better cooling down when the player can't move or not
        # use skills
        if character.stats.canMove == True and character.stats.shielding == False and character.stats.channeling == False:
            # ability 1
            if ability_1_cd == 0:
                # if the ability is a tap type ability
                if (character_skills.check_held_skill(character, 'ability1')) != False:
                    use_ability(p, keyBindings, character, players, player, 'ability1', '1')
            # ability_2
            if ability_2_cd == 0:
                # if the ability is a tap type ability
                if (character_skills.check_held_skill(character, 'ability2')) != False:
                    use_ability(p, keyBindings, character, players, player, 'ability2', '2')
            # ability_3
            if ability_3_cd == 0:
                if (character_skills.check_held_skill(character, 'ability3')) != False:
                    use_ability(p, keyBindings, character, players, player, 'ability3', '3')
            # ability_4
            if ability_4_cd == 0:
                if (character_skills.check_held_skill(character, 'ability4')) != False:
                    use_ability(p, keyBindings, character, players, player, 'ability4', '4')

        # cd reduction
        if ability_1_cd != 0:
            players[player].ability_cd['1'] -= 1
        if ability_2_cd != 0:
            players[player].ability_cd['2'] -= 1
        if ability_3_cd != 0:
            players[player].ability_cd['3'] -= 1
        if ability_4_cd != 0:
            players[player].ability_cd['4'] -= 1

        # toggle held skills
        if(character_skills.check_held_skill(character, 'ability1')) and (character_skills.check_held_skill(character, 'ability2')) and (character_skills.check_held_skill(character, 'ability4')) and (character_skills.check_held_skill(character, 'ability4')):
            # check timers
            if players[player].abilities_held['1'] == True:
                players[player].abilities_held_timers['1'] += 1
            if players[player].abilities_held['2'] == True:
                players[player].abilities_held_timers['2'] += 1
            if players[player].abilities_held['3'] == True:
                players[player].abilities_held_timers['3'] += 1
            if players[player].abilities_held['4'] == True:
                players[player].abilities_held_timers['4'] += 1
            # check release
            if not p[keyBindings['ability1']] and character_skills.check_held_skill(character, 'ability1')['type'] == True:
                if players[player].abilities_held['1'] == True:
                    animator.removeAnimation(character, character.spriteObject.animationSet['combat_walk'])
                    players[player].abilities_held['1'] = False
                    skill = character_skills.use_skill(character, 'ability1', players[player])
                    players[player].ability_cd['1'] = skill[0]
            if not p[keyBindings['ability2']] and character_skills.check_held_skill(character, 'ability2')['type'] == True:
                if players[player].abilities_held['2'] == True:
                    animator.removeAnimation(character, character.spriteObject.animationSet['combat_walk'])
                    players[player].abilities_held['2'] = False
                    skill = character_skills.use_skill(character, 'ability2', players[player])
                    players[player].ability_cd['2'] = skill[0]
            if not p[keyBindings['ability3']] and character_skills.check_held_skill(character, 'ability3')['type'] == True:
                if players[player].abilities_held['3'] == True:
                    animator.removeAnimation(character, character.spriteObject.animationSet['combat_walk'])
                    players[player].abilities_held['3'] = False
                    skill = character_skills.use_skill(character, 'ability3', players[player])
                    players[player].ability_cd['3'] = skill[0]
            if not p[keyBindings['ability4']] and character_skills.check_held_skill(character, 'ability4')['type'] == True:
                if players[player].abilities_held['4'] == True:
                    animator.removeAnimation(character, character.spriteObject.animationSet['combat_walk'])
                    players[player].abilities_held['4'] = False
                    skill = character_skills.use_skill(character, 'ability4', players[player])
                    players[player].ability_cd['4'] = skill[0]

        #if you get knocked out while shielding or holding an ability down or if the character is not shielding but staggered
        if character.stats.knockedOut == True or character.stats.shielding != True and character.stats.canMove == False:
            if character_skills.check_held_skill(character, 'ability1')['type'] == True:
                if players[player].abilities_held['1'] == True:
                    animator.removeAnimation(character, character.spriteObject.animationSet['combat_walk'])
                    players[player].abilities_held['1'] = False
                    skill = character_skills.use_skill(character, 'ability1', players[player])
                    players[player].ability_cd['1'] = skill[0]
            if character_skills.check_held_skill(character, 'ability2')['type'] == True:
                if players[player].abilities_held['2'] == True:
                    animator.removeAnimation(character, character.spriteObject.animationSet['combat_walk'])
                    players[player].abilities_held['2'] = False
                    skill = character_skills.use_skill(character, 'ability2', players[player])
                    players[player].ability_cd['2'] = skill[0]
            if character_skills.check_held_skill(character, 'ability3')['type'] == True:
                if players[player].abilities_held['3'] == True:
                    animator.removeAnimation(character, character.spriteObject.animationSet['combat_walk'])
                    players[player].abilities_held['3'] = False
                    skill = character_skills.use_skill(character, 'ability3', players[player])
                    players[player].ability_cd['3'] = skill[0]
            if character_skills.check_held_skill(character, 'ability4')['type'] == True:
                if players[player].abilities_held['4'] == True:
                    animator.removeAnimation(character, character.spriteObject.animationSet['combat_walk'])
                    players[player].abilities_held['4'] = False
                    skill = character_skills.use_skill(character, 'ability4', players[player])
                    players[player].ability_cd['4'] = skill[0]

    # Swap between characters temp
    if sdebounce == 0 and keyBindings != None:
        if p[keyBindings['changeChr']]:
            players[player].ability_cd['chr_swap'] = 3
            # first we need to draw the area that each object is going to be
            # no of player character
            player_characters = []
            for key in chrList:
                if chrList[key].playerCharacter == True:
                    player_characters.append(chrList[key])

            # change character to next character in dic
            current_chr = character

            for i in range(0, len(player_characters)):
                if current_chr == None:
                    change_sc(players, player, player_characters[0], chrList)
                if player_characters[i] == current_chr and i != len(player_characters) - 1:
                    change_sc(players, player, player_characters[i + 1], chrList)
                    break
                elif player_characters[i] == current_chr and i == len(player_characters) - 1:
                    change_sc(players, player, player_characters[0], chrList)
                    break
    else:
        players[player].ability_cd['chr_swap'] -= 1