from ursina import *
from testPlayer import Player
from multiplayer import Multiplayer
import main_menu

# started script cant complete till other scripts are done
# testplayer - partially complete needs custom camera instead of FPC because it bugs otherwise
# multiplayer - Done
# main menu - Done? havent been able to test everything but it runs well so far

# cant be tested without all the scripts or I would have one large script

#creating a window to see the game
app = Ursina()
window.title = "Goofy Racers"

ply = Player()

main_menu = main_menu.MainMenu(ply)

Sky()

def update():
    # if multiplayer call multiplayer class
    if ply.multiplayer:
        global multiplayer
        multiplayer = Multiplayer(ply)
        Player.multiplayer_update = True
        Player.multiplayer = False
    
    if ply.multiplayer_update:
        if multiplayer.client.connected:
            if ply.connected_text:
                main_menu.connected.enable()
                ply.connected_text = False
            else:
                invoke(main_menu.connected.disable, delay = 2)
            main_menu.not_connected.disable()
        else:
            if ply.disconnected_text:
                main_menu.not_connected.enable()
                ply.disconnected_text = False
            else:
                invoke(main_menu.not_connected.disable, delay = 2)
            main_menu.connected.disable()

    if ply.multiplayer_running:
        ply.server.update_server()
        if ply.server.server_update:
            ply.server.easy.process_net_events()

    
def input(key):

    if ply.multiplayer_update:
        multiplayer.client.send_message("MyPosition", tuple(ply.position))
        multiplayer.client.send_message("MyRotation", tuple(ply.rotation))
        multiplayer.client.send_message("MyTexture", str(ply.texture))

        multiplayer.client.send_message("MyModel", str(ply.model_path))

app.run()