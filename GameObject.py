from panda3d.core import Vec3, Vec2
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode

FRICTION = 150.0


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

    # clean objec
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
            "models/act_p3d_chan",
            {"stand": "models/a_p3d_chan_idle", "walk": "models/a_p3d_chan_run"},
            5,
            10,
            "player",
        )
        self.actor.getChild(0).setH(180)

        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        # loop the stand animation
        self.actor.loop("stand")

    def update(self, keys, dt):
        super().update(dt)

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
            # if walkig is false, check if stand animation playing , if not stop walk animation and play stand animation
            standControl = self.actor.getAnimControl("stand")
            if not standControl.isPlaying():
                self.actor.stop("walk")
                self.actor.loop("stand")

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
                 "SimpleEnemy/simpleEnemy.egg",
                 {
                     "stand" : "SimpleEnemy/simpleEnemy-stand.egg",
                     "walk" : "SimpleEnemy/simpleEnemy-walk.egg",
                     "attack" : "SimpleEnemy/simpleEnemy-attack.egg",
                     "die" : "SimpleEnemy/simpleEnemy-die.egg",
                     "spawn" : "SimpleEnemy/simpleEnemy-spawn.egg",
                 },
                 3.0,
                 7.0,
                 "walkingEnemy"
        )

        self.attackDistance = 0.75
        self.acceleration = 100.0

         # direction vector of the enemy
        self.yVector = Vec2(0,1)

    def runLogic(self, player, dt):

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
            self.walking = True
            vectorToPlayer.setZ(0)
            vectorToPlayer.normalize()
            self.velocity += vectorToPlayer * self.acceleration * dt
        else:
            self.walking = False
            self.velocity.set(0,0,0)

        self.actor.setH(heading)