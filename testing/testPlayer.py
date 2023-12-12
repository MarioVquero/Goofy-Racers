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


        # Bools for collision
        self.hitting_wall = False
        self.atFinishLine = False



        # multiplayer bools
        self.multiplayer = False
        self.multiplayer_update = False
        self.multiplayer_running = False

        # show if youre connected to a server or not
        self.connected_text = True
        self.disconnected_test = False


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
        # Gravity
        movementY = self.velocity_y/50
        direction = (0, sign(movementY), 0)

        

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


