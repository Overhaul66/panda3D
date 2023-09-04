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

import random
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

        #player character will be created in the startGame method
        self.player = None
        self.enemies = []
        self.trapEnemies = []
        self.deadEnemies = []

        # setup some spawn points
        self.spawnPoints = []
        numPointsPerWall = 5
        for i in range(numPointsPerWall):
            coord = 7.0/numPointsPerWall + 0.5
            self.spawnPoints.append(Vec3(-7.0, coord, 0))
            self.spawnPoints.append(Vec3(7.0, coord, 0))
            self.spawnPoints.append(Vec3(coord, -7.0, 0))
            self.spawnPoints.append(Vec3(coord, 7.0, 0))
        # Values to control when to spawn enemies, and
        # how many enemies there may be at once     
        self.initialSpawnInterval = 1.0
        self.minimumSpawnInterval = 0.2
        self.spawnInterval = self.initialSpawnInterval
        self.spawnTimer = self.spawnInterval
        self.maxEnemies = 2
        self.maximumMaxEnemies = 20

        self.numTrapsPerSide = 2

        self.difficultyInterval = 5.0
        self.difficultyTimer = self.difficultyInterval

        self.exitFunc = self.cleanup

        self.startGame()

        self.disableMouse()

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def updateTask(self, task):
        dt = globalClock.getDt()
        
        #if the player is dead , or has not started to play
        # ignore this logic
        if self.player is not None:
            if self.player.health > 0:
                self.player.update(self.keyMap, dt)

                # wait to spawn an enemy
                self.spawnTimer -= dt
                if self.spawnTimer <= 0:
                    self.spawnTimer = self.spawnInterval
                    self.spawnEnemy()

                # update all enemies and traps
                [enemy.update(self.player, dt) for enemy in self.enemies]
                [trap.update(self.player, dt) for trap in self.trapEnemies]
                #get a list of daed enemies
                newlyDeadEnemies = [enemy for enemy in self.enemies if enemy.health <= 0]
                #remove dead enemies from enemy list
                self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]

                for enemy in newlyDeadEnemies:
                    enemy.collider.removeNode()
                    enemy.actor.play("die")
                    self.player.score += enemy.scoreValue
                # update player score if dead enemies are more that 0
                if len(newlyDeadEnemies) > 0:
                    self.player.updateScore()

                self.deadEnemies += newlyDeadEnemies

                enemiesAnimatingDeaths = []
                for enemy in self.deadEnemies:
                    deathAnimControl = enemy.actor.getAnimControl("die")
                    if deathAnimControl is None or not deathAnimControl.isPlaying():
                        enemy.cleanup()
                    else:
                        enemiesAnimatingDeaths.append(enemy)
                self.deadEnemies = enemiesAnimatingDeaths

                #make the game more difficult over time
                self.difficultyTimer -= dt
                if self.difficultyTimer <= 0:
                    self.difficultyTimer = self.difficultyInterval
                    if self.maxEnemies < self.maximumMaxEnemies:
                        self.maxEnemies += 1
                    if self.spawnInterval > self.minimumSpawnInterval:
                        self.spawnInterval -= 0.1


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
    
    def startGame(self):
        # clean up anything in the
        # level : enemies, traps, etc. before
        # starting a new one.
        self.cleanup()
        self.player = Player()

        self.maxEnemies = 2
        self.spawnInterval = self.initialSpawnInterval
        self.difficultyTimer = self.difficultyInterval

        sideTrapSlots = [
            [],
            [],
            [],
            []
        ]
        trapSlotDistance = 0.4
        slotPos = -8 + trapSlotDistance
        while slotPos < 8:
            if abs(slotPos) > 1.0:
                sideTrapSlots[0].append(slotPos)
                sideTrapSlots[1].append(slotPos)
                sideTrapSlots[2].append(slotPos)
                sideTrapSlots[3].append(slotPos)
            slotPos += trapSlotDistance

        for i in range(self.numTrapsPerSide):
            slot = sideTrapSlots[0].pop(random.randint(0, len(sideTrapSlots[0])-1))
            trap = TrapEnemy(Vec3(slot, 7.0, 0))
            self.trapEnemies.append(trap)

            slot = sideTrapSlots[1].pop(random.randint(0, len(sideTrapSlots[1])-1))
            trap = TrapEnemy(Vec3(slot, -7.0, 0))
            self.trapEnemies.append(trap)

            slot = sideTrapSlots[2].pop(random.randint(0, len(sideTrapSlots[2])-1))
            trap = TrapEnemy(Vec3(7.0,slot, 0))
            trap.moveInX = True
            self.trapEnemies.append(trap)

            slot = sideTrapSlots[3].pop(random.randint(0, len(sideTrapSlots[3])-1))
            trap = TrapEnemy(Vec3(-7.0,slot, 0))
            trap.moveInX = True
            self.trapEnemies.append(trap)

    def cleanup(self):
        # Call our various cleanup methods,
        # empty the various lists,
        # and make the player "None" again.

        for enemy in self.enemies:
            enemy.cleanup()
        self.enemies = []

        for enemy in self.deadEnemies:
            enemy.cleanup()
        self.deadEnemies = []

        for trap in self.trapEnemies:
            trap.cleanup()
        self.trapEnemies = []

        if self.player is not None:
            self.player.cleanup()
            self.player = None

    def quit(self):
        self.cleanup()
        base.userExit()

    def spawnEnemy(self):
        if len(self.enemies) < self.maxEnemies:
            spawnPoint = random.choice(self.spawnPoints)
            newEnemy = WalkingEnemy(spawnPoint)
            self.enemies.append(newEnemy)

game = Game()
game.run()
