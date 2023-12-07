from asyncio.tasks import sleep
from random import uniform
from time import *
from ursinanetworking import *
# from perlin_noise import PerlinNoise
# from opensimplex import OpenSimplex
from ursina import *
# import asyncio

Server = UrsinaNetworkingServer("localhost", 55555)
Easy = EasyUrsinaNetworkingServer(Server)

@Server.event
def onClientConnected(client):
    Easy.create_replicated_variable(
        f"player_{client.id}",
        {"type": "player", "id" : client.id, "position": (0,0,0)}
    )
    print(f"{client} Connected")
    client.send_message("GetID", client.id)



@Server.event
def MyPosition(Client, NewPos):
    Easy.update_replicated_variable_by_name(f"player_{Client.id}", "position",NewPos)


# ground = Entity(
#     model = 'cube',
#     # texture = 'grass.png',
#     scale = (100,1,100),
#     collider= 'box'
# )

while True:
    Easy.process_net_events()