from collections import deque
from random import choice
from mapcache import MapCache

from chunk import Chunk

class ChunkManager:

	def __init__(self, world):
		self.world = world
		self.chunkCache = deque()
		self.mapCache = MapCache(self, self.world.seed)
		self.maxCacheSize = 64
		self.chunkSize = 16

	
	def getChunk(self, x, y):
		chunkX = x >> 4
		chunkY = y >> 4

		for c in self.chunkCache:
			if c.getPos() == (chunkX, chunkY):
				return c

		toLoad = Chunk((chunkX, chunkY), self.world.getSeed(), self.world.mobManager, self.mapCache)
		self.chunkCache.append(toLoad)
		
		if len(self.chunkCache) > self.maxCacheSize:
			toUnload = self.chunkCache.popleft()
			toUnload.unload()

		return toLoad
	
	def getMap(self, x, y):
		return self.mapCache.get(x, y)
	
	def getTile(self, (x, y)):
		c = self.getChunk(x, y)
		return c.getTile(x % self.chunkSize, y % self.chunkSize)

	def isLoaded(self, x, y):
				
		for c in self.chunkCache:
			if c.pos is (x, y):
				return True
			
		return False
	
	def setTile(self, (x, y), id):
		c = self.getChunk(x, y)
		c.setTile((x, y), id)

	
	def saveChunks(self):
		for c in self.chunkCache:
			c.unload()
			
	def getRandomChunk(self):
		return choice(self.chunkCache)