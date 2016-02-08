import pygame
from pygame.color import THECOLORS
import time

from options import Options
from output import Output
from viewport import Viewport
from status import Status

class Gameview(object):

	def __init__(self, world, player, surface, images, debug=None):
		self.world = world
		self.player = player
		self.surface = surface
		self.images = images
		self.debug = debug
		self.boxes = []
		
		self.viewportPos = (28, 28)
		self.viewportRect = pygame.Rect(self.viewportPos, (17*32, 17*32))
		self.boxes.append(self.viewportRect)
		self.viewport = Viewport(self.surface.subsurface(self.viewportRect), self.viewportPos, world, player, images)
		
		self.optionsPos = (600,28)
		self.optionsRect = pygame.Rect(self.optionsPos, (396, 32 * 6))
		self.boxes.append(self.optionsRect)
		self.options = Options(self.surface.subsurface(self.optionsRect), self.optionsPos, self.player, images)
		
		self.statusPos = (600,252)
		self.statusRect = pygame.Rect(self.statusPos, (396, 32))
		self.boxes.append(self.statusRect)
		self.status = Status(self.surface.subsurface(self.statusRect), self.statusPos, self.player, images)
		
		self.logPos = (600,316)
		self.logRect = pygame.Rect(self.logPos, (396,16*16))
		self.boxes.append(self.logRect)
		self.logWindow = Output(self.surface.subsurface(self.logRect), self.logPos, self.player.log)
		
		player.screenshot = self.printscreen
		
	def update(self):
		self.viewport.update()

	def draw(self):

		self.update()		
		self.surface.fill(THECOLORS["royalblue4"])
		for box in self.boxes:
			pygame.draw.rect(self.surface, THECOLORS["azure2"], box, 5)
		self.options.draw()
		self.status.draw()
		self.logWindow.draw()
		self.viewport.draw()
		if self.debug is not None:
			self.viewport.display(self.debug())
		
		pygame.display.flip()

	def getElement(self, pos):
		if self.viewportRect.collidepoint(pos):
			return self.viewport.getElement(pos)
		if self.optionsRect.collidepoint(pos):
			return self.options.getElement(pos)
		
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
