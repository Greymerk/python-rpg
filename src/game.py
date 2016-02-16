import time
import pygame

from world import World
from gui import Gameview
from player import Player
from images import ImageCache
from sounds import SoundCache

class Game(object):

	FPS = 30

	def __init__(self):

		pygame.init()
		self.screenSize = (1024, 600)
		pygame.display.set_caption("RPG Game")

		self.seed = 26281376
		self.surface = pygame.display.set_mode(self.screenSize)

		self.world = World(self.seed, SoundCache())
		self.user = Player(self)
		self.view = Gameview(self.world, self.user, self.surface, ImageCache(), self.debug)

		self.clock = pygame.time.Clock()
		self.renderTime = 0
		self.processTime = 0		
		
	def run(self):

		while(True):

			self.clock.tick(Game.FPS)
			t = time.time()
			self.view.draw()
			self.renderTime = time.time() - t
			
			t = time.time()
			if not self.world.update():
				continue
			
			if self.user.turn():
				continue

			self.world.turn()
			self.user.save()
			self.processTime = time.time() - t
	
	def debug(self):
		msg = []
		msg.append(['FPS: ' + str(int(self.clock.get_fps()))])
		msg.append(['Mobs: ' + str(len(self.world.mobManager.mobs))])
		msg.append(['Chunks: ' + str(len(self.world.chunkManager.chunkCache))])
		msg.append(['Render: ' + str(int(self.renderTime * 1000)) + 'ms'])
		msg.append(['World: ' + str(int(self.processTime * 1000)) + 'ms'])
		return msg
