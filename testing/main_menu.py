from ursina import *
from server import Server
import os

Text.default_resolution = 1080 * Text.size

class MainMenu(Entity):
    def __init__(self, player):
        super().__init__(
            
        )

        # starting title banner thing I assume this is before testing
        start_title = Entity(model ="quad", scale = (0.5, 0.2, 0.2), texture = "grass.png", parent = self.start_menu, y = 0.3)

        # will have 2 buttons later but for now hard code to join server or start one if one isnt available
        start_button = Button(text = "JoinGame",color = color.gray, highlight_color = color.light_gray, scale_y = 0.1, scale_x = 0.3, y = -0.08, parent = self.start_meny)


        # quit func to quit the game instead of X button on top right
        def quit():
            application.quit()
            os._exit(0)

        