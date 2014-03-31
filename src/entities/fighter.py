'''
Created on 2013-05-26

@author: brian
'''
from entity import Entity
import pygame
from random import randint
from random import choice
from ai import *

from items import ShortSword
from items import LongSword
from items import MagicSword

class Fighter(Entity):

	living = "fighter.png"
	dead = "body.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.singular = 'a fighter'
		self.inventory.weapon = choice([ShortSword(), LongSword(), MagicSword()])
		
		self.ai.addAI(Flee(self))
		self.ai.addAI(Cast(self))
		self.ai.addAI(Pursue(self))
		self.ai.addAI(Follow(self))
		self.ai.addAI(Wander(self))

	def equip(self):
		self.inventory.weapon = choice([ShortSword(), LongSword(), MagicSword()])

