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
        #self.props.setMouseMode(WindowProperties.M_relative)
        self.props.setFullscreen(True)

        self.win.requestProperties(self.props)

        self.rot = 0

        self.POSX = int(base.win.getXSize() / 2)
        self.POSY = int(base.win.getYSize() / 2)

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
        base.cam.setH(265)
        

        self.disable_mouse()

        taskMgr.add(self.move_phoenix, 'move phoenix')
        taskMgr.add(self.mouse_movement, 'mouse_movemnt')

        self.currentMouseX = 0
        self.previousMouseX = 0
        self.currentMouseY = 0
        self.previousMouseY = 0
        self.mouseMotionX = False
        self.mouseMotionY = False

        self.accept('q', self.quit)
       
    def quit(self):
        sys.exit()

    def move_phoenix(self, task):
        dt = globalClock.getDt()
       
        #self.phoenix_bird.setPos(self.phoenix_bird.getPos() + Vec3(1 * dt, 0, 0) )

        return task.cont 
    
    def mouse_movement(self, task):

        # get mouse position
        if base.mouseWatcherNode.hasMouse():
            self.currentMouseX = base.mouseWatcherNode.getMouseX()
            self.currentMouseY = base.mouseWatcherNode.getMouseY()
            # set mouse position to the middle of the window
            base.win.movePointer(0,self.POSX,self.POSY)
            
           
           
        # check if current mouse X position is equal to previous X mouse position
        # if yes , there is a motion, if not there was no motion
        if self.currentMouseX != self.previousMouseX:
            self.mouseMotionX = True
        else:
            self.mouseMotionX = False

        if self.currentMouseY != self.previousMouseY:
            self.mouseMotionY = True
        else:
            self.mouseMotionY = False

        # store current mouse X for reference
        self.previousMouseX = self.currentMouseX
        self.previousMouseY = self.currentMouseY

        # create mouse sensitivity
        # somehow rotation moves slow!!1
        mouse_sensitivity = 100 * globalClock.getDt()

        # rotate the player, als rotates the camera, 
        # since camera is a child of the parent 
        if self.mouseMotionX:
            if self.currentMouseX > 0:
                base.cam.setH(base.cam.getH() + self.currentMouseX * mouse_sensitivity)
                print("mouse going right")
            else:
                base.cam.setH(base.cam.getH() - self.currentMouseX * mouse_sensitivity)
                print("mouse going left")

        if self.mouseMotionY:
            if self.currentMouseY > 0:
                base.cam.setP(base.cam.getP() + self.currentMouseY )
            else:
                base.cam.setP(base.cam.getP() - self.currentMouseY )
          
        
        
      
        return task.cont



game = MyApp()
game.run()
