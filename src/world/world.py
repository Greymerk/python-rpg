import sys
from random import randint
import math
import time
import os
import items

from src.util import Vector2

from entity import MobManager
from entity import Party
from terrain import ChunkManager
import terrain

class World:

	def __init__(self, seed, sounds):
	
		if not os.path.isdir('save'):
			os.mkdir('save')
	
		self.sounds = sounds
		self.items = items.ItemFactory(terrain)
		self.combat = 0
		self.seed = seed
		self.chunkManager = ChunkManager(self)
		self.time = 0
		self.mobManager = MobManager(self)
		self.friendly = []
		self.spawn = self.getSpawnLocation()
		self.log = None
		self.materials = terrain.lookup



	def getSeed(self):
		return self.seed

	def update(self):
			
		done = True
		for e in list(set(self.friendly) | set(self.mobManager.mobs)):
			if e.update() is False:
				done = False
		return done
			

	def turn(self):
		
		self.mobManager.turn()
		for e in self.friendly:
			e.turn()
					
		self.time += 1

	def isLocationPassable(self, location):

		entity = self.getEntityFromLocation(location)
		if entity is not None and entity.isAlive():
			return False
				
		tile = self.chunkManager.getTile((location[0], location[1]))
		if tile is None:
			return False
			
		return tile.isPassable()
		
	def look(self, position):

		for e in list(set(self.mobManager.mobs) | set(self.friendly)):
			if e.position == position:
				if e.name is not None:
					return e.name
				return e.singular 
			
		env = self.chunkManager		
		
		x, y = position
		t = env.getTile((x, y))
		m = t.getGround()
		return m.singular

	def getTile(self, location):
		return self.chunkManager.getTile(location)
	
	def setTile(self, location, tileId):
		self.chunkManager.setTile(location, tileId)
		return True
	
	def build(self, location, tileId):
		tile = self.getTile(location)
		if not tile.canBuild():
			return False
		self.chunkManager.setTile(location, tileId)
		return True
		
	def destroy(self, location):
		tile = self.getTile(location)
		return tile.destroy()
		
	def quit(self):
		self.chunkManager.saveChunks()
		sys.exit()
			
	def getSpawnLocation(self):
		x = 0
		y = 0
		
		spread = 1
		
		while(not (self.getTile((x, y)).getGround().spawnable)):
			x = randint(-spread,spread)
			y = randint(-spread,spread)
			if spread is 100:
				print "Failed to find a place to spawn"
				break
			spread += 1
			
		return x, y
	
	def getEntityFromLocation(self, location, living = True):
		for e in self.getAllEntities():
			if e.position == location:
				if living and e.isAlive():
					return e
				elif not living and not e.isAlive(): 
					return e
			
		return None

	def getAllEntities(self):
		return list(set(self.mobManager.mobs) | set(self.friendly))

	def obscured(self, start, end):

		vStart = Vector2(start[0] + 0.5, start[1] + 0.5)
		vEnd = Vector2(end[0] + 0.5, end[1] + 0.5)

		angle = math.atan2(float(vEnd.y - vStart.y), float(vEnd.x - vStart.x))
		step = Vector2(math.cos(angle) * 0.2, math.sin(angle) * 0.2)

		while vStart.dist(vEnd) > 0.5:
			tile = self.getTile((int(vStart.x), int(vStart.y)))
			if not tile.isTransparent():
				return True
			vStart + step

		return False
		
	def loadParty(self, data):
		party = Party(self)
		party.load(data)
		return party


