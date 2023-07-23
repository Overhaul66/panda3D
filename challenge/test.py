from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Vec3,Vec4
from direct.task import Task
from direct.gui.DirectGui import DirectWaitBar, DirectButton
from panda3d.core import WindowProperties

import sys

class Game(ShowBase):
	def __init__(self):
		super().__init__()

		self.disableMouse()

		self.properties = WindowProperties()
		self.properties.setSize(1024, 600)
		self.win.requestProperties(self.properties)

		# loading bar
		self.bar = DirectWaitBar(	text="loading", 
			   						value = 50, 
									pos = (0,.4,.4),
								    barColor = Vec4(1, 1, 0.09, 1)
								)
									

		self.text = OnscreenText(pos=(0, 0.5), bg=Vec4(1,1,1,1),  font = loader.loadFont("challenge/SuperMario256.ttf"))
	
		self.button1 = DirectButton(text=('About'), scale=0.07, command= self.about, pos=(-0.1,0,-0.1))

		self.button2 = DirectButton(text=('Toggle Fullscreen'), scale=0.07, command = self.fullscreen, pos=(-0.1,0,-0.2))
	
		self.button3 = DirectButton(text=('Exit') , scale=0.07, command = self.exit, pos=(-0.1,0, -0.3))

		# hide all buttons and text
		self.text.hide()
		self.button1.hide()
		self.button2.hide()
		self.button3.hide()
		

		self.taskMgr.add(self.testTime, "loader")

	def testTime(self, task):
		counter = int(task.time) * 10
		if counter >= 110:
			self.bar.hide()
			self.bar['value'] = counter
			self.text.show()

			# show all buttons 
			self.button1.show()
			self.button2.show()
			self.button3.show()

			return task.done
		
		self.bar['value'] = counter
		return task.cont
	
	def about (self):
		self.text['text'] = 'This porgram is a challege...'

	def fullscreen(self):
		self.properties.fullscreen = True
		self.win.requestProperties(self.properties)

	def exit(self):
		sys.exit()

	


game = Game()
game.run()
