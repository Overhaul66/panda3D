from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task

from panda3d.core import WindowProperties
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec4, Vec3
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerPusher
from panda3d.core import CollisionNode
from panda3d.core import CollisionSphere
from panda3d.core import CollisionTube
from panda3d.core import loadPrcFile

from GameObject import *

loadPrcFile("config/Config.prc")

class Game(ShowBase):
    
    def __init__(self):
        super().__init__()

        self.render.setShaderAuto()
        

        #properties = WindowProperties()
        #properties.setSize(1000, 750)
        #properties.setTitle("Game")
        #self.win.requestProperties(properties)

        self.environment = self.loader.loadModel("Environment/environment")
        self.environment.reparentTo(self.render)

        self.pusher = CollisionHandlerPusher()
        self.cTrav = CollisionTraverser()


        mainlight = DirectionalLight("main light")
        self.mainLightNodePath = self.render.attachNewNode(mainlight)
        self.mainLightNodePath.setHpr(45, -45, 0)
        self.render.setLight(self.mainLightNodePath)

        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)

        self.accept('d', self.updateKeyMap, ["right", True] )
        self.accept('d-up', self.updateKeyMap, ["right", False] )
        self.accept('a', self.updateKeyMap, ["left", True] )
        self.accept('a-up', self.updateKeyMap, ["left", False] )
        self.accept('w', self.updateKeyMap, ["up", True] )
        self.accept('w-up', self.updateKeyMap, ["up", False] )
        self.accept('s', self.updateKeyMap, ["down", True] )
        self.accept('s-up', self.updateKeyMap, ["down", False] )
        

        self.keyMap = {
            "right":False,
            "left":False,
            'up':False,
            'down':False,
            'shoot':False,
        }

        wallSolid = CollisionTube(-8.0,0,0,8.0,0,0,0.2) #create a collision solid
        wallNode = CollisionNode("wall") # create a collision node (wall node)
        wallNode.addSolid(wallSolid) # add the collision solid to the wall node
        wall = self.render.attachNewNode(wallNode) # attach the wall node to the root node (render)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(-8.0,0,0,8.0,0,0,0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = self.render.attachNewNode(wallNode)
        wall.setY(-8.0)
        wall.show()

        wallSolid = CollisionTube(0,-8.0,0,0,8.0,0,0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = self.render.attachNewNode(wallNode)
        wall.setX(-8.0)
        wall.show()

        wallSolid = CollisionTube(0,-8.0,0,0,8.0,0,0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = self.render.attachNewNode(wallNode)
        wall.setX(8.0)
        wall.show()

    
        self.camera.setPos(0, 0, 32)
        self.camera.setP(-90)

        self.taskMgr.add(self.updateTask, "update")

        self.player = Player() 
        self.tempEnemy = WalkingEnemy(Vec3(5,0,0))

        self.disableMouse()

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def updateTask(self, task):
        dt = globalClock.getDt()
        
        self.player.update(self.keyMap, dt)
        self.tempEnemy.update(self.player, dt)

        return task.cont


game = Game()
game.run()
