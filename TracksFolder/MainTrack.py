from ursina import *

class MainTrack(Entity):
    def __init__(self, player):
        super().__init__(
            model = "UROAD.obj",
            texture = "grass.png",
            position = (0,-10,0),
            rotation = (0,270,0),
            scale = (10,1,10),
            collider = "mesh"
        )

        self.ply = player

        