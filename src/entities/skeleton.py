'''
Created on 2013-05-28

@author: brian
'''

import pygame
from random import randint
from random import choice
from items.abilities import MagicMissile


from entity import Entity
from items import *
from entities.ai import *

class Skeleton(Entity):

	living = "skeleton.png"
	dead = "gore.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.world = world
		self.hostile = True
		self.singular = 'a skeleton'
	

class SkeletalWarrior(Skeleton):
	
	def __init__(self, world):
		Skeleton.__init__(self, world)
		

		
		self.ai.addAI(Cast(self))
		self.ai.addAI(Pursue(self))
		self.ai.addAI(Wander(self))
	
	def equip(self):
		self.inventory.bar[0] = self.world.itemList['ShortSword']()
		
class SkeletalArcher(Skeleton):
	
	def __init__(self, world):
		Skeleton.__init__(self, world)
		self.ai.addAI(Fallback(self))
		self.ai.addAI(Cast(self))
		self.ai.addAI(Pursue(self))
		self.ai.addAI(Wander(self))
		
	def equip(self):
		chance = randint(0, 100)
		if chance < 5:
			self.inventory.bar[0] = self.world.itemList['MagicBow']()
		elif chance < 20:
			self.inventory.bar[0] = self.world.itemList['LongBow']()
		else:
			self.inventory.bar[0] = self.world.itemList['ShortBow']()
			
			
class SkeletalMage(Skeleton):
	
	def __init__(self, world):
		Skeleton.__init__(self, world)
		self.ai.addAI(Fallback(self))
		self.ai.addAI(Cast(self))
		self.ai.addAI(Pursue(self))
		self.ai.addAI(Wander(self))
		
	def equip(self):
		self.inventory.bar[0] = self.world.itemList['Staff']()
		self.inventory.bar[0].ability = MagicMissile