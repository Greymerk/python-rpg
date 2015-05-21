'''
Created on 2013-05-26

@author: brian
'''
from entity import Entity
import pygame
from random import randint
from random import choice
from src.ai import task

class Fighter(Entity):

	living = "fighter"
	dead = "body"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.singular = 'a fighter'

		
		self.ai.addAI(task.Flee(self))
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Pursue(self))
		self.ai.addAI(task.Follow(self))
		self.ai.addAI(task.Wander(self))

	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getSword()
		
	@classmethod
	def onDamage(cls, sounds):
		sounds.get("damage.wav").play()

