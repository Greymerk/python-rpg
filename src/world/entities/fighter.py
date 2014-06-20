'''
Created on 2013-05-26

@author: brian
'''
from entity import Entity
import pygame
from random import randint
from random import choice
from ai import *


class Fighter(Entity):

	living = "fighter.png"
	dead = "body.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.singular = 'a fighter'

		
		self.ai.addAI(Flee(self))
		self.ai.addAI(Cast(self))
		self.ai.addAI(Pursue(self))
		self.ai.addAI(Follow(self))
		self.ai.addAI(Wander(self))

	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getSword()

