'''
Created on 2013-05-15

@author: brian
'''

from mobspawner import MobSpawner
from mobs import lookup

class MobManager(object):

	def __init__(self, world):
		self.world = world
		self.mobs = []
		self.mobSpawner = MobSpawner(self.world)
	
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
			
