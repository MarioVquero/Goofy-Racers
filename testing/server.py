from ursinanetworking import *
from ursina import *
import os

class Server:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.start_server = False
        self.server_update = False

    def update_server(self):
        # print("starting server ")
        if self.start_server:
            self.server = UrsinaNetworkingServer(self.ip, int(self.port))
            self.easy = EasyUrsinaNetworkingServer(self.server)

            @self.server.event
            def OnClientConnected(client):
                self.easy.create_replicated_variable(
                    f"player_{client.id}",
                    {"type": "player", "id": client.id, "position":(0,0,0),"rotation": (0,0,0),"model": "cube", "texture": "grass.png"}
                )
                print(f"{client} connected!!")
                client.send_message("GetID", client.id)
            
            @self.server.event
            def onClientDisconnected(client):
                self.easy.remove_replicated_variable_by_name(f"player_{client.id}")

            @self.server.event
            def MyPosition(client,newpos):
                self.easy.update_replicated_variable_by_name(f"player_{client.id}", "position", newpos)

            @self.server.event
            def MyRotation(client, newrot):
                self.easy.update_replicated_variable_by_name(f"player_{client.id}", "rotation", newrot)

            @self.server.event
            def MyModel(client, newmodel):
                self.easy.update_replicated_variable_by_name(f"player_{client.id}", "model", newmodel)

            @self.server.event
            def MyTexture(client, newtex):
                self.easy.update_replicated_variable_by_name(f"player_{client.id}", "texture", newtex)
            
            self.server_update = True
            self.start_server = False

if __name__ == "__main__":
    
    app = Ursina()
    window.title = "Goofy Racers Server Test"
    window.borderless = False

    # camera.ui needs to be that parent of these input fields
    ip = "localhost"#InputField(default_value= "IP", limit_content_to = "0123456789.localhost", color = color.black,alpha = 100, y= 0.1,parent = camera.ui)
    port = 55555#InputField(default_value= "PORT", limit_content_to = "0123456789", color = color.black,alpha = 100, y = 0.02, parent = camera.ui)

    server = Server(ip,port)

    Sky()

    # camera.ui needs to be the parent of these input fields
    def create_server():
        
        server.start_server = True
        running = Text(text="Running server...", scale = 1.5, line_height = 2, x=0, origin = 0,y=0, parent = camera.ui)
        create_server_button.disable()
        # ip.disable()
        # port.disable()
        stop_button.enable()
        print("Server has been made")

    def stop_server():
        os._exit(0)
    
    create_server_button = Button(text="Create", color= color.hex("F58300"),scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = camera.ui)
    create_server_button.on_click = Func(create_server)

    stop_button = Button(text="Stop", color = color.hex("D22828"),scale_y = 0.1, scale_x = 0.3, y=-0.2, parent = camera.ui)
    stop_button.disable()
    stop_button.on_click = Func(stop_server)

    def update():
        server.update_server()
        if server.server_update == True:
            server.easy.process_net_events()

    app.run()