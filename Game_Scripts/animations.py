############################################################################
############################################################################

# dictionary of animations
# dictionary key for animation = animation set
# .ie "tank" = tank animations
# delay is how many frames pass before next animation is played
# animations with higher priority get played over those with lower
animations = {
    "tank" : {



        # Priority List:
        
        # combat_idle : 0
        # combat_walk : 1
        # combat_basic_attack_1 : 4
        # combat_basic_attack_2 : 4
        # combat_basic_attack_3 : 4
        # combat_basic_attack_4 : 4
        # combat_basic_dash_attack : 4
        # combat_heavy_charge : 4
        # combat_heavy_charged_0 : 4
        # combat_heavy_hit_0 : 4
        # combat_stagger : 5
        # ombat_shield : 6
        # combat_knocked_out : 7
        # combat_recover : 8
        # combat_knocked_down : 9



        # Walk animation
        
        "combat_walk" : {
            "animation_priority" : 1,
            "name" : 'combat_walk',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Walk/0-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Walk/0-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Walk/0-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Walk/0-3.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Walk/0-4.png",
            ],
            "sounds" : {
            },
        },

        # Basic Attack Animations

        "combat_basic_attack_1" : {
            "animation_priority" : 4,
            "name" : 'meleeAtk',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/0-0-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/0-0-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/0-0-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/0-0-3.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/0-0-4.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/0-0-5.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/0-0-6.png",
            ],
            "sounds" : {
                "swing" : {
                    "frame" : 1,
                    "volume" : 1,
                    "source" : "Sound_Assets/melee_2.wav"
                },
                "battle_cry" : {
                    "frame" : 0,
                    "volume" : 1,
                    "source" : "Sound_Assets/female_battlecry_short_4.wav"
                },
            },
        },
        "combat_basic_attack_2" : {
            "animation_priority" : 4,
            "name" : 'meleeAtk',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/1-1-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/1-1-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/1-1-3.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/1-1-4.png",
            ],
            "sounds" : {
                "swing" : {
                    "frame" : 1,
                    "volume" : 1,
                    "source" : "Sound_Assets/melee_3.wav"
                },
                "battle_cry" : {
                    "frame" : 0,
                    "volume" : 0,
                    "source" : "Sound_Assets/female_battlecry_short_4.wav"
                },
            },
        },
        "combat_basic_attack_3" : {
            "animation_priority" : 4,
            "name" : 'meleeAtk',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/3-3-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/3-3-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/3-3-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/3-3-3.png",
            ],
            "sounds" : {
                "swing" : {
                    "frame" : 1,
                    "volume" : 1,
                    "source" : "Sound_Assets/melee_3.wav"
                },
                "battle_cry" : {
                    "frame" : 0,
                    "volume" : 0,
                    "source" : "Sound_Assets/female_battlecry_short_4.wav"
                },
            },
        },
        "combat_basic_attack_4" : {
            "animation_priority" : 4,
            "name" : 'meleeAtk',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/4-00.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/4-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/4-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/4-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/4-3-3.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/4-4-4.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/4-5.png",
            ],
            "sounds" : {
                "swing" : {
                    "frame" : 1,
                    "volume" : 1,
                    "source" : "Sound_Assets/melee_2.wav"
                },
                "battle_cry" : {
                    "frame" : 0,
                    "volume" : 1,
                    "source" : "Sound_Assets/female_battlecry_long_2.wav"
                },
            },
        },

        # Dash Attack Animation

        "combat_basic_attack_dash" : {
            "animation_priority" : 4,
            "name" : 'meleeAtk',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/2-2-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/2-2-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/2-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/2-3.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/2-4.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Basic/2-5.png",
            ],
            "sounds" : {
                "swing" : {
                    "frame" : 1,
                    "volume" : 1,
                    "source" : "Sound_Assets/melee_2.wav"
                },
                "battle_cry" : {
                    "frame" : 0,
                    "volume" : 1,
                    "source" : "Sound_Assets/female_battlecry_short_3.wav"
                },
            },
        },

        # Charged Attack Animations

        "combat_heavy_charge" : {
            "animation_priority" : 4,
            "name" : 'meleeAtk',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/0-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/0-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/0-3.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/0-4.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/0-5.png",
            ],
            "sounds" : {
            },
        },
        "combat_heavy_charged_0" : {
            "animation_priority" : 4,
            "name" : 'meleeAtk',
            "looped" : True,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/1-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/1-1.png",
            ],
            "sounds" : {
            },
        },
        "combat_heavy_hit_0" : {
            "animation_priority" : 4,
            "name" : 'meleeAtk',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/2-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/2-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/2-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/2-3.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/2-4.png",
            ],
            "sounds" : {
                "charged_0" : {
                    "frame" : 0,
                    "volume" : 1,
                    "source" : "Sound_Assets/melee_4.wav"
                },
            },
        },
        "combat_heavy_hit_1" : {
            "animation_priority" : 4,
            "name" : 'meleeAtk',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/2-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/3-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/3-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/3-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Heavy/2-4.png",
            ],
            "sounds" : {
                "charged_1" : {
                    "frame" : 0,
                    "volume" : 1,
                    "source" : "Sound_Assets/melee_4.wav"
                },
            },
        },

        # Rolling Animation

        "combat_roll" : {
            "animation_priority" : 4,
            "name" : 'dash',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Roll/0-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Roll/0-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Roll/0-3.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Roll/0-4.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Roll/0-5.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Roll/0-6.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Roll/0-7.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Roll/0-8.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Roll/0-9.png",
            ],
            "sounds" : {
            },
        },

        # Shielding Animation

        "combat_shield" : {
            "animation_priority" : 6,
            "name" : 'shield',
            "looped" : True,
            "delay" : 1,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Shield/1.png",
            ],
            "sounds" : {
            },
        },

        # Hit Animations

        "combat_stagger" : {
            "animation_priority": 5,
            "name" : 'stagger',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Stagger/0-0.png",
            ],
            "sounds":{
            },
        },
        "combat_knocked_down" : {
            "animation_priority": 9,
            "name" : 'knockedDown',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Knock_Down/0-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Knock_Down/0-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Knock_Down/0-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Knock_Down/0-3.png",
                #"Sprite_Assets/Sprites/Tank_Sprites/Combat_Knock_Down/0-4.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Knock_Down/0-5.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Knock_Down/0-6.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Knock_Down/0-7.png",
            ],
            "sounds" : {
                "hit" : {
                    "frame" : 0,
                    "volume" : 0.4,
                    "source" : "Sound_Assets/heavy_hit_1.wav"
                },
                "hurt" : {
                    "frame" : 0,
                    "volume" : 1,
                    "source" : "Sound_Assets/female_hurt_heavy_4.wav"
                },
            },
        },
        "combat_knocked_out" : {
            "animation_priority": 7,
            "name" : 'knockedOut',
            "looped" : True,
            "delay" : 1,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Knock_Down/0-7.png",
            ],
            "sounds" : {
            },
        },
        "combat_recover" : {
            "animation_priority": 8,
            "name" : 'recover',
            "looped" : False,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Recovery/0-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Recovery/0-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Recovery/0-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Recovery/0-3.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Recovery/0-4.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Recovery/0-5.png",
            ],
            "sounds" : {
            },
        },

        # Idle Animation

        "combat_idle" : {
            "animation_priority": 0,
            "name" : 'idle',
            "looped" : True,
            "delay" : 2,
            "frames" : [
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Idle/0-0.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Idle/0-1.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Idle/0-2.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Idle/0-3.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Idle/0-4.png",
                "Sprite_Assets/Sprites/Tank_Sprites/Combat_Idle/0-5.png",
            ],
            "sounds" : {
            },
        },
    }
}



def returnAnimation(animationSet):
    # check if animations exists
    if not animationSet in animations:
        # This makes sure even if we can't find the file it does not crash the engine.
        print("key error:"+animationSet)
        return(False)
    # return the image in cache
    return animations[animationSet]



############################################################################
############################################################################