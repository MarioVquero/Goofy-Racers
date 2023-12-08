from ursina import *
from testPlayer import Player
from multiplayer import Multiplayer

# started script cant complete till other scripts are done
# testplayer - Done
# multiplayer - Done
# main menu - started

# cant be tested without all the scripts or I would have one large script

#creating a window to see the game
app = Ursina()
window.title = "Goofy Racers"

Sky()


player = Player()



def update():
    # if multiplayer call multiplayer class
    pass

