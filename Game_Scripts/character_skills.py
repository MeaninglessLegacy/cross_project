########################################################################################################################
########################################################################################################################

#Character Skills

########################################################################################################################
########################################################################################################################

#skills

import Game_Scripts.Character_Skills.tank_skills




# import the skills
skills_folder = Game_Scripts.Character_Skills

tank_skills = skills_folder.tank_skills



# put skills into dictionary
# class of chr is called and returns skills
abilities = {
    'tank' : tank_skills,
}



########################################################################################################################
########################################################################################################################

def return_skills(chr):
    """
    takes the character and returns the skills of the character if the characters class if found in the skill imports
    :param chr: character object, defined in characters_and_sprites.py
    :return:
    """
    chrClass = chr.stats.chrClass
    if chrClass in abilities:
        return abilities[chrClass]



def use_skill(chr, skill, player):
    """
    executes a skill for a character
    :param chr: character object, defined in characters_and_sprites.py
    :param skill: the string name of which skill is executed
    :param player: the player that is in global variables
    :return:
    """
    # return skill set
    skill_set = return_skills(chr)

    # if our skill set exists
    if not skill_set is None:
        # first skill is activated
        if skill == 'ability1':
            # checks to see if the chr has a skill in slot 1
            if hasattr(skill_set, 'ability1') == True:
                # use ability and get cooldown
                cd = skill_set.ability1(chr, player)
                # return cooldown
                return  (cd, skill_set.held_skills['ability1'])
                # first skill is activated
        if skill == 'ability2':
            # checks to see if the chr has a skill in slot 2
            if hasattr(skill_set, 'ability2') == True:
                # use ability and get cooldown
                cd = skill_set.ability2(chr, player)
                # return cooldown
                return (cd, skill_set.held_skills['ability2'])
        if skill == 'ability3':
            # checks to see if the chr has a skill in slot 3
            if hasattr(skill_set, 'ability3') == True:
                # use ability and get cooldown
                cd = skill_set.ability3(chr, player)
                # return cooldown
                return (cd, skill_set.held_skills['ability3'])
        if skill == 'ability4':
            # checks to see if the chr has a skill in slot 4
            if hasattr(skill_set, 'ability4') == True:
                # use ability and get cooldown
                cd = skill_set.ability4(chr, player)
                # return cooldown
                return (cd, skill_set.held_skills['ability4'])

    return False



def check_held_skill(chr, skill):
    """
    determines if a certain skills is a held ability or not
    :param chr: the character which is used to get the list of skills from, this is a character object,
    defined in characters_and_sprites.py
    :param skill: the skill name as a string for which skill to check
    :return:
    """
    # return skill set
    skill_set = return_skills(chr)
    # if our skill set exists
    if not skill_set is None:
        # first skill is activated
        if skill == 'ability1':
            # checks to see if the chr has a skill in slot 1
            if 'ability1' in skill_set.held_skills.keys():
                return skill_set.held_skills['ability1']
        if skill == 'ability2':
            if 'ability2' in skill_set.held_skills.keys():
                return skill_set.held_skills['ability2']
        if skill == 'ability3':
            if 'ability3' in skill_set.held_skills.keys():
                return skill_set.held_skills['ability3']
        if skill == 'ability4':
            if 'ability4' in skill_set.held_skills.keys():
                return skill_set.held_skills['ability4']

    return False