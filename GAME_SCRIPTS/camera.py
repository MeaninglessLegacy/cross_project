########################################################################################################################
########################################################################################################################


# CAMERA FILE
# This file includes the definition for the camera object and the functions to move the camera


########################################################################################################################
########################################################################################################################

# DEFINITIONS

class Camera:
    def __init__(self,
                 position=(0, 0, 0),
                 rotation=(0, 0)):
        """
        Creates a camera object

        :param position: tuple
            a x,y,z tuple of the camera's position in world space
        :param rotation: tuple
            a x,y tuple of the camera's x rotation and y rotation
        """
        self.position = position
        self.rotation = rotation
