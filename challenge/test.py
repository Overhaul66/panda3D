from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode, Vec3

import hashlib # for hashing

class Game(ShowBase):
	def __init__(self):
		super().__init__()

		font = self.loader.loadFont('SuperMario256.ttf')

		DOB = "21 March 1999"
		hashed_DOB = hashlib.md5(DOB.encode())

		output = "William " + str(hashed_DOB.hexdigest())

		text = TextNode("text node")
		text.setText(output)
		text.setFont(font)
		text.setCardColor(1, 0, 0, 0.2)
		text.setCardAsMargin(4, 4, 4, 4)
		text.setCardDecal(True)
		textNodePath = self.render.attachNewNode(text)
		textNodePath.setScale(0.08)
		textNodePath.setPos(-0.9, 5, 0)

		self.disableMouse()


game = Game()
game.run()
