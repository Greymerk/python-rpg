'''
Created on 2013-05-27

@author: brian
'''

from entity import Entity
import pygame
from random import randint
from ai import task

class Mage(Entity):

	living = "mage"
	dead = "body"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.singular = 'a mage'

		self.ai.addAI(task.Fallback(self))
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Follow(self))
		self.ai.addAI(task.Wander(self))
		
		
	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getDamageStaff()
		self.inventory.bar[2] = self.world.items.weapons.getHealStaff()
		self.inventory.bar[3] = self.world.items.weapons.getResStaff()
		
	@classmethod
	def onDamage(cls, sounds):
		sounds.get("damage.wav").play()