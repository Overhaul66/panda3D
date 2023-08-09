from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Vec3, WindowProperties
from direct.task import Task
loadPrcFile('conf.prc')
import math

def rotate(degrees, vector):
    deg2Rad = degrees * (math.pi / 180)
    xr = vector.getX() * math.cos(deg2Rad) - vector.getY() * math.sin(deg2Rad)
    yr = vector.getX() * math.sin(deg2Rad) + vector.getY() * math.cos(deg2Rad)
    zr = vector.getZ()

    return Vec3(xr, yr, zr)

class FloorPlan(ShowBase):


    def __init__(self):
        super().__init__()
        self.disableMouse()
        
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)

        self.cam.setPos(0, 0, 0.8)
        self.setBackgroundColor(0, 0, 0, 1)
        self.house = self.loader.loadModel('./floorplan.glb')
        self.house.setH(265)
        self.house.reparentTo(self.render)
        
        self.accept('q', self.quit_program)

        self.accept('w', self.setKey, ["forward", True])
        self.accept('w-up', self.setKey, ["forward", False])
        self.accept('s', self.setKey, ["backward", True])
        self.accept('s-up', self.setKey, ["backward", False])
        self.accept('a', self.setKey, ["left", True])
        self.accept('a-up', self.setKey, ["left", False])
        self.accept('d', self.setKey, ["right", True])
        self.accept('d-up', self.setKey, ["right", False])

        self.key = {
            "forward":False,
            "backward":False,
            "left":False,
            "right":False,
        }   

        # 7 11

        self.velocity = Vec3()
        self.direction = Vec3()
        self.speed = 0.1
        self.x = 0
        self.y = 0
        self.px = 0
        self.py = 0

        self.taskMgr.add(self.moveTask, "move task")
        self.taskMgr.add(self.mouselookTask, "mouselook task")


    def quit_program(self):
        sys.exit(0)

    def setKey(self, keypressed, state):
        self.key[keypressed] = state

    def moveTask(self, task):

        if self.key['forward']:
            self.direction.setY(1)
        elif self.key['backward']:
            self.direction.setY(-1)
        else:
            self.direction.setY(0)

        if self.key['left']:
            self.direction.setX(-1) 
        elif self.key['right']:
            self.direction.setX(1)
        else:
            self.direction.setX(0)

        #print(self.direction.getX(), self.direction.getY(), self.direction.getZ())
        #rotate the direction vector according to the camera's angle
        rotated_vec = rotate(self.cam.getH(), self.direction)

        self.velocity = rotated_vec * self.speed

        self.cam.setPos(self.cam.getPos() + self.velocity)

        return task.cont

    #worst implementation of mouselook ever 
    def mouselookTask(self, task):
        mw = base.mouseWatcherNode
        if mw.has_mouse():
            self.x = mw.getMouseX()
            self.y = mw.getMouseY()

            relX = self.x - self.px
            relY = self.y - self.py

            self.cam.setH(self.cam.getH() - relX * 360)
            self.cam.setP(self.cam.getP() + relY * 90)
    
            self.px = self.x
            self.py = self.y

        return task.cont


game = FloorPlan()
game.run()