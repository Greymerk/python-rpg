'''
Created on 2013-05-28

@author: brian
'''

import pygame
from random import randint
from random import choice



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
		
		self.inventory.bar[0] = self.world.itemList['ShortSword']()
		
		self.ai.addAI(Cast(self))
		self.ai.addAI(Pursue(self))
		self.ai.addAI(Wander(self))
		
class SkeletalArcher(Skeleton):
	
	def __init__(self, world):
		Skeleton.__init__(self, world)
				
		chance = randint(0, 100)
		if chance < 5:
			self.inventory.bar[0] = self.world.itemList['MagicBow']()
		elif chance < 20:
			self.inventory.bar[0] = self.world.itemList['LongBow']()
		else:
			self.inventory.bar[0] = self.world.itemList['ShortBow']()
		
		self.ai.addAI(Fallback(self))
		self.ai.addAI(Cast(self))
		self.ai.addAI(Pursue(self))
		self.ai.addAI(Wander(self))
		
class SkeletalMage(Skeleton):
	
	def __init__(self, world):
		Skeleton.__init__(self, world)
		
		self.inventory.bar[0] = self.world.itemList['MageStaff']()
		
		self.ai.addAI(Fallback(self))
		self.ai.addAI(Cast(self))
		self.ai.addAI(Pursue(self))
		self.ai.addAI(Wander(self))
