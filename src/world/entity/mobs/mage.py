'''
Created on 2013-05-27

@author: brian
'''

from entity import Entity
import pygame
from random import randint

class Mage(Entity):

	living = "mage.png"
	dead = "body.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.singular = 'a mage'

		self.ai.addAI(self.ai.tasks.Fallback(self))
		self.ai.addAI(self.ai.tasks.Cast(self))
		self.ai.addAI(self.ai.tasks.Follow(self))
		self.ai.addAI(self.ai.tasks.Wander(self))
		
		
	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getDamageStaff()
		self.inventory.bar[1] = self.world.items.weapons.getHealStaff()
		self.inventory.bar[2] = self.world.items.weapons.getResStaff()
		
	@classmethod
	def onDamage(cls, sounds):
		sounds.get("damage.wav").play()