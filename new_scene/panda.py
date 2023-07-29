from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import DirectionalLight, Vec4, Vec3
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText

class MyApp(ShowBase):

    def __init__(self):
        super().__init__()

        self.rot = 0

        self.phoenix_bird = Actor('phoenix_bird/scene.gltf',
                                  {'fly':'phoenix_bird/scene.gltf'}
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
       

    def move_phoenix(self, task):
        dt = globalClock.getDt()
        self.phoenix_bird.setPos(self.phoenix_bird.getPos() + Vec3(1 * dt, 0, 0) )
        return task.cont 


game = MyApp()
game.run()
