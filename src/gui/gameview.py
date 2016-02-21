import pygame
from pygame.color import THECOLORS
import time


from cell import Cell
from viewport import Viewport
from displaypanel import DisplayPanel


class Gameview(object):

	def __init__(self, world, player, images, debug=None):
		self.world = world
		self.player = player
		self.screenSize = (1024, 600)
		self.surface = pygame.display.set_mode(self.screenSize)
		self.images = images
		self.debug = debug
		self.renderTime = 0
		self.boxes = []
		
		self.viewportPos = (28, 28)
		viewportLength = Viewport.size * Cell.size
		self.viewportRect = pygame.Rect(self.viewportPos, (viewportLength, viewportLength))
		self.boxes.append(self.viewportRect)
		self.viewport = Viewport(self.surface.subsurface(self.viewportRect), self.viewportPos, world, player, images)
		
		self.displayPos = (viewportLength + 56, 28)
		self.displayRect = pygame.Rect(self.displayPos, (Cell.size * 12, viewportLength))
		self.display = DisplayPanel(self.surface.subsurface(self.displayRect), self.displayPos, self.player, images)
		
		player.screenshot = self.printscreen

	def draw(self):

		self.surface.fill(THECOLORS["royalblue4"])
		self.viewport.draw()
		self.display.draw()
		if self.debug is not None and self.player.debug:
			self.viewport.display(self.debug())
		
		pygame.display.flip()

	def notify(self, pos, event):
		if self.viewportRect.collidepoint(pos):
			self.viewport.notify(pos, event)
		if self.displayRect.collidepoint(pos):
			self.display.notify(pos, event)
		
	def printscreen(self):
		date = time.gmtime() 
		fileName =	"screenshot_" + \
				str(date[0]) + '-' + \
				str(date[1]) + '-' + \
				str(date[2]) + '-' + \
				str(date[3]-8) + '-' + \
				str(date[4]) + '-' + \
				str(date[5]) + \
				'.jpg'

		pygame.image.save(self.surface, fileName)
