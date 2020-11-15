############################################################################
############################################################################

import Game_Scripts.tileMap

tileMapper = Game_Scripts.tileMap

#dictionary of stages
#dictionary key for assets
#.ie "dusk_city_roof_1 = stage of dusk city roof
stages = {
    "bridge_1" : {
        "background": {
            "visible" : True,
            "img" : 'Stage_Assets/backgrounds/sunset_4.png',
            "position" : None,
            "scale" : (1,1),
        },
        "middle_ground": {
            "visible" : False,
            "img" : None,
            "position" : None,
            "scale" : None,
        },
        "stage_floor": {
            "visible" : True,
            "img" : 'Stage_Assets/stage_floors/bridge_2.png',
            "position" : (70,21),
            "scale" : (100,26),
        },
        "on_floor": {
            "visible" : False,
            "img" : None,
            "position" : None,
            "scale" : None,
        },
        "foreground": {
            "visible" : True,
            "img" : 'Stage_Assets/foregrounds/bridge_under_4.png',
            "position" : (70,2),
            "scale" : (100,30),
        },
        "bgm" : {
            "name" : "Final Encounter",
            "volume" : 0.3,
            "fade_in_time" : 50,
            "source" : 'Stage_Assets/bgm/The Last Encounter Collection/TLE Digital Loop Medium.wav',
            #"source" : 'Stage_Assets/bgm/NO_EX01.mp3',
        },
        "map" : {
            'tile_set' : tileMapper.tileSet2D(20,10,0,-2,-15,2),
        },
        "spawns" : [
            (36,8),
            (4,8),
        ],
        "camera_spawn" : (20,-10,15)
    },
    "field_day_1" : {
        "background": {
            "visible" : False,
            "img" : 'Stage_Assets/backgrounds/sky_day_1.png',
            "position" : None,
            "scale" : (1,1),
        },
        "middle_ground": {
            "visible" : False,
            "img" : None,
            "position" : (120,38),
            "scale" : (140,40),
        },
        "stage_floor": {
            "visible" : False,
            "img" : None,
            "position" : (120,3),
            "scale" : (140,30),
        },
        "on_floor": {
            "visible" : False,
            "img" : None,
            "position" : (120,-9),
            "scale" : (140,3),
        },
        "foreground": {
            "visible" : False,
            "img" : None,
            "position" : (70,2),
            "scale" : (100,30),
        },
        "bgm" : {
            "name" : "Heated Battle",
            "volume" : 0.3,
            "fade_in_time" : 50,
            "source" : 'Stage_Assets/bgm/1-15 289 - Heated Battle (Loop).MP3',
            #"source" : 'Stage_Assets/bgm/NO_EX01.mp3',
        },
        "map" : {
            'tile_set' : tileMapper.tileSet2D(40,1,0,-2,-15,2),
        },
        "spawns" : [
            (36,0.5),
            (4,0.5),
        ],
        "camera_spawn" : (36,8,5)
    },
    "blank" : {
        "background": {
            "visible" : False,
            "img" : None,
            "position" : None,
            "scale" : (1,0.6),
        },
        "middle_ground": {
            "visible" : False,
            "img" : None,
            "position" : None,
            "scale" : None,
        },
		"on_floor": {
            "visible" : False,
            "img" : None,
            "position" : None,
            "scale" : None,
        },
        "stage_floor": {
            "visible" : False,
            "img" : None,
            "position" : (700,125),
            "scale" : (1.5,1),
        },
        "foreground": {
            "visible" : False,
            "img" : None,
            "position" : None,
            "scale" : None,
        },
        "bgm" : {
            "name" : "NO.EX01",
            "volume" : 0.2,
            "fade_in_time" : 50,
            "source" : 'Stage_Assets/bgm/NO_EX01.mp3',
        },
        "map" : {
            'tile_set' : tileMapper.tileSet2D(40,3,0,0,-15,2),
        },
        "spawns" : [
            (36,0.5),
            (4,0.5),
        ],
        "camera_spawn" : (20,-50,15)
    }
}

def returnAsset(stage):
    # check if stage exists
    if not stage in stages:
        # This makes sure even if we can't find the file it does not crash the engine.
        print("key error:"+stage)
        return(False)
    # return the stage
    return stages[stage]


############################################################################
############################################################################