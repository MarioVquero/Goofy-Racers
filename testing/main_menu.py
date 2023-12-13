from ursina import *
from server import Server
import os

Text.default_resolution = 1080 * Text.size

class MainMenu(Entity):
    def __init__(self, player, main_track):
        super().__init__(
            parent = camera.ui
        )

        self.player = player

        # all the different menus
        self.start_menu = Entity(parent = self, enabled = True)
        self.host_menu = Entity(parent = self,enabled = False)
        self.created_server_menu = Entity(parent= self,enabled = False)
        self.server_menu = Entity(parent = self, enabled = False)
        self.main_menu = Entity(parent = self, enabled = False)
        self.quit_menu = Entity(parent = self, enabled = False)
        
        self.main_track = main_track

        def main_track_func():
            self.player.visible = True
            # mouse.locked = True
            self.player.position = (0,2,0)
            self.player.rotation = (0,90,0)
            main_track.enable()


        # switches the UI from start menu to host
        def multiplayer():
            print("Starting server process")
            self.start_menu.disable()
            self.host_menu.enable()

            
        # quit func to quit the game instead of X button on top right
        def quit():
            application.quit()
            os._exit(0)

        # takes you back from the quit menu
        def dont_quit():
            self.quit_menu.disable()
            self.start_menu.enable()

        # creates a server using the value of the input fields below
        def create_server():
            print(f"\n IP: {self.player.IP} \n PORT#: {self.player.PORT}")
            print(f"\n HOST IP: {self.player.host_ip} \n HOST PORT#: {self.player.host_port}")
            if str(self.player.host_ip) != "IP" and str(self.player.host_port) != "PORT":
                print("\nVALID IP AND PORT")
                self.player.server = Server(player.host_ip, player.host_port)
                self.player.server_running = True
                self.player.server.start_server = True
                print(self.player.server.start_server)
                self.host_menu.disable()
                self.created_server_menu.enable()
                
                
        # switches UI from host menu to server_menu names will change in the future for clarification
        def join_server_func():
            print("join server process")
            main_track.enable()
            self.host_menu.disable()
            self.server_menu.enable()

        # leave host meny and go to start
        def back_host():
            self.host_menu.disable()
            self.start_menu.enable()
            
        # finds the host IP and PORT and switches UI from created server to main
        def join_hosted_server_func():
            player.IP = player.host_ip
            player.PORT = player.host_port
            player.multiplayer = True
            self.created_server_menu.disable()
            self.main_menu.enable()

        # stops server from running
        def stop_server():
            application.quit()
            os._exit(0)

        # joins server and switching UI again
        def join_server():
            if str(self.player.IP) != "IP" and str(self.player.PORT) != "PORT":
                player.multiplayer = True
                self.server_menu.disable()
                self.main_menu.enable()
                main_track_func()
                print("track should load here")
                

        # change UI from server_menu to host
        def back_server():
            self.host_menu.enable()
            self.server_menu.disable()

        
        # starting title banner 
        start_title = Entity(model ="quad", scale = (0.5, 0.2, 0.2), texture = "grass.png", parent = self.start_menu, y = 0.3)


        # will have 2 buttons later but for now hard code to join server or start one if one isnt available
        # starts the process for creating a server
        start_button = Button(text = "Play Game",color = color.gray, highlight_color = color.light_gray,pressed_color = self.color.tint(-.2), scale_y = 0.1, scale_x = 0.3, y = -0.08, parent = self.start_menu)
        # changes the UI to create a server
        start_button.on_click = Func(multiplayer)


        # input fields for later use currently hard coding the IP to localhost and port 55555
        self.player.host_ip = "localhost"#InputField(default_value= "localhost", limit_content_to = "0123456789.localhost", color = color.black, alpha = 100, y = 0.1, parent = self.host_menu)
        self.player.host_port = 55555#InputField(default_value= "55555", limit_content_to = "0123456789", color = color.black, alpha = 100, y =0.02, parent = self.host_menu)

        # 3 different buttons for the Host_menu
        # button for creating a server
        create_server_button = Button(text = "Create Server", color = color.hex("F58300"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.host_menu)
        
        # button for joining a server
        join_server_button = Button(text = "Join Server", color = color.hex("0097F5"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.host_menu)
        
        # button for going back to the main menu
        back_button_host = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.host_menu)

        # calls the create_server Func that actually makes and starts the server
        create_server_button.on_click = Func(create_server)
        
        # switches UI to join existing server
        join_server_button.on_click = Func(join_server_func)
        
        # switches UI back to main menu
        back_button_host.on_click = Func(back_host)

        # button for joining an existing server
        join_hosted_server = Button(text = "Join Hosted Server", color = color.hex("F58300"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.created_server_menu)
        
        # not sure what this does at the moment might have missed this
        running = Text(text= "Running server...", scale =1.5, line_height = 2, x=0,origin = 0, y=0.2, parent = self.created_server_menu)
        
        # button that stops the server
        stop_button = Button(text="STOP",color= color.hex("D22828"),scale_y = 0.1, scale_x = 0.3, y = -0.22,parent = self.created_server_menu)
        
        # on click actually joins the server using join_hosted_server_func function
        join_hosted_server.on_click = Func(join_hosted_server_func)
        
        # on click stops the current server if youre host
        stop_button.on_click = Func(stop_server)

        # currently hard coded player IP and port Inputs will change later
        player.IP = "localhost"#InputField(default_value = "IP", limit_content_to = "0123456789.localhost", color = color.black, alpha = 100, y = 0.1, parent = self.server_menu)
        player.PORT = 55555#InputField(default_value = "PORT", limit_content_to = "0123456789", color = color.black, alpha = 100, y = 0.02, parent = self.server_menu)
        
        # # join button to join server
        join_button = Button(text = "Join Server", color = color.hex("F58300"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.server_menu)
        
        back_button_server = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.server_menu)


        join_button.on_click = Func(join_server)
        back_button_server.on_click = Func(back_server)


        # Server Error Log
        self.connected = Text(text = "Connected to server!", scale = 1.5, color = color.hex("4dff4d"), line_height = 2, x = -0.55, origin = 0, y = 0.45, parent = camera.ui)
        self.not_connected = Text(text = "Not connected to server...", scale = 1.5, color = color.hex("FF2E2E"), line_height = 2, x = -0.55, origin = 0, y = 0.45, parent = camera.ui)
        self.connected.disable()
        self.not_connected.disable()

