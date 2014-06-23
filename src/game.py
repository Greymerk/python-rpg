import time
import pygame

from world import World
from gui import Gameview
from player import Player
from images import ImageCache

class Game(object):

	def __init__(self):

		pygame.init()
		self.screenSize = (1024, 600)
		pygame.display.set_caption("RPG Game")

		self.seed = 26281376
		self.surface = pygame.display.set_mode(self.screenSize)

		self.world = World(self.seed)
		self.user = Player(self.world)
		self.view = Gameview(self.world, self.user, self.surface, ImageCache())

		self.clock = pygame.time.Clock()

	def run(self):

		while(True):

			self.view.draw()

			if not self.world.update():
				continue
			
			if self.user.turn():
				continue

			self.world.turn()
			self.user.save()
			
			self.clock.tick(30)
