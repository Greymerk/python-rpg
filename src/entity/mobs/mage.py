'''
Created on 2013-05-27

@author: brian
'''

from entity import Entity
import pygame
from random import randint
from src.ai import task
from src.abilities import *

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
		self.abilities = [FireBall, HealBolt, Resurrection]
		
	@classmethod
	def onDamage(cls, sounds):
		sounds.get("damage.wav").play()
