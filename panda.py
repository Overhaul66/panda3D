from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task

from panda3d.core import WindowProperties
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec4
from panda3d.core import Vec3
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerPusher
from panda3d.core import CollisionNode
from panda3d.core import CollisionSphere
from panda3d.core import CollisionTube

class Game(ShowBase):
    
    def __init__(self):
        super().__init__()

        self.render.setShaderAuto()
        
        properties = WindowProperties()
        properties.setSize(1000, 750)
        properties.setTitle("Eli")
        self.win.requestProperties(properties)

        self.environment = self.loader.loadModel("Environment/environment")
        self.environment.reparentTo(self.render)

        self.tempActor = Actor('models/act_p3d_chan', 
            {
                "walk":"models/a_p3d_chan_walk",
            }
        )
        self.tempActor.reparentTo(self.render)
        #self.tempActor.setPos(0,7,0)
        #self.tempActor.getChild(0).setH(90)
        self.tempActor.loop('walk')


        mainlight = DirectionalLight("main light")
        #mainlight.setColor(Vec4(1,1,1,1))
        self.mainLightNodePath = self.render.attachNewNode(mainlight)
        self.mainLightNodePath.setHpr(45, -45, 0)
        self.render.setLight(self.mainLightNodePath)

        self.accept('d', self.updateKeyMap, ["right", True] )
        self.accept('d-up', self.updateKeyMap, ["right", False] )
        self.accept('a', self.updateKeyMap, ["left", True] )
        self.accept('a-up', self.updateKeyMap, ["left", False] )
        self.accept('w', self.updateKeyMap, ["top", True] )
        self.accept('w-up', self.updateKeyMap, ["top", False] )
        self.accept('s', self.updateKeyMap, ["down", True] )
        self.accept('s-up', self.updateKeyMap, ["down", False] )
        

        self.keyMap = {
            "right":False,
            "left":False,
            'top':False,
            'down':False,
            'shoot':False,
        }

        self.taskMgr.add(self.updatePlayer)

        #collision
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        #create a collision node
        colliderNode = CollisionNode("player")
        #add a collision solid by creating a solid
        colliderNode.addSolid(CollisionSphere(0,0,0,0.3))
        #attach the collion node to the player
        collider = self.tempActor.attachNewNode(colliderNode)
        collider.show()

        #tell the traverser and the pusher that the player is an object that should 
        #collide with things

        #the pusher wants collider and a nodePath of the player
        self.pusher.addCollider(collider, self.tempActor)
        #the transverser wants a collider and a handler
        self.cTrav.addCollider(collider, self.pusher)

        #prevents the pusher responses to be restricted to the horizontal 
        #since we dealing with falt surfaces (2D)
        self.pusher.setHorizontal(True)

        wallSolid = CollisionTube(-8.0,0,0,8.0,0,0,0.2) #create a collison solid
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

        self.disableMouse()

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def updatePlayer(self, task):
        dt = globalClock.getDt()

        if self.keyMap['right']:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(10 * dt,0,0))
        elif self.keyMap['left']:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(-10 * dt,0,0))
        elif self.keyMap['top']:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0,10 * dt,0))
        elif self.keyMap['down']:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0,-10 * dt,0))

        return task.cont
        

game = Game()
game.run()
