############################################################################
############################################################################

#Character Skills

import Game_Scripts.functions

functions = Game_Scripts.functions



############################################################################
############################################################################

#skills

import Game_Scripts.Character_Skills.tank_skills




#import the skills
skills_folder = Game_Scripts.Character_Skills

tank_skills = skills_folder.tank_skills



#put skills into dictionary
#class of chr is called and returns skills
abilities = {
    'tank' : tank_skills,
}



############################################################################
############################################################################

#returns the skills of the character

def return_skills(chr):
    chrClass = chr.stats.chrClass
    if chrClass in abilities:
        return abilities[chrClass]



#Main useSkillFunction
def use_skill(chr, skill, player):
    #return skill set
    skill_set = return_skills(chr)

    #if our skill set exists
    if not skill_set is None:
        #first skill is activated
        if skill == 'ability1':
            #checks to see if the chr has a skill in slot 1
            if hasattr(skill_set, 'ability1') == True:
                #use ability and get cooldown
                cd = skill_set.ability1(chr, player)
                #return cooldown
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