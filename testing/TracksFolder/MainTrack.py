from ursina import *

class MainTrack(Entity):
    def __init__(self, player):
        super().__init__(
            model = "cube",
            texture = "grass.png",
            position = (0,-2,0),
            rotation = (0,270,0),
            scale = (1000,1,1000),
            collider = "cube"
        )

        self.ply = player

        