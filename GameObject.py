from panda3d.core import Vec3, Vec4
from panda3d.core import CollisionNode, CollisionSphere
from direct.actor.Actor import Actor

FRICTION = 150

class GameObject():
    '''
    Base class for game objects example player, enemy, 

    '''
    def __init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName):
        #set up the game objects model
        self.actor = Actor(modelName, modelAnims)
        self.actor.reparentTo(self.render)
        self.actor.setPos(pos)

        self.maxHealth = maxHealth
        self.health = maxHealth

        self.maxSpeed = maxSpeed

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = 300.0

        self.walking = False

        #collision node for the game object
        colliderNode = CollisionNode(colliderName)
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
        self.collider = self.actor.attachNewNode(colliderNode)

        self.collider.setPythonTag("owner", self) # adds a reference of the GameObject to the collider

    def update(self, dt):
        
        speed = self.velocity.lenght()          #get speed of velocity

        #if the speed of velocity is greater than maxSpeed 
        if speed > self.maxSpeed:
            self.velocity.normalize()           # normalize the vector, direction is not affected
            self.velocity *= self.maxSpeed      # set the velocity to maxSpeed
            speed = self.maxSpeed               # speed will be altered, set it to maxSpeed

        if not self.walking:                    # if player is about stopping or has stopped 
            frictionVal = FRICTION * dt
            if frictionVal > speed:             
                self.velocity.set(0,0,0)
            else:
                frictionVec = -self.velocity
                frictionVec.normalize()
                frictionVec *= frictionVal

                self.velocity += frictionVec    # add frictionVec to velocity to simulate friction

        self.actor.setPos(self.actor.getPos() + self.velocity * dt)

    
    def alterHealth(self, dHealth):
        self.health += dHealth

        # make sure health does not exceed maxHealth
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    # removes and clears various component of objects associated with this class
    def cleanup(self):
        
        if self.collider is not None and not self.collider.isEmpty():
            self.collider.clearPythonTag("owner")    # removes the class associated with owner
            base.cTrav.removeCollider(self.collider) # removes self.collider from the traverser 
            base.pusher.removeCollider(self.collider)# removes self.collider from the pusher

        if self.actor is not None:
            self.actor.cleanup() # clean ups the actor model
            self.actor.removeNode() # removes the actor model form the node
            self.actor = None 

        self.collider = None

class Player(GameObject):
    '''
    class for player , inherits GameObject
    '''
    pass


class Enemy(GameObject):
    '''
    Base class for all enemies, and subclass of GameObject
    '''
    pass

class WalkingEnemy(Enemy):
    '''
    class for specific type of enemy
    '''
    pass