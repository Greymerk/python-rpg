'''
Created on 2013-05-15

@author: brian
'''

import entity
from mobspawner import MobSpawner

from orc import Orc
from rat import Rat
from snake import Snake
from spider import Spider
from headless import Headless
from ettin import Ettin
from fighter import Fighter
from mage import Mage
from bard import Bard
from skeleton import *

lookup = {}
lookup['Orc'] = Orc
lookup['Rat'] = Rat
lookup['Snake'] = Snake
lookup['Spider'] = Spider
lookup['Headless'] = Headless
lookup['Ettin'] = Ettin
lookup['Fighter'] = Fighter
lookup['Mage'] = Mage
lookup['Bard'] = Bard
lookup['SkeletalWarrior'] = SkeletalWarrior
lookup['SkeletalMage'] = SkeletalMage
lookup['SkeletalArcher'] = SkeletalArcher

mobs = {}
mobs['Orc'] = Orc
mobs['Rat'] = Rat
mobs['Snake'] = Snake
mobs['Spider'] = Spider
mobs['Headless'] = Headless
mobs['Ettin'] = Ettin
mobs['SkeletalWarrior'] = SkeletalWarrior
mobs['SkeletalMage'] = SkeletalMage
mobs['SkeletalArcher'] = SkeletalArcher

class MobManager(object):

	def __init__(self, world):
		
		self.world = world
		self.mobs = []
		self.mobSpawner = MobSpawner(self.world, mobs)
	
	def addMob(self, mob):
		self.mobs.append(mob)
		
	def update(self):
		
		for mob in self.mobs:
			mob.update()
			
		for mob in self.mobs:
			if mob.deathTimer <= 0:
				self.mobs.remove(mob)
		
	def turn(self):
		
		self.mobSpawner.spawn()
		
		for mob in self.mobs:
			if self.isPlayerInRange(mob):
				mob.turn()
			
		for mob in self.mobs:
			if mob.deathTimer <= 0:
				self.mobs.remove(mob)
			
	def save(self, chunkPos):
		
		mobData = []
		for mob in self.mobs:
			if mob.inChunk(chunkPos):
				mobData.append(mob.save())
		
		return mobData
	
	def isPlayerInRange(self, entity):
	
		for e in self.world.friendly:
			if e.distance(entity.position) < 40:
				return True

		return False

	def unload(self, chunkPos):

		toRemove = []
		
		for i in range(len(self.mobs)):
			if self.mobs[i].inChunk(chunkPos):
				toRemove.append(i)

		toRemove.reverse()
		for i in toRemove:
			del self.mobs[i]
					 
	def loadEntity(self, data):
		mobType = data['type']
		e = lookup[mobType](self.world)
		e.load(data)
		return e
	
	def load(self, mobData):
		for data in mobData:
			mob = self.loadEntity(data)
			self.mobs.append(mob)