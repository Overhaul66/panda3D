from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, Vec4, Vec3, DirectionalLight
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionNode, CollisionBox, CollisionTube, CollisionSphere
from direct.task import Task

class Game(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        self.GRAVITY = 10
        self.speed = 10


        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        winProperties = WindowProperties()
        winProperties.setTitle("Test collisions")
        winProperties.setSize(1024, 780)
        self.win.requestProperties(winProperties)

        self.player = self.loader.loadModel("player.glb")
        self.player.setColor(Vec4(1.0,0.0,0.0,1))
        self.player.setPos(0,0,40)
        self.player.reparentTo(self.render)

        self.platform = self.loader.loadModel("platform.glb")
        self.platform.setColor(Vec4(0.3,0.5,0.7,1))
        self.platform.reparentTo(self.render)

        self.platform2 = self.loader.loadModel("platform.glb")
        self.platform2.setColor(Vec4(1,0.5,0.7,1))
        self.platform2.setScale(.2,.2,.2)
        self.platform2.setPos(-30,0, 10)
        self.platform2.reparentTo(self.render)
        self.platform2.setColor(Vec4(0.5,0,1,1))



        light = DirectionalLight("main light")
        mainlight = self.render.attachNewNode(light)
        mainlight.setPos(100,0,-100)
        mainlight.setColor(Vec4(1,0,0,0.4))
        mainlight.setHpr(0,-90, 0)
        self.render.setLight(mainlight)

        playerColliderNode = CollisionNode("player")
        playerColliderNode.add_solid(CollisionBox(Vec3(0,0,0.5),1,1,1.5))
        playerCollider = self.player.attachNewNode(playerColliderNode)
        #playerCollider.show()

        platformColliderNode = CollisionNode("platform")
        platformColliderNode.add_solid(CollisionBox(Vec3(0,0,0),50,50,1))
        platformCollider = self.platform.attachNewNode(platformColliderNode)
        #platformCollider.show()

        platformColliderNode2 = CollisionNode("platform")
        platformColliderNode2.add_solid(CollisionBox(Vec3(0,0,0),50,50,1))
        platformCollider2 = self.platform2.attachNewNode(platformColliderNode2)
        #platformCollider2.show()

        self.pusher.addCollider(playerCollider, self.player)
        self.cTrav.addCollider(playerCollider, self.pusher)
       
        self.taskMgr.add(self.apply_gravity_task, "apply garvity")

        self.accept('w', self.updateKeyMap, ["forward", True])
        self.accept('w-up', self.updateKeyMap, ["forward", False])
        self.accept('s', self.updateKeyMap, ["backward", True])
        self.accept('s-up', self.updateKeyMap, ["backward", False])
        self.accept('a', self.updateKeyMap, ["left", True])
        self.accept('a-up', self.updateKeyMap, ["left", False])
        self.accept('d', self.updateKeyMap, ["right", True])
        self.accept('d-up', self.updateKeyMap, ["right", False])
        self.accept('u', self.updateKeyMap, ['jump', True])
        self.accept('u-up', self.updateKeyMap, ['jump', False])

        self.keyMap = {
            "right" : False,
            "left" : False,
            "forward" : False,
            "backward" : False,
            "jump" : False
        }

        self.camera.setPos(0, -70, 70)
        self.camera.setP(-40)

    def updateKeyMap(self, key, status):
        self.keyMap[key] = status

    def apply_gravity_task(self, task):
        dt = globalClock.getDt()
        
        #apply gavity
        self.player.setZ(self.player.getZ() - self.GRAVITY * dt)
        
        if self.keyMap["forward"]:
            self.player.setY(self.player.getY() + self.speed * dt)
            self.camera.setY(self.camera.getY() + self.speed * dt)
        if self.keyMap["backward"]:
            self.player.setY(self.player.getY() - self.speed * dt)
            self.camera.setY(self.camera.getY() - self.speed * dt)
        if self.keyMap["right"]:
            self.player.setX(self.player.getX() + self.speed * dt)
            self.camera.setX(self.camera.getX() + self.speed * dt)
        if self.keyMap["left"]:
            self.player.setX(self.player.getX() - self.speed * dt)
            self.camera.setX(self.camera.getX() - self.speed * dt)

        if self.keyMap["jump"]:
            self.player.setZ(self.player.getZ() + 2)

        return task.cont
    

app = Game()
app.run()