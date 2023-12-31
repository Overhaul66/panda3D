from panda3d.core import Vec3, Vec2, Vec4
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode
from panda3d.core import CollisionRay, CollisionHandlerQueue
from panda3d.core import BitMask32
from panda3d.core import Plane, Point3, Point2
from panda3d.core import CollisionSegment
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import PointLight


FRICTION = 150.0

import math
import random

class GameObject:
    def __init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName):
        self.actor = Actor(modelName, modelAnims)
        self.actor.reparentTo(render)
        self.actor.setPos(pos)

        self.maxHealth = maxHealth
        self.health = maxHealth

        self.maxSpeed = maxSpeed

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = 300.0

        self.walking = False

        colliderNode = CollisionNode(colliderName)
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
        self.collider = self.actor.attachNewNode(colliderNode)
        self.collider.setPythonTag("owner", self)

    def update(self, dt):
        speed = self.velocity.length()
        # clamp speed 
        if speed > self.maxSpeed:
            self.velocity.normalize()
            self.velocity *= self.maxSpeed
            speed = self.maxSpeed

        # add friction to velocity
        if not self.walking:
            frictionVal = FRICTION * dt
            if frictionVal > speed:
                self.velocity.set(0, 0, 0)
            # slows down the enenmy over time
            else:
                frictionVec = -self.velocity
                frictionVec.normalize()
                frictionVec *= frictionVal

                self.velocity += frictionVec

        # update player position
        self.actor.setPos(self.actor.getPos() + self.velocity * dt)

    def alterHealth(self, dHealth):
        self.health += dHealth

        # clamp health
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    # clean object
    def cleanup(self):
        if self.collider is not None and not self.collider.isEmpty():
            self.collider.clearPythonTag("owner")
            base.cTrav.removeCollider(self.collider)
            base.pusher.removeCollider(self.collider)

        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None

        self.collider = None

    


class Player(GameObject):
    def __init__(self):
        super().__init__(
            Vec3(0, 0, 0),
            "models/panda_chan/act_p3d_chan",
            {"stand": "models/panda_chan/a_p3d_chan_idle", "walk": "models/panda_chan/a_p3d_chan_run"},
            5,
            10,
            "player",
        )
        self.actor.getChild(0).setH(180)

         #load laser
        self.beamModel = loader.loadModel("models/BambooLaser/bambooLaser.egg")
        self.beamModel.reparentTo(self.actor)
        self.beamModel.setZ(1.5)
        # prevents lights from affecting this model
        self.beamModel.setLightOff()
        self.beamModel.hide()

        self.lastMousePos = Vec2(0,0)
        self.groundPlane = Plane(Vec3(0,0,1), Vec3(0,0,0))
        self.yVector = Vec2(0,1)
       
        base.pusher.addCollider(self.collider, self.actor)
        
        # tell traverser to check collisions with self.collider , using base.pusher
        base.cTrav.addCollider(self.collider, base.pusher)

        mask = BitMask32()
        mask.setBit(1)

        self.collider.node().setIntoCollideMask(mask)

        mask = BitMask32()
        mask.setBit(1)

        self.collider.node().setFromCollideMask(mask)

        # loop the stand animation
        self.actor.loop("stand")

        self.ray = CollisionRay(0,0,0,0,1,0)
        rayNode = CollisionNode("playerRay")
        rayNode.addSolid(self.ray)

        self.rayNodePath = render.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()

        mask = BitMask32()
        mask.setBit(2)
        rayNode.setFromCollideMask(mask)
        mask = BitMask32()
        rayNode.setIntoCollideMask(mask)

        # we want our ray to collide with things so tell the 
        # traverser about it
        base.cTrav.addCollider(self.rayNodePath, self.rayQueue)

        self.damagePerSecond = -5.0

        self.score = 0

        self.scoreUI = OnscreenText(
            text = "0",
            pos = Point2(-1.23,0.65),
            mayChange=True,
        )
        #list to store life images 
        self.healthIcons = []
        # for loop to create and store love images in self.healthIcons
        for i in range(self.maxHealth):
            heartImage = OnscreenImage(
                image= "models/UI/health.png",
                pos = (-1.23 + (i * 0.1),0, 0.8),
                scale=0.04
            )
            #set the transparency of the image
            heartImage.setTransparency(True)

            self.healthIcons.append(heartImage)

        self.beamHitModel = loader.loadModel("models/BambooLaser/bambooLaserHit.egg")
        self.beamHitModel.reparentTo(render)
        self.beamHitModel.setZ(1.5)
        self.beamHitModel.setLightOff()
        self.beamHitModel.hide()

        self.beamHitPulseRate = 0.15
        self.beamHitTimer = 0

        self.beamHitLight = PointLight("beamHitLight")
        self.beamHitLight.setColor(Vec4(0.1,1.0,0.2,1))

        # These "attenuation" values govern how the light
        # fades with distance. They are, respectively,
        # the constant, linear, and quadratic coefficients
        # of the light's falloff equation.  

        self.beamHitLight.setAttenuation((1.0,0.1,0.5))
        self.beamHitLightNodePath = render.attachNewNode(self.beamHitLight)

        self.damageTakenModel = loader.loadModel("models/BambooLaser/playerHit.egg")
        self.damageTakenModel.setLightOff()
        self.damageTakenModel.setZ(0.1)
        self.damageTakenModel.reparentTo(self.actor)
        self.damageTakenModel.hide()

        self.damageTakenModelTimer = 0
        self.damageTakenModelDuration = 0.15

    def alterHealth(self, dHealth):
        self.updateHealthUI()
        self.damageTakenModel.show()
        self.damageTakenModel.setH(random.uniform(0.0,360.0))
        self.damageTakenModelTimer = self.damageTakenModelDuration
        super().alterHealth(dHealth)
        
    def updateHealthUI(self):
        for index, icon in enumerate(self.healthIcons):
            if index < self.health:
                icon.show()
            else:
                icon.hide()

    def updateScore(self):
        self.scoreUI.setText(str(self.score))
        
    def update(self, keys, dt):
        super().update(dt)

        mousePos3D = Point3()
        nearPoint = Point3()
        farPoint = Point3()

        mouseWatcher = base.mouseWatcherNode
        if mouseWatcher.hasMouse():
            mousePos = mouseWatcher.getMouse()
        else:
            mousePos = self.lastMousePos

        # we want to determine the position of the 2D mouse pointer in 3D
        # the extrude function finds the (3D position) third components for the 2D mouse pointer 
        # position
        base.camLens.extrude(mousePos, nearPoint, farPoint)
        self.groundPlane.intersectsLine(mousePos3D,
                                        render.getRelativePoint(base.camera, nearPoint),
                                        render.getRelativePoint(base.camera, farPoint)
                                    )

        self.walking = False

        # respond to key pressed by adding acceleration to the player's velocity 
        if keys["up"]:
            self.walking = True
            self.velocity.addY(self.acceleration * dt)
        if keys["down"]:
            self.walking = True
            self.velocity.addY(-self.acceleration * dt)
        if keys["left"]:
            self.walking = True
            self.velocity.addX(-self.acceleration * dt)
        if keys["right"]:
            self.walking = True
            self.velocity.addX(self.acceleration * dt)
        if keys['shoot']:
            if self.rayQueue.getNumEntries() > 0:
                # flag to determine if an enemy is hit
                scoredHit = False
                # to make the first into object be at index 0
                self.rayQueue.sortEntries()
                # get the object the ray hit first
                rayHit = self.rayQueue.getEntry(0)
                hitPos = rayHit.getSurfacePoint(render)

                hitNodePath = rayHit.getIntoNodePath()
                if hitNodePath.hasPythonTag('owner'):
                   
                    hitObject = hitNodePath.getPythonTag('owner')
                    if not isinstance(hitObject, TrapEnemy):
                        hitObject.alterHealth(self.damagePerSecond*dt)
                        scoredHit = True
                beamLength = (hitPos - self.actor.getPos()).length()
                self.beamModel.setSy(beamLength)
                self.beamModel.show()

                if scoredHit:
                    #show the beam hit when player is hit
                    self.beamHitModel.show()
                    self.beamHitModel.setPos(hitPos)
                    self.beamHitLightNodePath.setPos(hitPos + Vec3(0,0,0.5))
                    #check if the there is a pointlight in the SCENEgraph
                    if  not render.hasLight(self.beamHitLightNodePath):
                        # set the light if not
                        render.setLight(self.beamHitLightNodePath)
                else:
                    if render.hasLight(self.beamHitLightNodePath):
                        render.clearLight(self.beamHitLightNodePath)
                    self.beamHitModel.hide()
        else:
            self.beamModel.hide()
            #if player is not lasering the enemy
            # hide the beam hit model and clear the light
            self.beamHitModel.hide()
            
            if render.hasLight(self.beamHitLightNodePath):
                render.clearLight(self.beamHitLightNodePath)
        # if self.walking is true , stop stand animation
        if self.walking:
            standControl = self.actor.getAnimControl("stand")
            if standControl.isPlaying():
                standControl.stop()
            # if walk animation is not playing, start playing it
            walkControl = self.actor.getAnimControl("walk")
            if not walkControl.isPlaying():
                self.actor.loop("walk")
        else:
            # if walking is false, check if stand animation playing , if not stop walk animation and play stand animation
            standControl = self.actor.getAnimControl("stand")
            if not standControl.isPlaying():
                self.actor.stop("walk")
                self.actor.loop("stand")

        firingVector = Vec3(mousePos3D - self.actor.getPos())
        firingVector2D = firingVector.getXy()
        firingVector2D.normalize()
        firingVector.normalize()

        #find the angle between yVector and firingVector2D
        heading = self.yVector.signedAngleDeg(firingVector2D)

        # makes the player faces the direction of the mouse
        self.actor.setH(heading)

        if firingVector.length() > 0.001:
            self.ray.setOrigin(self.actor.getPos())
            self.ray.setDirection(firingVector)

        # store the mouse pos when mouse is not detected
        self.lastMousePos = mousePos

        self.beamHitTimer -= dt
        if self.beamHitTimer <= 0:
            self.beamHitTimer = self.beamHitPulseRate
            self.beamHitModel.setH(random.uniform(0.0,360.0))
        self.beamHitModel.setScale(math.sin(self.beamHitTimer*3.142/self.beamHitPulseRate)*0.4 + 0.9)

        # accumulate time over time :)
        # if timer is equal to the duration 
        # hide the model
        # this makes the hit model show the model for a period of time
        if self.damageTakenModelTimer > 0:
            self.damageTakenModelTimer -= dt
            self.damageTakenModel.setScale(2.0 - self.damageTakenModelTimer/self.damageTakenModelDuration)
            if self.damageTakenModelTimer <= 0:
                self.damageTakenModel.hide()
        if self.damageTakenModelTimer <= 0:
            self.damageTakenModel.hide()
       
    def cleanup(self):
        base.cTrav.removeCollider(self.rayNodePath)
        # remove scoreUI from root path
        self.scoreUI.removeNode()
        # remove icons from root path
        for icon in self.healthIcons:
            icon.removeNode()
        # remove the beam hit model, and light
        self.beamHitModel.removeNode()
        render.clearLight(self.beamHitLightNodePath)
        self.beamHitLightNodePath.removeNode()

        super().cleanup()

  

class Enemy(GameObject):

    def __init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName):
        super().__init__(pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName)

        self.scoreValue = 1

    def update(self, player, dt):

        super().update(dt)

        self.runLogic(player, dt)

        # handle enemy animations
        if self.walking:
            walkingControl = self.actor.getAnimControl("walk")
            if not walkingControl.isPlaying():
                self.actor.loop("walk")
        # play stand animation if spawn and attack are not playing and enemy is not walking
        else:
            spawnControl = self.actor.getAnimControl("spawn")
            if spawnControl is None or not spawnControl.isPlaying():
                attackControl = self.actor.getAnimControl("attack")
                if attackControl is None or not attackControl.isPlaying(): 
                    standControl = self.actor.getAnimControl("stand")
                    if not standControl.isPlaying():
                        self.actor.loop("stand")

    def runLogic(self, player, dt):
            pass

class WalkingEnemy(Enemy):
    
    def __init__(self, pos):
        super().__init__( pos,
                 "models/SimpleEnemy/simpleEnemy.egg",
                 {
                     "stand" : "models/SimpleEnemy/simpleEnemy-stand.egg",
                     "walk" : "models/SimpleEnemy/simpleEnemy-walk.egg",
                     "attack" : "models/SimpleEnemy/simpleEnemy-attack.egg",
                     "die" : "models/SimpleEnemy/simpleEnemy-die.egg",
                     "spawn" : "models/SimpleEnemy/simpleEnemy-spawn.egg",
                 },
                 3.0,
                 7.0,
                 "walkingEnemy"
        )

        self.attackDelay = 0.3
        # the delay between the start of the attack and the potential of it landing
        # when attck delay timer finishes there is a potential land of attack
        self.attackDelayTimer = 0
        # time the enemy takes to do another attack on the player
        self.attackWaitTimer = 0

        mask = BitMask32()
        mask.setBit(2)

        self.collider.node().setIntoCollideMask(mask)

        self.attackDistance = 0.75
        self.acceleration = 100.0

        # create a segment collision 
        self.attackSegment = CollisionSegment(0, 0, 0, 10, 0, 0)
        segmentNode = CollisionNode("enemyAttackSegment")
        segmentNode.addSolid(self.attackSegment)

        mask = BitMask32()
        mask.setBit(1)

        segmentNode.setFromCollideMask(mask)

        mask = BitMask32()
        segmentNode.setIntoCollideMask(mask)

        self.attackSegmentNodePath = render.attachNewNode(segmentNode)
        self.attackSegmentNodePath.show()
        self.segmentQueue = CollisionHandlerQueue()

        base.cTrav.addCollider(self.attackSegmentNodePath, self.segmentQueue)

        # damage the enemy attack does
        self.attackDamage = -1

         # direction vector of the enemy
        self.yVector = Vec2(0,1)
        
    def runLogic(self, player, dt):

        spawnControl = self.actor.getAnimControl("spawn")
        if spawnControl is not None and spawnControl.isPlaying():
            return

        # set the start and end of the segment
        self.attackSegment.setPointA(self.actor.getPos())
        self.attackSegment.setPointB(self.actor.getPos() + self.actor.getQuat().getForward() * self.attackDistance)
        # get the differnece between the player and the enemy
        # this gives a vector with it direction pointing to the player
        vectorToPlayer = player.actor.getPos() - self.actor.getPos() 

        vectorToPlayer2D = vectorToPlayer.getXy()
        distanceToPlayer = vectorToPlayer2D.length()

        vectorToPlayer2D.normalize()

        # set the angle of the enemy
        heading = self.yVector.signedAngleDeg(vectorToPlayer2D)

        # if player is not in attacking Range 
        if distanceToPlayer > self.attackDistance * 0.9:
            # get the atack animation control
            attackControl = self.actor.getAnimControl("attack")
            if not attackControl.isPlaying():
                self.walking = True
                vectorToPlayer.setZ(0)
                vectorToPlayer.normalize()
                self.velocity += vectorToPlayer * self.acceleration * dt
                self.attackWaitTimer = 0.2
                self.attackDelayTimer = 0
        else:
            self.walking = False
            self.velocity.set(0,0,0)

            if self.attackDelayTimer > 0:
                self.attackDelayTimer -= dt
                # the enemy makes a successful attack landing
                # check if the player was hit
                if self.attackDelayTimer <= 0:
                    # check for a player hit
                    if self.segmentQueue.getNumEntries() > 0: # if true, there was hit
                        # now check if it is the player
                        self.segmentQueue.sortEntries()
                        # get the first hit
                        segmentHit = self.segmentQueue.getEntry(0)
                        hitNodePath = segmentHit.getIntoNodePath()
                        if hitNodePath.hasPythonTag("owner"):
                            # apply damage
                            hitObject = hitNodePath.getPythonTag('owner')
                            hitObject.alterHealth(self.attackDamage)
                            self.attackWaitTimer = 1.0
            elif self.attackWaitTimer > 0:
                self.attackWaitTimer -= dt
                # if the timer has ended
                if self.attackWaitTimer <= 0:
                    # start attack
                    self.attackWaitTimer = random.uniform(0.5, 0.7)
                    self.attackDelayTimer = self.attackDelay
                    self.actor.play("attack")

        self.actor.setH(heading)

    def alterHealth(self, dHealth):
        self.updateHealthVisual()
        super().alterHealth(dHealth)
        
    def updateHealthVisual(self):
        perc = self.health/self.maxHealth
        if perc < 0:
            perc = 0

        self.actor.setColorScale(perc, perc, perc, 1)            

class TrapEnemy(Enemy):

    def __init__(self, pos):
        super().__init__(pos, 
                         "models/SlidingTrap/trap", 
                         {'walk':'models/SlidingTrap/trap-walk',
                          'stand':'models/SlidingTrap/trap-stand'
                          }, 
                         100.0, 
                         10.0, 
                         "trapEnemy")
        
        # make it an active collider object
        base.pusher.add_collider(self.collider, self.actor)
        base.cTrav.add_collider(self.collider, base.pusher)

        self.moveInX = False

        self.moveDirection = 0

        self.ignorePlayer = False
        
        # trap enemy should hit both player and walkingEnemy so 
        # we set their mask here
        mask = BitMask32()
        mask.setBit(1)
        mask.setBit(2)

        self.collider.node().setIntoCollideMask(mask)

        mask = BitMask32()
        mask.setBit(1)
        mask.setBit(2)

        self.collider.node().setFromCollideMask(mask)

    def runLogic(self, player, dt):

        if self.moveDirection != 0:
            self.walking = True
            if self.moveInX:
                self.velocity.addX(self.moveDirection * self.acceleration * dt)
            else:
                self.velocity.addY(self.moveDirection * self.acceleration * dt)
        else:
            self.walking = False
            diff = player.actor.getPos() - self.actor.getPos()

            if self.moveInX:
                detector = diff.y
                movement = diff.x
            else:
                detector = diff.x
                movement = diff.y

            if abs(detector) < 0.5:
                self.moveDirection = math.copysign(1, movement)
