'''
Created on 2013-05-16

@author: brian
'''

import entities
from random import choice
from random import randint

class MobSpawner(object):

	maxMobs = 40
	spawnFrequency = 10

	def __init__(self, world):
		self.world = world

	def spawn(self):
		
		if len(self.world.mobManager.mobs) >= self.maxMobs:
			return
		
		if not (randint(0, self.spawnFrequency) == 0):
			return
		
		mob = self.getRandomMob()
		
		found = self.getSpawnLocation(mob)
		
		if not found:
			return
		
		self.world.mobManager.addMob(mob)
		
	def getRandomMob(self):
		
		randomMobClass = choice(entities.mobs.values())
		mob = randomMobClass(self.world)
		mob.equip()
		return mob
		
	def getSpawnLocation(self, mob):
		
		found = False
		attempts = 0
		
		while not found and attempts < 20:
			found = True
			chunk = self.world.chunkManager.getRandomChunk()
			chunkX, chunkY = chunk.getPos()
			posX = chunkX << 4
			posY = chunkY << 4
			mob.position = (posX + randint(0,15), posY + randint(0,15))
			if not mob.canSpawn(mob.position):
				found = False
			for e in self.world.friendly:
				if e.canSee(mob.position):
					found = False
			attempts += 1
			
		return found
			
		
		
		
		
