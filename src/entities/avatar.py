import pygame
from entity import Entity

from ai import *

class Avatar(Entity):

	living = "player.png"
	dead = "body.png"

	def __init__(self, world):
		
		Entity.__init__(self, world)
		self.world = world
		self.position = self.world.spawn
		self.singular = 'the avatar'
		self.range = 1

		self.ai.addAI(Flee(self))
		self.ai.addAI(Attack(self))
		self.ai.addAI(Pursue(self))
		self.ai.addAI(Follow(self))
		self.ai.addAI(Wander(self))
		
