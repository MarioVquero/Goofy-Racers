from ursinanetworking import *
from ursina import Entity, Vec3, color,destroy
from ursina.prefabs.first_person_controller import FirstPersonController


# carSTR = "Low_Poly_Car.obj"
carTex = "Wheel Base Color.png"

sign = lambda x: -1 if x <0 else (1 if x>0 else 0)
# have to make a camera because FirstPersonController bugs out the whole thing

# the player class that has all the default values
class Player(Entity):
    def __init__(self, position = (0,0,4), rotation = (0,0,0), topSpeed = 10, accelaration = 1, brakingStrength = 30, friction = 1, cameraSpeed = 10, drift_speed = 35):
        super().__init__(
            position = position,
            rotation = rotation,
            model = "Low_Poly_Car.obj",
            texture = carTex
            )

        # Rotation parent
        self.rotation_parent = Entity()

        # controls
        self.controls = "wasd"

        # Player values
        self.speed = 0
        self.velocity_y = 0
        self.rotation_speed = 0
        self.max_rotation_speed = 5
        self.steering_amount = 8
        self.topSpeed = topSpeed
        self.brakingStrength = brakingStrength
        self.camera_speed = cameraSpeed
        self.accelaration = accelaration
        self.friction = friction
        self.turning_Speed = 40
        self.pivot_rotation_distance = 1
        self.drift_speed = drift_speed
        self.drift_amount = 4.5
        self.max_drift_speed = 20
        self.min_drift_speed = 10




        # Camera Values to follow the players
        self.camera_angle = "behind"
        self.camera_offset = (0,100,0)
        self.camera_rotation = 40
        self.camera_follow = True
        self.change_camera = False
        self.c_pivot = Entity()
        self.camera_pivot = Entity(parent = self.c_pivot, position = self.camera_offset)
        

        # pivots 
        self.pivot = Entity()
        self.pivot.position = self.position
        self.pivot.rotation = self.rotation

        # Bools for collision
        self.copy_normals = False
        self.hitting_wall = False
        self.atFinishLine = False
        
        # bools for driving
        self.driving = False
        self.driving = True

        # Making sure Tracks is accessible in update
        self.main_track = None


        # multiplayer bools
        self.multiplayer = False
        self.multiplayer_update = False
        self.server_running = False

        # show if youre connected to a server or not
        self.connected_text = True
        self.disconnected_text = False

        self.model_path = str(self.model).replace("render/scene/player", "")

        invoke(self.update_model_path,delay = 5)


    def player_car(self):
        self.model = "Low_Poly_Car.obj"
        self.texture = carTex
        self.topSpeed = 60
        self.accelaration = 10
        self.turning_Speed = 10
        self.max_rotation_speed = 6
        self.steering_amount = 15
        self.drift_speed = 20

    def update(self):
        # spacer to make reading prints easier
        print("\n")
        # help keep track of the player
        # print(f"POS: {self.position}")
        self.pivot.position = self.position
        # print(f"PivotPOS: {self.pivot.position} \n POS: {self.position}")
        self.c_pivot.position = self.position
        self.c_pivot.rotation_y = self.rotation_y
        self.camera_pivot.position = self.camera_offset

        # camera
        if self.camera_follow:
            # print(f"Camera POS: {camera.position} \n Player POS: {Player.position}")
            if self.camera_angle == "top":
                # camera.rotation_x = 50
                # used to change the camera to a different POV cant be used at the moment
                if self.change_camera:
                    camera.rotation_x  = 35
                    self.camera_rotation = 40
                
                self.camera_offset = (0,100,0)
                self.camera_speed = 4
                self.change_camera = False
                # camera.rotation_x = lerp(camera.rotation_x, self.camera_rotation, 2 * time.dt)
                camera.world_position = lerp(camera.world_position, self.camera_pivot.world_position, time.dt * self.camera_speed / 2)
                # print(camera.world_position)
                camera.world_rotation_y = lerp(camera.world_rotation_y, self.world_rotation_y, time.dt * self.camera_speed / 2)
            
            elif self.camera_angle == "behind":
                camera.rotation_x = 12
                self.camera_rotation = 40
                self.camera_offset = (0,10,-30)
                self.camera_speed = 8
                
                # print(f"Camera POS: {camera.world_position}")
                # works on the x axis of rotation
                camera.rotation_x = lerp(camera.rotation_x,self.camera_rotation /3, 2 * time.dt)
                
                # print(f"Cam Pivot: {self.camera_pivot.world_position}")
                # print(self.camera_speed)
                # handles cam position
                camera.world_position = lerp(camera.world_position, self.camera_pivot.world_position, time.dt * self.camera_speed / 2)
                

                # works on the y axis of rotation 
                camera.world_rotation_y = lerp(camera.world_rotation_y, self.world_rotation_y, time.dt * self.camera_speed/2)

                # print(f"Time.DT : {time.dt} \n CamSpeed :{self.camera_speed} \n CamPos: {camera.world_position} \n PlayerPos : {self.position}")
        
        # the y rotation distance between the car and the pivot
        self.pivot_rotation_distance = (self.rotation_y - self.pivot.rotation_y)
        

        # Drifting/Turning
        # NOTE: this is necessary for making the car turn
        print(f"PivotRotY: {self.pivot.rotation_y} \n RotY: {self.rotation_y}")
        if self.pivot.rotation_y != self.rotation_y and self.driving:

            if self.pivot.rotation_y > self.rotation_y:
                
                print("rotate left")
                self.pivot.rotation_y -= (self.drift_speed * ((self.pivot.rotation_y - self.rotation_y) / 40)) * time.dt
                
                
                if self.speed > 1 or self.speed < -1:
                    self.speed += self.pivot_rotation_distance / self.drift_amount * time.dt
                self.camera_rotation -= self.pivot_rotation_distance / 3 * time.dt
                self.rotation_speed -= 1 * time.dt
                
                
                if self.pivot_rotation_distance >= 50 or self.pivot_rotation_distance <= -50:
                    self.drift_speed += self.pivot_rotation_distance / 5 * time.dt
                
                
                else:
                    self.drift_speed -= self.pivot_rotation_distance / 5 * time.dt
            
            if self.pivot.rotation_y < self.rotation_y:

                print(f"rotate right \n")
                self.pivot.rotation_y += (self.drift_speed * ((self.rotation_y - self.pivot.rotation_y) / 40)) * time.dt
                
                
                if self.speed > 1 or self.speed < -1:
                    self.speed -= self.pivot_rotation_distance / self.drift_amount * time.dt
                self.camera_rotation += self.pivot_rotation_distance / 3 * time.dt
                self.rotation_speed += 1 * time.dt
                
                
                if self.pivot_rotation_distance >= 50 or self.pivot_rotation_distance <= -50:
                    self.drift_speed -= self.pivot_rotation_distance / 5 * time.dt
                
                
                else:
                    self.drift_speed += self.pivot_rotation_distance / 5 * time.dt


        # Gravity
        movementY = self.velocity_y / 50 * time.dt
        direction = (0, sign(movementY), 0)

        # main raycast for collision
        y_ray = raycast(origin=self.world_position,direction=(0,-1,0),ignore=[self,])
        
        # NOTE: can only drive if on the ground
        if y_ray.distance <= 5:
            # Holding W or Up Arrow allows you and your camera to move forward
            if held_keys[self.controls[0]] or held_keys["up arrow"]:
                
                self.speed += self.accelaration * 50 * time.dt
                self.speed += -self.velocity_y * 4 * time.dt

                self.camera_rotation -= self.accelaration * 30 * time.dt
                self.driving = True
                
            else:
                self.driving = False
                if self.speed >1:
                    self.speed -= self.friction *5 * time.dt
                elif self.speed < -1:
                    self.speed += self.friction * 5 * time.dt
                self.camera_rotation += self.friction * 20  * time.dt
            if held_keys[self.controls[2]] or held_keys["down arrow"]:
                self.speed -= self.brakingStrength * time.dt
                self.braking  = True
            else:
                self.braking = False
        
        # STEERING
        # print(f"Rotation_y: {self.rotation_y} \n Rotation speed: {self.rotation_speed}")
        self.rotation_y += self.rotation_speed * 50 * time.dt

        if self.rotation_speed > 0:
            self.rotation_speed -= self.speed / 6 * time.dt
        elif self.rotation_speed < 0:
            self.rotation_speed += self.speed / 6 * time.dt

        if self.speed > 1 or self.speed < -1:
            if held_keys[self.controls[1]] or held_keys["left arrow"]:
                self.rotation_speed -= self.steering_amount * time.dt
                self.position.x += 5 * time.dt
                if self.speed > 1:
                    self.speed -= self.turning_Speed * time.dt
                elif self.speed < 0:
                    self.speed += self.turning_Speed / 5 * time.dt
            
            elif held_keys[self.controls[3]] or held_keys["right arrow"]:
                self.rotation_speed += self.steering_amount * time.dt
                self.position -= 5 * time.dt
                if self.speed > 1:
                    self.speed -= self.turning_Speed * time.dt
                elif self.speed < 0:
                    self.speed += self.turning_Speed / 5 * time.dt

            else:
                if self.rotation_speed > 0:
                    self.rotation_speed = 0#5 * time.dt
                elif self.rotation_speed < 0:
                    self.rotation_speed = 0#5 * time.dt
                    
        # Cap the speed
        if self.speed >= self.topSpeed:
            self.speed = self.topSpeed
        if self.speed <= -15:
            self.speed = -15
        if self.speed <= 0:
            self.pivot.rotation_y = self.rotation_y
        
        # Cap the camera rotation
        if self.camera_rotation >= 40:
            self.camera_rotation = 40
        elif self.camera_rotation <= 30:
            self.camera_rotation = 30

        # steering limit
        if self.rotation_speed >= self.max_rotation_speed:
            self.rotation_speed = self.max_rotation_speed
        if self.rotation_speed <= -self.max_rotation_speed:
            self.rotation_speed = -self.max_rotation_speed

        # rotation
        self.rotation_parent.position = self.position


        # not sure if necessary but leaving uncommented for easy access
        # Lerps the car's rotation to the rotation parent's rotation (Makes it smoother)
        self.rotation_x = lerp(self.rotation_x, self.rotation_parent.rotation_x, 20 * time.dt)
        self.rotation_z = lerp(self.rotation_z, self.rotation_parent.rotation_z, 20 * time.dt)

        # check if car is hitting the ground

        if self.visible:
            # print(y_ray.distance)
            if y_ray.distance <= self.scale_y * 1.7 + abs(movementY):
                # resets velocity of falling so it doesnt add up
                self.velocity_y = 0

                
                # check if collision with wall or steep slope
                ############################
                # YOURE THE FUCKING PROBLEM
                if y_ray.world_normal.y > 0.7 and y_ray.world_point.y - self.world_y < 0.5:
                    # set the y value to the grounds y value
                    self.y = y_ray.world_point.y + 1.4
                    self.hitting_wall = False
                else:
                    self.hitting_wall = True
                ############################
                if self.copy_normals:
                    self.ground_normal = self.position + y_ray.world_normal
                else:
                    self.ground_normal = self.position + (0,180,0)


                # rotates the car according the ground normals
                if not self.hitting_wall:
                    # print("TURNING")
                    self.rotation_parent.look_at(self.ground_normal, axis="up")

                    self.rotation_parent.rotate((0,self.rotation_y + 180, 0))
                
                else:
                    self.rotation_parent.rotation = self.rotation


            else:
                self.y += movementY * 50 * time.dt
                self.velocity_y -= 50 * time.dt
                self.rotation_parent.rotation = self.rotation
                
        # movement
        # print(f"Pivot.Forward: ({self.pivot.forward[0]}, {self.pivot.forward[1]}, {self.pivot.forward[2]})")
        movementX = self.pivot.forward[0] * self.speed * time.dt
        movementZ = self.pivot.forward[2] * self.speed * time.dt
        # print(f"Pivot.Forward: ({self.pivot.forward[0]}, {self.pivot.forward[1]}, {self.pivot.forward[2]})")

        # collision detection
        print(f"Movement X: {movementX}")
        if movementX != 0:
            print("moving")
            direction = (sign(movementX),0,0)
            print(f"MovementX Direc: {direction}")
            x_ray = raycast(origin  = self.world_position, direction= direction, ignore = [self,])

            if x_ray.distance > self.scale_x/2 + abs(movementX):
                self.x += movementX
                print(self.x)
        print(f"Movement Z: {movementZ}")
        if movementZ != 0:
            direction = (0,0,sign(movementZ))
            print(f"movementZ Direc: {direction}")
            z_ray = raycast(origin = self.world_position, direction = direction, ignore = [self, ])

            if z_ray.distance > self.scale_z /2 + abs(movementZ):
                self.z += movementZ

        # spacer to make reading prints easier
        print("\n")
        

    def update_model_path(self):
        """
        Updates the models path for multiplayer
        """
        self.model_path = str(self.model).replace("render/scene/player/", "")
        invoke(self.update_model_path,delay =3)


# class to copy and update the players position and rotation for multiplayer
class  PlayerRep(Entity):
    def __init__(self, player, position = (0,0,0), rotation = (0,0,0)):
        super().__init__(
            parent = scene,
            model = "Low_Poly_Car.obj",
            texture = carTex,
            collider = "box",
            position = position,
            rotation = rotation,
            scale = (1,1,1)
        )
        self.model_path = str(self.model).replace("render/scene/playerRep/","")
        self.player = player
        invoke(self.update_rep,delay = 5)
        print("testing server updating")
        
    # used to continuously update the pos and rot of the PlayerRep to match the values of the Player
    def update_rep(self):
        self.position = self.player.position
        self.rotation = self.player.rotation
        invoke(self.update_rep, delay = 5)


