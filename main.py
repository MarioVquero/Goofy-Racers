from direct.stdpy import thread
from ursina import *
from testPlayer import Player
from multiplayer import Multiplayer
import main_menu


from TracksFolder.MainTrack import MainTrack

# started script cant complete till other scripts are done
# testplayer - partially complete camera needs a couple of lines to track and move with player but lets UI work now
# multiplayer - Done
# main menu - Almost done server wont start from here but running the server scrip seperately can let you start a server AND trying to connect
# using main.py allows a connection
# at the moment infinite clients are connected for some reason

#creating a window to see the game
app = Ursina()
window.title = "Goofy Racers"



#######################################################################################################################################


                                                    # LOADING ASSETS

def load_assets():
    models_to_load = [
        # cars
        "Low_Poly_Car.obj"
    ]

    textures_to_load = [

    ]

    for i, m in enumerate(models_to_load):
        load_model(m)
    
    for i,t in enumerate(textures_to_load):
        load_model(t)

try:
    thread.start_new_thread(function=load_assets,args="")
except Exception as e:
    print("error starting new thread",e)


#######################################################################################################################################



ply = Player()
ply.player_car()

# Main Track
main_track = MainTrack(ply)

ply.main_track = main_track

main_menu = main_menu.MainMenu(ply, main_track)

Sky()

def update():
    # spacers to make reading prints easier
    print("\nmain.py")
    # if multiplayer call multiplayer class should be default
    if ply.multiplayer:
        print("Multiplayer true")
        global multiplayer
        multiplayer = Multiplayer(ply)
        print(multiplayer)
        ply.multiplayer_update = True
        ply.multiplayer = False

    # Update the multiplayer and check whether the client is connected
    if ply.multiplayer_update:
        print(f"Multiplayer should be updating and {ply.multiplayer_update}")

        # THIS IS VERY IMPORTANT YOU NEED THIS TO UPDATE THE SERVER
        ###################################
        multiplayer.update_Multiplayer()
        ###################################
        if multiplayer.client.connected:
            print("Connected: True")
            if ply.connected_text:
                print("Show Text")
                main_menu.connected.enable()
                ply.connected_text = False
            else:

                invoke(main_menu.connected.disable, delay = 2)
            main_menu.not_connected.disable()
        else:
            print("Connected: False")
            if ply.disconnected_text:
                main_menu.not_connected.enable()
                ply.disconnected_text = False
            else:
                invoke(main_menu.not_connected.disable, delay = 2)
            main_menu.connected.disable()

    # if the user is hosting the server, update the server
            
    if ply.server_running:
        print("Server Running: {ply.server_running}")
        ply.server.update_server()
        if ply.server.server_update:
            print(f"Server Updating: {ply.server.server_update}")
            ply.server.easy.process_net_events()
    

    # not player inputs but values sent from client to server to send to other clients in the same server 
def input(key):
    print(f"can multi update: {ply.multiplayer_update}")
    if ply.multiplayer_update:
        multiplayer.client.send_message("MyPosition", tuple(ply.position))
        print(f"POS: {ply.position}")

        multiplayer.client.send_message("MyRotation", tuple(ply.rotation))
        print(f"ROT: {ply.rotation}")
        
        multiplayer.client.send_message("MyTexture", str(ply.texture))
        print(f"TEXTURE: {ply.texture}")
        
        multiplayer.client.send_message("MyModel", str(ply.model_path))
        print(f"MODEL: {ply.model}")

    # spacers to make reading prints easier
    print("\n END of MAIN.PY")

app.run()