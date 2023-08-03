from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task

import sys

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

        # add in pattern , for determing a node colliding into another node
        self.pusher.add_in_pattern("%fn-into-%in")

        self.accept("trapEnemy-into-wall", self.stopTrap)
        self.accept("trapEnemy-into-trapEnemy", self.stopTrap)
        self.accept("trapEnemy-into-player", self.trapHitsSomething)
        self.accept("trapEnemy-into-walkingEnemy", self.trapHitsSomething)


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
        self.accept('q', self.updateKeyMap, ['shoot', True])
        self.accept('q-up', self.updateKeyMap, ['shoot', False])
        

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
        self.tempEnemy = WalkingEnemy(Vec3(0,0,0))
        self.trapEnemy = TrapEnemy(Vec3(-2, 7, 0))

       

        self.disableMouse()

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def updateTask(self, task):
        dt = globalClock.getDt()
        
        self.player.update(self.keyMap, dt)
        self.tempEnemy.update(self.player, dt)
        self.trapEnemy.update(self.player, dt)

        return task.cont

    def stopTrap(self, entry):
        # get the from collision node path
        # in this case trap
        collider = entry.getFromNodePath()
        
        if collider.hasPythonTag("owner"):
            # get reference to trap object
            trap = collider.getPythonTag("owner")
            trap.moveDirection = 0
            trap.ignorePlayer = False

    def trapHitsSomething(self, entry):
        collider = entry.getFromNodePath()

        if collider.hasPythonTag("owner"):
            trap = collider.getPythonTag("owner")

            if trap.moveDirection == 0:
               return

            # get into collider [ what the trapis colliding into ]
            # in this case player or walking enemy
            intoCollider = entry.getIntoNodePath()
            if intoCollider.hasPythonTag("owner"):
                # get the objects of the collider
                obj = intoCollider.getPythonTag("owner")
                if isinstance(obj, Player):
                    if not trap.ignorePlayer:
                        obj.alterHealth(-1)
                        trap.ignorePlayer = True
                else:
                    obj.alterHealth(-10)

game = Game()
game.run()
