'''
Created on 2013-05-16

@author: brian
'''

from entities import ai

import pygame
from entity import Entity

class Snake(Entity):

	living = "snake.png"
	dead = "gore.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.inventory.bar[0] = self.world.itemList['BareHands']()
		
		self.world = world
		self.hostile = True
		
		self.ai.addAI(ai.Flee(self))
		self.ai.addAI(ai.Cast(self))
		self.ai.addAI(ai.Pursue(self))
		self.ai.addAI(ai.Wander(self))
		self.singular = 'a snake'
