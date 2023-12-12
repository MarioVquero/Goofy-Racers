from ursinanetworking import *
from ursina import Entity, Vec3, color,destroy
from ursina.prefabs.first_person_controller import FirstPersonController

# have to make a camera because FirstPersonController bugs out the whole thing

# the player class that has all the default values
class Player(FirstPersonController):
    def __init__(self, position = (0,0,0), rotation = (0,0,0)):
        super().__init__(
            model = "cube",
            texture = "grass.png",
            collider = "box",
            position = position,
            rotation = rotation
        )

        # multiplayer bools
        self.multiplayer = False
        self.multiplayer_update = False
        self.multiplayer_running = False

        # show if youre connected to a server or not
        self.connected_text = True
        self.disconnected_test = False


# class to copy and update the players position and rotation for multiplayer
class  PlayerRep(Entity):
    def __init__(self, player, position = (0,0,0), rotation = (0,0,0)):
        super().__init__(
            parent = scene,
            model = "cube",
            texture = "grass.png",
            collider = "box",
            position = position,
            rotation = rotation,
            scale = (1,1,1)
        )


