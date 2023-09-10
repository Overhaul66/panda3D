from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point2, Point3, Vec4
from panda3d.core import WindowProperties
from panda3d.core import loadPrcFile
from panda3d.core import (  CollisionNode, 
                            CollisionTube,
                            CollisionSphere, 
                            CollisionBox, 
                            CollisionTraverser, 
                            CollisionHandlerPusher
                         )
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
import sys

loadPrcFile('conf.prc')

GRAVITY = 10

class FloorPlan(ShowBase):

    def __init__(self):
        super().__init__()
        self.camera.setPos(0, 0, -5)
        #self.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(props)
        self.path = self.render.attach_new_node("player")
        self.path.setPos(0,0,2)
        base.camLens.set_fov(100, 100)
        base.camera.reparentTo(self.path)
        self.setBackgroundColor(0, 0, 0, 1)
        self.house = self.loader.loadModel('./floorplan.glb')
        self.house.setPos(0, 0, -2)
        self.house.setH(self.house, 90)
        self.house.reparentTo(self.render)
        self.prev_mouse = Point2(0)
        self.accept('q', self.quit_program)
        self.accept('c', self.viewCollisions)
        self.taskMgr.add(self.update_keys, 'update-keys')
        self.taskMgr.add(self.debug, 'debug')

        self.viewCollisions = False

        OnscreenText(text="Press Q to quit\nPress C to toggle collisions off and on", 
                     pos=Point2(-0.7,0.9), scale=0.05, fg=Vec4(1,1,1,1))

        player_collision = CollisionNode("player")
        player_collision.add_solid(CollisionTube(
            Point3(0, 0, 0),
            Point3(0, 0, 0.5),
            0.5
        ))
        player_collision_path = self.path.attach_new_node(player_collision)
        player_collision_path.setZ(-.7)
        player_collision_path.setY(0.5)
        # see the player collision
       
        #player_collision_path.show()

        house_collision = CollisionNode("house collision")
        
        floor_collision_solid = CollisionBox(
            Point3(0, 0, -0.1),
            8.9, 4.7, 0.2
        )

        sidewall_collision_solid_1 = CollisionBox(
            Point3(0,4.6,1.8),
            8.9, 0.15, 1.6
        )

        sidewall_collision_solid_2 = CollisionBox(
            Point3(-1.9,-4.67,1.8),
            6.9, 0.15, 1.6
        )

        sidewall_collision_solid_3 = CollisionBox(
            Point3(-8.79,1.7,1.7),
            0.10, 2.8, 1.6
        )

        sidewall_collision_solid_4 = CollisionBox(
            Point3(-8.79,-3.45,1.7),
            0.10, 1.4, 1.6
        )

        sidewall_collision_solid_5 = CollisionBox(
            Point3(5.04,-1.0,1.7),
            0.10, 3.8, 1.6
        )

        sidewall_collision_solid_6 = CollisionBox(
            Point3(8.75,2.0,1.7),
            0.10, 1.2, 1.6
        )

        sidewall_collision_solid_7 = CollisionBox(
            Point3(7.0,0.9,1.7),
            1.7, 0.10, 1.6
        )

        sidewall_collision_solid_8 = CollisionBox(
            Point3(8.0,2.8,1.7),
            0.7, 0.10, 1.6
        )

        sidewall_collision_solid_9 = CollisionBox(
            Point3(5.5,2.75,1.7),
            0.5, 0.05, 1.6
        )

        sidewall_collision_solid_10 = CollisionBox(
            Point3(-1.3,-2.9,1.7),
            3, 0.05, 1.6
        )

        sidewall_collision_solid_11 = CollisionBox(
            Point3(3.5,-0.94,1.7),
            1.4, 0.07, 1.6
        )

        sidewall_collision_solid_12 = CollisionBox(
            Point3(0.15,-0.94,1.7),
            0.6, 0.07, 1.6
        )

        sidewall_collision_solid_13 = CollisionBox(
            Point3(-1.7,-0.94,1.7),
            0.3, 0.07, 1.6
        )

        sidewall_collision_solid_14 = CollisionBox(
            Point3(-6.6,-3.0,1.7),
            0.25, 0.05, 1.6
        )

        sidewall_collision_solid_15 = CollisionBox(
            Point3(-8.2,-3.0,1.7),
            0.5, 0.05, 1.6
        )

        sidewall_collision_solid_16 = CollisionBox(
            Point3(-2,-1.9,1.7),
            0.05,1, 1.6
        )

        sidewall_collision_solid_17 = CollisionBox(
            Point3(0.5,-1.9,1.7),
            0.05,1, 1.6
        )

        sidewall_collision_solid_18 = CollisionBox(
            Point3(1.67,-3.8,1.7),
            0.05,0.7, 1.6
        )

        sidewall_collision_solid_19 = CollisionBox(
            Point3(-6.35,-3.8,1.7),
            0.05,0.7, 1.6
        )


        solids = [floor_collision_solid
                ,sidewall_collision_solid_1
                ,sidewall_collision_solid_2
                ,sidewall_collision_solid_3
                ,sidewall_collision_solid_4
                ,sidewall_collision_solid_5
                ,sidewall_collision_solid_6
                ,sidewall_collision_solid_7
                ,sidewall_collision_solid_8
                ,sidewall_collision_solid_9
                ,sidewall_collision_solid_10
                ,sidewall_collision_solid_11
                ,sidewall_collision_solid_12
                ,sidewall_collision_solid_13
                ,sidewall_collision_solid_14
                ,sidewall_collision_solid_15
                ,sidewall_collision_solid_16
                ,sidewall_collision_solid_17
                ,sidewall_collision_solid_18
                ,sidewall_collision_solid_19
        ]

        for solid in solids:
            house_collision.add_solid(solid)

        self.house_collision_path = self.house.attach_new_node(house_collision)
       

        base.cTrav = CollisionTraverser()
        pusher = CollisionHandlerPusher()
        base.cTrav.add_collider(player_collision_path, pusher)
        pusher.add_collider(player_collision_path, self.path)

    def update_keys(self, task):

        if base.mouseWatcherNode.has_mouse():
            mouse = base.mouseWatcherNode.get_mouse()
            button = getattr(base.mouseWatcherNode, 'is_raw_button_down',
                             base.mouseWatcherNode.is_button_down)
            delta = mouse - self.prev_mouse
            self.prev_mouse = Point2(mouse)
            self.path.setH(self.path, -delta.x * 15)
            base.cam.set_p(base.cam, delta.y * 15)
            base.cam.set_p(max(-85, min(base.cam.get_p(), 85)))
            speed = (8 + int(button("lshift") * 4)) * base.clock.dt
            # move the player (path ) relative to itself, makes
            # player moves to the path is looking at
            self.path.setPos(self.path,
                             ((int(button("d") - int(button("a"))) * speed)),
                             ((int(button("w") - int(button("s"))) * speed)),
                            0)

            self.path.setZ(self.path.getZ() - GRAVITY * base.clock.dt)

        return task.cont

    def debug(self, task):
        button = base.mouseWatcherNode.is_button_down('p')
        return task.cont

    def quit_program(self):
        sys.exit(0)

    def viewCollisions(self):
        if not self.viewCollisions:
            self.house_collision_path.show()
        else:
            self.house_collision_path.hide()   
        self.viewCollisions = not self.viewCollisions


game = FloorPlan()
game.run()
