'''
Created on 2013-05-27

@author: brian
'''

from entity import Entity
import pygame
from random import randint
from ai import *


class Mage(Entity):

	living = "mage.png"
	dead = "body.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.singular = 'a mage'

		self.ai.addAI(Fallback(self))
		self.ai.addAI(Cast(self))
		self.ai.addAI(Follow(self))
		self.ai.addAI(Wander(self))
		
		
	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getDamageStaff()
		self.inventory.bar[1] = self.world.items.weapons.getHealStaff()
		self.inventory.bar[2] = self.world.items.weapons.getResStaff()
		
