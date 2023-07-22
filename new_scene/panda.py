from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import DirectionalLight, Vec4, Vec3
from direct.task import Task

class MyApp(ShowBase):

    def __init__(self):
        super().__init__()

        

        self.phoenix_bird = Actor('phoenix_bird/scene.gltf',
                                  {'fly':'phoenix_bird/scene.gltf'}
                                  )
        self.phoenix_bird.setPos(-2000, 900, 0)
        self.phoenix_bird.loop('fly')
        self.phoenix_bird.reparentTo(self.render)

        light = DirectionalLight('light')
        light.setColor(Vec4(1,0,0,1))
        lightNode = self.render.attachNewNode(light)
        lightNode.setP(90)
        self.render.setLight(lightNode)

        

        camera.setPos(-4000, 940 , 500)
        camera.setHpr(-90, -10, 0)
        

        

        self.disable_mouse()

        taskMgr.add(self.move_phoenix, 'move phoenix')

    def move_phoenix(self, task):
        self.phoenix_bird.setPos(self.phoenix_bird.getPos() + Vec3(7, 0, 0) )
        self.camera.setPos(self.camera.getPos() + Vec3(7, 0,0))
        return task.cont 

game = MyApp()
game.run()
