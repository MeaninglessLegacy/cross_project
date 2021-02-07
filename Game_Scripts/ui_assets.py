########################################################################################################################
########################################################################################################################

# dictionary of ui_assets
# dictionary key for assets
# .ie "tank_healthbar" = tank health bar
assets = {
    "tank" : {
        "combat_healthBar" : {
            "image" : "UI_Assets/healthBars/tank_healthBar.png",
        },
        "portrait" : {
            "image" : "UI_Assets/portraits/tetra_1.png",
        },
    },
    "universal" : {
        "portrait_select" : {
            "image" : "UI_Assets/portraits/selected_generic_2.png",
        },
    }
}


def return_asset(asset):
    """
    returns an object that contains the urls for a specific ui
    :param asset:
    :return:
    """
    # check if asset exists
    if not asset in assets:
        # This makes sure even if we can't find the file it does not crash the engine.
        print("key error:"+asset)
        return(False)
    # return the image in cache
    return assets[asset]


########################################################################################################################
########################################################################################################################