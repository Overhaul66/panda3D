from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import DirectionalLight, Vec4, Vec3, WindowProperties
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText

import math, sys

def rotate(vector, angle):
    x = vector.x * math.cos(angle) - vector.y * math.sin(angle)
    y = vector.x * math.sin(angle) - vector.y * math.cos(angle)
    z = vector.z
    
    return (x, y , z)

class MyApp(ShowBase):

    def __init__(self):
        super().__init__()

        self.props = WindowProperties()
        self.props.setCursorHidden(True)
        self.props.setMouseMode(WindowProperties.M_relative)
        #self.props.setFullscreen(True)

        self.win.requestProperties(self.props)

        self.rot = 0

        self.phoenix_bird = Actor('phoenix_bird/scene.bam',
                                  {'fly':'phoenix_bird/scene.bam'}
                                  )
        self.phoenix_bird.setPos(-10, 0, 1)
        self.phoenix_bird.loop('fly')
        self.phoenix_bird.reparentTo(self.render)
        self.phoenix_bird.setScale(0.001)

        self.forest = loader.loadModel("lowPolyForest/FOREST.dae")
        self.forest.reparentTo(self.render)
        self.forest.setP(90)

        self.light = DirectionalLight('main light')
        self.main_light = self.render.attachNewNode(self.light)
        self.main_light.setP(270)
        self.render.setLight(self.main_light)

        # reparent the camera to the player
        base.cam.reparentTo(self.phoenix_bird)
        base.cam.setPos(-2000,150, 100)
        base.cam.setH(265)
        

        self.disable_mouse()

        taskMgr.add(self.move_phoenix, 'move phoenix')
        taskMgr.add(self.mouse_movement, 'mouse_movemnt')

        self.currentMouseX = 0
        self.previousMouseX = 0
        self.mouseMotion = False

        self.accept('q', self.quit)
       
    def quit(self):
        sys.exit()

    def move_phoenix(self, task):
        dt = globalClock.getDt()
       
        #self.phoenix_bird.setPos(self.phoenix_bird.getPos() + Vec3(1 * dt, 0, 0) )

        return task.cont 
    
    def mouse_movement(self, task):


        if base.mouseWatcherNode.hasMouse():
            self.currentMouseX = base.mouseWatcherNode.getMouseX()
            print(base.mouseWatcherNode.getMouseX())
           

        if self.currentMouseX != self.previousMouseX:
            self.mouseMotion = True
        else:
            self.mouseMotion = False

        self.previousMouseX = self.currentMouseX

        mouse_sensitivity = 100 * globalClock.getDt()

        if self.mouseMotion:
            self.phoenix_bird.setH(self.phoenix_bird.getH() - self.currentMouseX * mouse_sensitivity)

        
       return task.cont



game = MyApp()
game.run()
