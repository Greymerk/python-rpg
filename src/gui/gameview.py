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
		
		self.background = images.get("interface")
		
		viewportRect = pygame.Rect((28, 28), (17*32, 17*32))
		self.viewport = Viewport(self.surface.subsurface(viewportRect), world, player, images)
		
		optionsRect = pygame.Rect((600,28), (396, 16*12))
		self.options = Options(self.surface.subsurface(optionsRect), self.player)
		
		statusRect = pygame.Rect((600,252), (396, 32))
		self.status = Status(self.surface.subsurface(statusRect), self.player, images)
		
		logRect = pygame.Rect((600,316),(396,16*16))
		self.logWindow = Output(self.surface.subsurface(logRect), self.player.log)
		
		player.screenshot = self.printscreen
		
	def update(self):
		self.viewport.update()

	def draw(self):

		self.update()		
		self.surface.blit(self.background, (0,0))
		self.options.draw()
		self.status.draw()
		self.logWindow.draw()
		self.viewport.draw()
		if self.debug is not None:
			self.viewport.display(self.debug())
		
		pygame.display.flip()

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
