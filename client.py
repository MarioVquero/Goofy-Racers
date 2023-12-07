from re import A
import threading

from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController

from ursinanetworking import *
from time import sleep

import player

app = Ursina()


Client = UrsinaNetworkingClient("localhost", 55555)
Easy = EasyUrsinaNetworkingClient(Client)
window.borderless = False


ad = Audio("")
sky = Sky()

Players = {}
PlayersTargetPos = {}

SelfId = -1

@Client.event
def GetId(id):
    global SelfId
    SelfId = id
    print(f"My ID is: {SelfId}")

@Easy.event
def onReplicatedVariableUpdate(variable):
    global Client
    variable_name = variable.name
    variable_type = variable.content["type"]

    if variable_type != "player":
        print("what tf is this ")
    elif variable_type == "player":
        Players[variable_name] = player.PlayerRep()
        if SelfId == int(variable.content["id"]):
            Players[variable_name].color = color.red
            Players[variable_name].visisble = False

@Easy.event
def onReplicatedVariableUpdated(variable):
    PlayersTargetPos[variable.name] = variable.content["position"]


@Easy.event
def onReplicatedVariableRemoved(variable):
    variable_name = variable.name
    variable_type = variable.content["type"]

    if variable_type != "player":
        print("what tf is this")

    elif variable_type == "player":
        destroy(Players[variable_name])
        del Players[variable_name]

Ply = player.Player()

index = 1

def update():

    if Ply.position[1] < -5:
        Ply.position = (5,5)

    for p in Players:
        try:
            Players[p].position += (Vec3(PlayersTargetPos[p]) - Players[p].position) /25
        except Exception as e: print(e)
    Easy.process_net_events()

app.run()

