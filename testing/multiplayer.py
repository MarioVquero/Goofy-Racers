from ursinanetworking import *
from ursina import Entity,Vec3,color,destroy
from testPlayer import Player,PlayerRep

# its 1:38 am and I forgot what this does but pretty sure it manages the server
class Multiplayer(Entity):
    def __init__(self, player):
        self.player = player

        if str (self.car.ip.text) != "IP" and str(self.car.port.text) != "PORT":
            self.client = UrsinaNetworkingClient("localhost", 55555)
            self.easy = EasyUrsinaNetworkingClient(self.client)

            self.players = {}
            self.players_target_pos = {}
            self.players_target_rot = {}
            self.players_target_model = {}
            self.players_target_tex = {}
            

            self.selfid = -1

            @self.client.event
            def GetID(id):
                self.selfid = id
                print(f"My ID is : {self.selfid}")

            # when a new player joins
            @self.client.event
            def onReplicatedVariableCreated(variable):
                variable_name = variable.name
                

                self.players_target_pos[variable_name] = Vec3(-80,-30,15)
                self.players_target_rot[variable_name] = Vec3(0,90,0)

                self.players_target_model[variable_name] = "cube"
                self.players_target_tex[variable_name] = "grass.png"
                self.players[variable_name] = PlayerRep(self.player, (-80, -30, 15), (0, 90, 0))

                if self.selfid == int(variable.content["id"]):
                    self.players[variable_name].color = color.red
                    self.players[variable_name].visible = False
            
            # updates when the player moves or rotates 
            @self.easy.event
            def onReplicatedVariableUpdated(variable):
                self.players_target_pos[variable.name] = variable.content["position"]
                self.players_target_rot[variable.name] = variable.content["rotation"]
                self.players_target_model[variable.name] = variable.content["model"]
                self.players_target_tex[variable.name] = variable.content["texture"]

            # removes the player from everything on disconnect
            @self.easy.event
            def onReplicatedVaribaleRemoved(variable):
                variable_name = variable.name
                
                destroy(self.players[variable_name])
                del self.player[variable_name]
            

            # Updates the player for the server
            def update_Multiplayer(self):
                for p in self.players:
                    self.players[p].position += (Vec3(self.players_target_pos[p]) - self.players[p].position)/25
                    self.players[p].rotation += (Vec3(self.players_target_rot[p]) - self.players[p].rotation)/25
                    self.players[p].model = f"{self.player_target_model[p]}"
                    self.players[p].texture = f"{self.players_target_tex[p]}"



                self.easy.process_net_events()