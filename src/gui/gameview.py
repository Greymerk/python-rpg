import pygame
from pygame.color import THECOLORS
import time

from gui.options import Options
from gui.output import Output
from gui.viewport import Viewport

class Gameview(object):

	def __init__(self, world, player, surface, textureDir="images/u5/"):
		self.world = world
		self.player = player
		self.surface = surface
		
		self.background = pygame.image.load(textureDir + "interface.png").convert_alpha()
		
		viewportRect = pygame.Rect((28, 28), (17*32, 17*32))
		self.viewport = Viewport(self.surface.subsurface(viewportRect), world, player, textureDir)
		
		logRect = pygame.Rect((600,316),(396,16*16))
		self.logWindow = Output(self.surface.subsurface(logRect), self.player.log)
		
		optionsRect = pygame.Rect((600,28), (396, 16*12))
		self.options = Options(self.surface.subsurface(optionsRect), self.player)
		
		player.screenshot = self.printscreen
		
	def update(self):
		self.viewport.update()

	def draw(self):

		self.update()		
		self.surface.blit(self.background, (0,0))
		self.options.draw()
		self.logWindow.draw()
		self.viewport.draw()
		
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
