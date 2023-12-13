from ursinanetworking import *
from ursina import Entity, Vec3, color,destroy
from ursina.prefabs.first_person_controller import FirstPersonController


sign = lambda x: -1 if x <0 else (1 if x>0 else 0)
# have to make a camera because FirstPersonController bugs out the whole thing

# the player class that has all the default values
class Player(Entity):
    def __init__(self, position = (0,0,0), rotation = (0,0,0), topSpeed = 10, accelaration = 1, brakingStrength = 30, friction = 1, cameraSpeed = 10):
        super().__init__(
            model = "cube",
            texture = "grass.png",
            collider = "box",
            position = position,
            rotation = rotation
        )

        # Rotation parent
        self.rotation_parent = Entity()

        # controls
        self.controls = "wasd"

        # Player values
        self.speed = 0
        self.velocity_y = 0
        self.rotation_speed = 0
        self.max_rotation_speed = 2.6
        self.steering_amount = 8
        self.topSpeed = topSpeed
        self.brakingStrength = brakingStrength
        self.cameraSpeed = cameraSpeed
        self.accelaration = accelaration
        self.friction = friction
        self.turning_Speed = 5
        

        # Camera Follows the player
        self.camera_angle = "top"
        self.camera_offset = (0,60,-70)
        self.camera_rotation = 40
        self.camera_follow = False
        self.change_camera = False
        self.c_pivot = Entity()
        self.camera_pivot = Entity(parent = self.c_pivot, position = self.camera_offset)

        # pivots 
        self.pivot = Entity()
        self.pivot.position = self.position
        self.pivot.rotation = self.rotation
        


        # Bools for collision
        self.hitting_wall = False
        self.atFinishLine = False
        
        # Making sure Tracks is accessible in update
        self.main_track = None


        # multiplayer bools
        self.multiplayer = False
        self.multiplayer_update = False
        self.multiplayer_running = False

        # show if youre connected to a server or not
        self.connected_text = True
        self.disconnected_text = False


        def player_car(self):
            self.model = "cube"
            self.texture = "grass.png"
            self.topSpeed = 30
            self.accelaration = 0.3
            self.turning_Speed = 7
            self.max_rotation_speed = 3
            self.steering_amount = 7.5

        if self.camera_follow:
            if self.camera_angle == "top":
                if self.change_camera:
                    camera.rotation_x  = 35
                    self.camera_rotation = 40
                self.camera_offset = (0, 60, -70)
                self.camera_speed = 4
                self.change_camera = False
                camera.rotation_x = lerp(camera.rotation_x, self.camera_rotation, 2 * time.dt)
                camera.world_position = lerp(camera.world_position, self.camera_pivot.world_position, time.dt * self.camera_speed / 2)
                camera.world_rotation_y = lerp(camera.world_rotation_y, self.world_rotation_y, time.dt * self.camera_speed / 2)
            
        # self.pivot_rotation_distance = (self.rotation_y - self.pivot.rotation_y)

        # Gravity
        movementY = self.velocity_y/50
        direction = (0, sign(movementY), 0)

        # main raycast for collision
        y_ray = raycast(origin = self.world_position, direction = (0,-1,0), ignore = [self, ])

        if y_ray.distance <= 5:
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
        self.rotation_y += self.rotation_speed * 50 * time.dt

        if self.rotation_speed > 0:
            self.rotation_speed -= self.speed / 6 * time.dt
        elif self.rotation_speed < 0:
            self.rotation_speed += self.speed /6 * time.dt
        
        if self.speed > 1 or self.speed < -1:
            if held_keys[self.controls[1]] or held_keys["left arrow"]:
                self.rotation_speed -= self.steering_amount * time.dt
                self.drift_speed -= 5 * time.dt
                if self.speed > 1:
                    self.speed -= self.turning_speed * time.dt
                elif self.speed < 0:
                    self.speed += self.turning_speed / 5 * time.dt
            elif held_keys[self.controls[3]] or held_keys["right arrow"]:
                self.rotation_speed += self.steering_amount * time.dt
                self.drift_speed -= 5 * time.dt
                if self.speed > 1:
                    self.speed -= self.turning_speed * time.dt
                elif self.speed < 0:
                    self.speed += self.turning_speed / 5 * time.dt

        # # Cap the speed
        # if self.speed >= self.topspeed:
        #     self.speed = self.topspeed
        # if self.speed <= -15:
        #     self.speed = -15
        # if self.speed <= 0:
        #     self.pivot.rotation_y = self.rotation_y

        # Cap the camera rotation
        if self.camera_rotation >= 40:
            self.camera_rotation = 40
        elif self.camera_rotation <= 30:
            self.camera_rotation = 30

        # rotation
        self.rotation_parent.position = self.position

        # not sure if necessart but leaving uncommented for easy access

        # Lerps the car's rotation to the rotation parent's rotation (Makes it smoother)
        # self.rotation_x = lerp(self.rotation_x, self.rotation_parent.rotation_x, 20 * time.dt)
        # self.rotation_z = lerp(self.rotation_z, self.rotation_parent.rotation_z, 20 * time.dt)

        # check if car is hitting the ground

        if self.visible:
            if y_ray.distance <= self.scale_y * 1.7 + abs(movementY):
                self.velocity_y = 0
                # check if collision with wall or steep slope
                if y_ray.world_normal.y > 0.7 and y_ray.world_point.y - self.world_y < 0.5:
                    # set the y value to the grounds y value
                    self.y = y_ray.world_point.y = 1.4
                    self.hitting_wall = False
                else:
                    self.hitting_wall = True
                
                if self.copy_normals:
                    self.ground_normal = self.position + y_ray.world_normal
                else:
                    self.ground_normal = self.position + (0,180,0)

                # rotates the car according the ground normals
                if not self.hitting_wall:
                    self.rotation_parent.look_at(self.ground_normal, axis="up")
                    self.rotation_parent.rotate((0,self.rotation_y + 180, 0))

                else:
                    self.rotation_parent.rotation = self.rotation

            else:
                self.y += movementY * 50 * time.dt
                self.velocity_y -= 50 * time.dt
                self.rotation_parent.rotation = self.rotation
                

        movementX = self.pivot.forward[0] * self.speed * time.dt
        movementZ = self.pivot.forward[2] * self.speed * time.dt

        # collision detection
        if movementX != 0:
            direction = (sign(movementX),0,0)
            x_ray = raycast(origin  = self.world_position, direction= direction, ignore = [self,])

            if x_ray> self.scale_x/2 + abs(movementX):
                self.x += movementX

        if movementZ != 0:
            direction = (0,0,sign(movementZ))
            z_ray = raycast(origin = self.world_position, direction = direction, ignore = [self, ])

            if z_ray.distance > self.scale_z /2 + abs(movementZ):
                self.z == movementZ


# class to copy and update the players position and rotation for multiplayer
class  PlayerRep(Entity):
    def __init__(self, player, position = (0,0,0), rotation = (0,0,0)):
        super().__init__(
            parent = scene,
            model = "cube",
            texture = "grass.png",
            collider = "box",
            position = position,
            rotation = rotation,
            scale = (1,1,1)
        )

        invoke(self.update_rep,delay = 5)

    def update_rep(self):
        invoke(self.update_rep, delay = 5)


