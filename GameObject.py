from panda3d.core import Vec3, Vec4
from panda3d.core import CollisionNode, CollisionSphere
from direct.actor.Actor import Actor

FRICTION = 150

class GameObject():
    '''
    Base class for game objects example player, enemy, items

    '''
    def __init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName):
        #set up the game objects model
        self.actor = Actor(modelName, modelAnims)
        self.actor.reparentTo(render)
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

        self.collider.setPythonTag("owner", self)

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